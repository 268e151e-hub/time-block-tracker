# Time Block Tracker

[![CI](https://github.com/268e151e-hub/time-block-tracker/actions/workflows/ci.yml/badge.svg)](https://github.com/268e151e-hub/time-block-tracker/actions/workflows/ci.yml)

A lightweight command-line tool for recording daily activities using predefined time blocks and Pomodoro-style focus sessions.
A lightweight command-line tool for recording daily activities using predefined time blocks and Pomodoro-style focus sessions.

## Purpose

This tool helps users track how they spend their time every day. It supports two types of records:

- **Time blocks** for retrospective daily logging
- **Pomodoro sessions** for focused study/work logging

It also provides summaries and generates PDF charts for visualization.

## Installation

```bash
pip install -e ".[dev]"
```

## Quick Start

### Add a time block record

```bash
timeblock add-block --date 2026-07-13 --block morning --category Japanese --note "NHK listening"
```

### Add a Pomodoro record

```bash
timeblock add-pomodoro --date 2026-07-13 --start 20:00 --category Programming --minutes 25 --note "pytest practice"
```

### Show a daily summary

```bash
timeblock summary --date 2026-07-13
```

### Generate PDF charts

```bash
timeblock plot
```

Generated files:

- `reports/category_summary.pdf`
- `reports/daily_summary.pdf`

## Web Interface

This tool also provides a simple Streamlit web interface.

```bash
python -m streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

## Development Setup

```bash
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest
```

## Project Structure

```text
src/timeblock/      source code
tests/              unit tests
data/               CSV log data
reports/            generated PDF charts
.github/workflows/  CI configuration
```

## License

MIT License