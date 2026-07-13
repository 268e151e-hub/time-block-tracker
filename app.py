"""Streamlit web app for Time Block Tracker."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from timeblock.core import (
    TIME_BLOCKS,
    add_block_record,
    add_pomodoro_record,
    filter_by_date,
    load_log,
    summarize_by_category,
)
from timeblock.plot import plot_category_summary, plot_daily_summary


LOG_PATH = Path("data/time_log.csv")


st.set_page_config(
    page_title="Time Block Tracker",
    page_icon="⏱️",
    layout="centered",
)

st.title("⏱️ Time Block Tracker")
st.write("Record your daily time blocks and Pomodoro study sessions.")

tab1, tab2, tab3 = st.tabs(["Add Record", "Summary", "Plots"])


with tab1:
    st.header("Add a new record")

    record_type = st.radio(
        "Record type",
        ["Time block", "Pomodoro"],
        horizontal=True,
    )

    record_date = st.date_input("Date")
    category = st.selectbox(
        "Category",
        [
            "Japanese",
            "Programming",
            "Research",
            "JobHunting",
            "Rest",
            "Housework",
            "Other",
        ],
    )
    note = st.text_input("Note")

    if record_type == "Time block":
        block = st.selectbox("Time block", list(TIME_BLOCKS.keys()))

        start, end = TIME_BLOCKS[block]
        st.write(f"Selected time: {start} - {end}")

        if st.button("Add time block"):
            add_block_record(
                path=LOG_PATH,
                record_date=record_date.isoformat(),
                block=block,
                category=category,
                note=note,
            )
            st.success("Time block record added.")

    else:
        start = st.text_input("Start time", value="20:00")
        minutes = st.number_input(
            "Minutes",
            min_value=1,
            max_value=240,
            value=25,
            step=5,
        )

        if st.button("Add Pomodoro"):
            add_pomodoro_record(
                path=LOG_PATH,
                category=category,
                minutes=int(minutes),
                note=note,
                record_date=record_date.isoformat(),
                start=start,
            )
            st.success("Pomodoro record added.")


with tab2:
    st.header("Daily summary")

    summary_date = st.date_input("Summary date")

    df = load_log(LOG_PATH)
    daily_df = filter_by_date(df, summary_date.isoformat())

    if daily_df.empty:
        st.info("No records found for this date.")
    else:
        summary = summarize_by_category(daily_df)
        st.dataframe(summary.rename("minutes"))

        total = int(summary.sum())
        st.metric("Total minutes", total)
        st.metric("Total hours", round(total / 60, 2))

        st.subheader("Raw records")
        st.dataframe(daily_df)


with tab3:
    st.header("Plots")

    df = load_log(LOG_PATH)

    if df.empty:
        st.info("No records yet.")
    else:
        if st.button("Generate PDF plots"):
            category_path = plot_category_summary(
                df,
                Path("reports/category_summary.pdf"),
            )
            daily_path = plot_daily_summary(
                df,
                Path("reports/daily_summary.pdf"),
            )

            st.success("Plots generated.")
            st.write(f"Created: {category_path}")
            st.write(f"Created: {daily_path}")

        st.subheader("Current category summary")
        summary = summarize_by_category(df)
        st.bar_chart(summary)