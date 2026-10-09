
import pytest

from streamstats.errors import StreamStatsError
from streamstats.models import validate_event


@pytest.fixture
def valid_event():
    return {
        "timestamp": "2026-10-07T12:00:00+03:00",
        "level": "INFO",
        "source": "loader",
        "message": "Начало чтения файла",
    }


def test_valid_event_accepted(valid_event):
    assert validate_event(valid_event) is None


def test_missing_required_field_rejected(valid_event):
    del valid_event["source"]

    with pytest.raises(StreamStatsError):
        validate_event(valid_event)


@pytest.mark.parametrize(
    "level",
    ["UNKNOWN", "", "info", "ERRORS"],
)
def test_invalid_level_rejected(valid_event, level):
    valid_event["level"] = level

    with pytest.raises(StreamStatsError):
        validate_event(valid_event)


@pytest.mark.parametrize(
    "timestamp",
    [
        "not-a-date",
        "",
        "2026-99-99T25:61:00",
    ],
)
def test_invalid_timestamp_rejected(valid_event, timestamp):
    valid_event["timestamp"] = timestamp

    with pytest.raises(StreamStatsError):
        validate_event(valid_event)


def test_null_instead_of_event_rejected():
    with pytest.raises(StreamStatsError):
        validate_event(None)


def test_empty_source_rejected(valid_event):
    valid_event["source"] = ""

    with pytest.raises(StreamStatsError):
        validate_event(valid_event)


def test_non_string_message_rejected(valid_event):
    valid_event["message"] = 123

    with pytest.raises(StreamStatsError):
        validate_event(valid_event)
