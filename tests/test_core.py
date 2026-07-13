import pandas as pd
import pytest

from timeblock.core import (
    TIME_BLOCKS,
    add_block_record,
    add_pomodoro_record,
    block_minutes,
    count_pomodoros,
    empty_log,
    filter_by_date,
    load_log,
    summarize_by_category,
    summarize_by_date,
)


def test_empty_log_has_columns():
    df = empty_log()

    assert list(df.columns) == [
        "date",
        "type",
        "block",
        "start",
        "end",
        "minutes",
        "category",
        "note",
    ]


def test_block_minutes():
    assert block_minutes("morning") == 180
    assert block_minutes("afternoon") == 240
    assert block_minutes("night") == 180


def test_unknown_block_raises_error():
    with pytest.raises(ValueError):
        block_minutes("unknown")


def test_add_block_record(tmp_path):
    path = tmp_path / "time_log.csv"

    df = add_block_record(
        path=path,
        record_date="2026-07-13",
        block="morning",
        category="Japanese",
        note="NHK listening",
    )

    assert len(df) == 1
    assert df.loc[0, "type"] == "block"
    assert df.loc[0, "minutes"] == 180
    assert df.loc[0, "category"] == "Japanese"


def test_add_pomodoro_record(tmp_path):
    path = tmp_path / "time_log.csv"

    df = add_pomodoro_record(
        path=path,
        category="Programming",
        minutes=25,
        note="pytest practice",
        record_date="2026-07-13",
        start="20:00",
    )

    assert len(df) == 1
    assert df.loc[0, "type"] == "pomodoro"
    assert df.loc[0, "start"] == "20:00"
    assert df.loc[0, "end"] == "20:25"
    assert df.loc[0, "minutes"] == 25


def test_summarize_by_category():
    df = pd.DataFrame(
        {
            "category": ["Japanese", "Programming", "Japanese"],
            "minutes": [180, 25, 60],
        }
    )

    summary = summarize_by_category(df)

    assert int(summary["Japanese"]) == 240
    assert int(summary["Programming"]) == 25


def test_summarize_by_date():
    df = pd.DataFrame(
        {
            "date": ["2026-07-13", "2026-07-13", "2026-07-14"],
            "minutes": [180, 25, 60],
        }
    )

    summary = summarize_by_date(df)

    assert int(summary["2026-07-13"]) == 205
    assert int(summary["2026-07-14"]) == 60


def test_count_pomodoros():
    df = pd.DataFrame(
        {
            "type": ["block", "pomodoro", "pomodoro"],
        }
    )

    assert count_pomodoros(df) == 2


def test_filter_by_date():
    df = pd.DataFrame(
        {
            "date": ["2026-07-13", "2026-07-14"],
            "category": ["Japanese", "Programming"],
        }
    )

    result = filter_by_date(df, "2026-07-13")

    assert len(result) == 1
    assert result.iloc[0]["category"] == "Japanese"


def test_load_log_creates_file(tmp_path):
    path = tmp_path / "new_log.csv"

    df = load_log(path)

    assert path.exists()
    assert list(df.columns) == [
        "date",
        "type",
        "block",
        "start",
        "end",
        "minutes",
        "category",
        "note",
    ]