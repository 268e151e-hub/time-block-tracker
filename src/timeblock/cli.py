"""Command-line interface for Time Block Tracker."""

from __future__ import annotations

import argparse
from pathlib import Path

from timeblock.core import (
    add_block_record,
    add_pomodoro_record,
    count_pomodoros,
    filter_by_date,
    load_log,
    summarize_by_category,
)
from timeblock.plot import plot_category_summary, plot_daily_summary


DEFAULT_LOG_PATH = Path("data/time_log.csv")


def print_summary(df):
    """Print a simple summary by category."""
    if df.empty:
        print("No records found.")
        return

    summary = summarize_by_category(df)
    total = int(summary.sum())
    pomodoros = count_pomodoros(df)

    print("Summary")
    print("-------")

    for category, minutes in summary.items():
        print(f"{category}: {int(minutes)} min")

    print("-------")
    print(f"Total: {total} min")
    print(f"Pomodoro sessions: {pomodoros}")


def main():
    parser = argparse.ArgumentParser(
        description="Record daily activities with time blocks and Pomodoro sessions."
    )

    parser.add_argument(
        "--log",
        default=str(DEFAULT_LOG_PATH),
        help="Path to the time log CSV file.",
    )

    subparsers = parser.add_subparsers(dest="command")

    add_block_parser = subparsers.add_parser(
        "add-block",
        help="Add a predefined time block record.",
    )
    add_block_parser.add_argument("--date", required=True)
    add_block_parser.add_argument("--block", required=True)
    add_block_parser.add_argument("--category", required=True)
    add_block_parser.add_argument("--note", default="")

    add_pomodoro_parser = subparsers.add_parser(
        "add-pomodoro",
        help="Add a Pomodoro-style focus session.",
    )
    add_pomodoro_parser.add_argument("--category", required=True)
    add_pomodoro_parser.add_argument("--minutes", type=int, default=25)
    add_pomodoro_parser.add_argument("--note", default="")
    add_pomodoro_parser.add_argument("--date", default=None)
    add_pomodoro_parser.add_argument("--start", default=None)

    summary_parser = subparsers.add_parser(
        "summary",
        help="Show a summary of records.",
    )
    summary_parser.add_argument("--date", default=None)

    plot_parser = subparsers.add_parser(
        "plot",
        help="Create summary plots as PDF files.",
    )
    plot_parser.add_argument(
        "--output-dir",
        default="reports",
        help="Directory to save plot PDF files.",
    )

    args = parser.parse_args()
    log_path = Path(args.log)

    if args.command == "add-block":
        add_block_record(
            path=log_path,
            record_date=args.date,
            block=args.block,
            category=args.category,
            note=args.note,
        )
        print("Block record added.")

    elif args.command == "add-pomodoro":
        add_pomodoro_record(
            path=log_path,
            category=args.category,
            minutes=args.minutes,
            note=args.note,
            record_date=args.date,
            start=args.start,
        )
        print("Pomodoro record added.")

    elif args.command == "summary":
        df = load_log(log_path)

        if args.date is not None:
            df = filter_by_date(df, args.date)
            print(f"Date: {args.date}")

        print_summary(df)

    elif args.command == "plot":
        df = load_log(log_path)
        output_dir = Path(args.output_dir)

        category_path = plot_category_summary(
            df,
            output_dir / "category_summary.pdf",
        )
        daily_path = plot_daily_summary(
            df,
            output_dir / "daily_summary.pdf",
        )

        print(f"Created: {category_path}")
        print(f"Created: {daily_path}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()