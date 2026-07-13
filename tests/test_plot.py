import pandas as pd

from timeblock.plot import plot_category_summary, plot_daily_summary


def test_plot_category_summary_creates_pdf(tmp_path):
    df = pd.DataFrame(
        {
            "date": ["2026-07-13", "2026-07-13"],
            "category": ["Japanese", "Programming"],
            "minutes": [180, 25],
        }
    )

    output_path = tmp_path / "category_summary.pdf"

    result = plot_category_summary(df, output_path)

    assert result.exists()
    assert result.suffix == ".pdf"


def test_plot_daily_summary_creates_pdf(tmp_path):
    df = pd.DataFrame(
        {
            "date": ["2026-07-13", "2026-07-14"],
            "category": ["Japanese", "Programming"],
            "minutes": [180, 25],
        }
    )

    output_path = tmp_path / "daily_summary.pdf"

    result = plot_daily_summary(df, output_path)

    assert result.exists()
    assert result.suffix == ".pdf"