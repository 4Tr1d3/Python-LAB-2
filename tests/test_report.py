
import json

from streamstats.analysis import create_stats, final_stats
from streamstats.report import write_report


def test_write_report_creates_json_file(tmp_path):
    output_path = tmp_path / "report.json"
    stats = final_stats(create_stats())

    write_report(stats, output_path)

    assert output_path.exists()

    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert report["total_events"] == 0
    assert report["skipped"] == 0


def test_report_preserves_unicode(tmp_path):
    output_path = tmp_path / "report.json"
    stats = final_stats(create_stats())
    stats["example"] = "Привет, мир!"

    write_report(stats, output_path)

    report_text = output_path.read_text(encoding="utf-8")
    report = json.loads(report_text)

    assert report["example"] == "Привет, мир!"
    assert "Привет, мир!" in report_text
