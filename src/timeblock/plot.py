"""Plotting functions for Time Block Tracker."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from timeblock.core import summarize_by_category, summarize_by_date


def plot_category_summary(df: pd.DataFrame, output_path: str | Path) -> Path:
    """Create a bar chart of total minutes by category."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    summary = summarize_by_category(df)

    fig, ax = plt.subplots(figsize=(6, 4))

    if summary.empty:
        ax.text(0.5, 0.5, "No records", ha="center", va="center")
        ax.set_axis_off()
    else:
        summary.plot(kind="bar", ax=ax)
        ax.set_title("Time Allocation by Category")
        ax.set_xlabel("Category")
        ax.set_ylabel("Minutes")
        ax.tick_params(axis="x", rotation=30)

    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)

    return output_path


def plot_daily_summary(df: pd.DataFrame, output_path: str | Path) -> Path:
    """Create a line chart of total minutes by date."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    summary = summarize_by_date(df)

    fig, ax = plt.subplots(figsize=(6, 4))

    if summary.empty:
        ax.text(0.5, 0.5, "No records", ha="center", va="center")
        ax.set_axis_off()
    else:
        summary.plot(kind="line", marker="o", ax=ax)
        ax.set_title("Daily Tracked Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Minutes")
        ax.tick_params(axis="x", rotation=30)

    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)

    return output_path