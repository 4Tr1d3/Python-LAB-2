
import json

import pytest

from streamstats.analysis import create_stats
from streamstats.errors import StreamStatsError
from streamstats.parser import read_csv, read_jsonl


def make_event(message="Тестовое событие"):
    return {
        "timestamp": "2026-10-07T12:00:00+03:00",
        "level": "INFO",
        "source": "loader",
        "message": message,
    }


def test_read_jsonl(tmp_path):
    path = tmp_path / "events.jsonl"
    events = [
        make_event("Первое событие"),
        make_event("Второе событие"),
    ]
    path.write_text(
        "\n".join(json.dumps(event, ensure_ascii=False) for event in events)
        + "\n",
        encoding="utf-8",
    )

    result = list(
        read_jsonl(path, skip_invalid=False, stats=create_stats())
    )

    assert len(result) == 2
    assert result[0]["message"] == "Первое событие"
    assert result[1]["message"] == "Второе событие"


def test_read_csv(tmp_path):
    path = tmp_path / "events.csv"
    path.write_text(
        "timestamp,level,source,message\n"
        '2026-10-07T12:00:00+03:00,INFO,loader,"Книги, чтение"\n',
        encoding="utf-8",
    )

    result = list(
        read_csv(path, skip_invalid=False, stats=create_stats())
    )

    assert len(result) == 1
    assert result[0]["source"] == "loader"
    assert result[0]["message"] == "Книги, чтение"


def test_empty_jsonl(tmp_path):
    path = tmp_path / "empty.jsonl"
    path.write_text("", encoding="utf-8")

    assert list(
        read_jsonl(path, skip_invalid=False, stats=create_stats())
    ) == []

def test_empty_csv_with_header(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text(
        "timestamp,level,source,message\n",
        encoding="utf-8",
    )

    assert list(
        read_csv(path, skip_invalid=False, stats=create_stats())
    ) == []


def test_invalid_jsonl_raises_error(tmp_path):
    path = tmp_path / "broken.jsonl"
    path.write_text(
        '{"timestamp":"2026-10-07T12:00:00+03:00",'
        '"level":"INFO","source":"loader","message":"OK"}\n'
        '{"broken":\n',
        encoding="utf-8",
    )

    with pytest.raises(StreamStatsError):
        list(
            read_jsonl(path, skip_invalid=False, stats=create_stats())
        )


def test_skip_invalid_jsonl(tmp_path):
    path = tmp_path / "mixed.jsonl"
    valid_event = make_event()
    path.write_text(
        json.dumps(valid_event, ensure_ascii=False)
        + "\n"
        + '{"broken":\n'
        + json.dumps(make_event("После ошибки"), ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )
    stats = create_stats()

    result = list(
        read_jsonl(path, skip_invalid=True, stats=stats)
    )

    assert len(result) == 2
    assert result[1]["message"] == "После ошибки"
    assert stats["skipped"] == 1


def test_invalid_csv_event_raises_error(tmp_path):
    path = tmp_path / "broken.csv"
    path.write_text(
        "timestamp,level,source,message\n"
        "not-a-date,INFO,loader,Message\n",
        encoding="utf-8",
    )

    with pytest.raises(StreamStatsError):
        list(
            read_csv(path, skip_invalid=False, stats=create_stats())
        )


def test_unicode_is_preserved(tmp_path):
    path = tmp_path / "unicode.jsonl"
    event = make_event("Hello Привет Hola Bonjour Hallo Ciao Olá مرحبا こんにちは 안녕하세요 你好 🤖")
    path.write_text(
        json.dumps(event, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    result = list(
        read_jsonl(path, skip_invalid=False, stats=create_stats())
    )

    assert result[0]["message"] == "Hello Привет Hola Bonjour Hallo Ciao Olá مرحبا こんにちは 안녕하세요 你好 🤖"
