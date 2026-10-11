import json
import subprocess
import sys
from pathlib import Path


def test_multiple_csv_files(tmp_path):
    file1 = tmp_path / "first.csv"
    file2 = tmp_path / "second.csv"
    report = tmp_path / "report.json"

    file1.write_text(
        "timestamp,level,source,message\n"
        "2026-10-07T09:00:00+00:00,INFO,loader,Started\n"
        "2026-10-07T09:05:00+00:00,ERROR,api,Request failed\n",
        encoding="utf-8",
    )

    file2.write_text(
        "timestamp,level,source,message\n"
        "2026-10-07T09:10:00+00:00,CRITICAL,api,Service unavailable\n"
        "2026-10-07T09:15:00+00:00,WARNING,worker,Retrying\n",
        encoding="utf-8",
    )

    project_root = Path(__file__).resolve().parents[1]
    src_path = project_root / "src"

    import os
    env = os.environ.copy()
    env["PYTHONPATH"] = str(src_path) + os.pathsep + env.get("PYTHONPATH", "")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "streamstats",
            "analyze",
            str(file1),
            str(file2),
            "--format",
            "csv",
            "--output",
            str(report),
        ],
        cwd=project_root,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    assert result.returncode == 0, result.stderr
    assert report.exists(), "JSON-отчёт не создан"

    data = json.loads(report.read_text(encoding="utf-8"))

    
    assert data["total_events"] == 4
    assert data["count_level"] == {
        "INFO": 1,
        "ERROR": 1,
        "CRITICAL": 1,
        "WARNING": 1,
    }
    assert data["count_source"] == {
        "loader": 1,
        "api": 2,
        "worker": 1,
    }
    assert data["first_timestamp"] == "2026-10-07T09:00:00+00:00"
    assert data["last_timestamp"] == "2026-10-07T09:15:00+00:00"