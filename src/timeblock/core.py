"""Core functions for Time Block Tracker."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd


COLUMNS = [
    "date",
    "type",
    "block",
    "start",
    "end",
    "minutes",
    "category",
    "note",
]


TIME_BLOCKS = {
    "early_morning": ("06:00", "09:00"),
    "morning": ("09:00", "12:00"),
    "noon": ("12:00", "14:00"),
    "afternoon": ("14:00", "18:00"),
    "evening": ("18:00", "21:00"),
    "night": ("21:00", "24:00"),
}


def empty_log() -> pd.DataFrame:
    """Return an empty time log DataFrame."""
    return pd.DataFrame(columns=COLUMNS)


def ensure_log_file(path: str | Path) -> Path:
    """Create an empty log CSV file if it does not exist."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        empty_log().to_csv(path, index=False)

    return path


def load_log(path: str | Path) -> pd.DataFrame:
    """Load a time log CSV file."""
    path = ensure_log_file(path)
    return pd.read_csv(path)


def block_minutes(block: str) -> int:
    """Return the length of a predefined time block in minutes."""
    if block not in TIME_BLOCKS:
        raise ValueError(f"Unknown time block: {block}")

    start, end = TIME_BLOCKS[block]

    start_time = datetime.strptime(start, "%H:%M")

    if end == "24:00":
        end_time = datetime.strptime("00:00", "%H:%M") + timedelta(days=1)
    else:
        end_time = datetime.strptime(end, "%H:%M")

    return int((end_time - start_time).total_seconds() // 60)


def add_block_record(
    path: str | Path,
    record_date: str,
    block: str,
    category: str,
    note: str = "",
) -> pd.DataFrame:
    """Add a predefined time block record to the log."""
    df = load_log(path)

    if block not in TIME_BLOCKS:
        raise ValueError(f"Unknown time block: {block}")

    start, end = TIME_BLOCKS[block]

    new_record = {
        "date": record_date,
        "type": "block",
        "block": block,
        "start": start,
        "end": end,
        "minutes": block_minutes(block),
        "category": category,
        "note": note,
    }

    df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
    df.to_csv(path, index=False)

    return df


def add_pomodoro_record(
    path: str | Path,
    category: str,
    minutes: int = 25,
    note: str = "",
    record_date: str | None = None,
    start: str | None = None,
) -> pd.DataFrame:
    """Add a Pomodoro-style focus session to the log."""
    df = load_log(path)

    if record_date is None:
        record_date = date.today().isoformat()

    if start is None:
        start = datetime.now().strftime("%H:%M")

    start_time = datetime.strptime(start, "%H:%M")
    end = (start_time + timedelta(minutes=minutes)).strftime("%H:%M")

    new_record = {
        "date": record_date,
        "type": "pomodoro",
        "block": "",
        "start": start,
        "end": end,
        "minutes": minutes,
        "category": category,
        "note": note,
    }

    df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
    df.to_csv(path, index=False)

    return df


def summarize_by_category(df: pd.DataFrame) -> pd.Series:
    """Summarize total minutes by category."""
    if df.empty:
        return pd.Series(dtype="int64")

    return df.groupby("category")["minutes"].sum().sort_values(ascending=False)


def summarize_by_date(df: pd.DataFrame) -> pd.Series:
    """Summarize total minutes by date."""
    if df.empty:
        return pd.Series(dtype="int64")

    return df.groupby("date")["minutes"].sum()


def count_pomodoros(df: pd.DataFrame) -> int:
    """Count the number of Pomodoro records."""
    if df.empty:
        return 0

    return int((df["type"] == "pomodoro").sum())


def filter_by_date(df: pd.DataFrame, record_date: str) -> pd.DataFrame:
    """Return records for a specific date."""
    return df[df["date"] == record_date]