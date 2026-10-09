
from streamstats.analysis import analyze_events, create_stats, final_stats


def make_event(
    timestamp="2026-10-07T12:00:00+03:00",
    level="INFO",
    source="loader",
    message="Test event",
):
    return {
        "timestamp": timestamp,
        "level": level,
        "source": source,
        "message": message,
    }


def test_create_stats_empty_report():
    stats = create_stats()

    assert stats["total_events"] == 0
    assert stats["skipped"] == 0


def test_analyze_event_increments_total():
    stats = create_stats()

    analyze_events(make_event(), stats)
    final_stats(stats)

    assert stats["total_events"] == 1


def test_multiple_events_counted():
    stats = create_stats()

    analyze_events(make_event(source="loader"), stats)
    analyze_events(
        make_event(
            timestamp="2026-10-07T13:00:00+03:00",
            source="worker",
        ),
        stats,
    )
    final_stats(stats)

    assert stats["total_events"] == 2
