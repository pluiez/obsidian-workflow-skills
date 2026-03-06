#!/usr/bin/env python3
"""
Scan archive/ directory and list dates with actual archives.

Usage:
    python scan_archive.py <vault_path> [--days N]

Options:
    --days N    Only show dates within the last N days (default: 30)

Output:
    One line per archived date (YYYY-MM-DD), sorted ascending.
    Summary line at the end with total count and date range.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, timedelta
from pathlib import Path

from loguru import logger


# --- Core logic ---

def scan_dates(archive_dir: Path, max_days: int | None = None) -> list[date]:
    """Scan archive/ for YYYY-MM/YYYY-MM-DD directories, return sorted dates."""
    if not archive_dir.is_dir():
        return []

    cutoff = date.today() - timedelta(days=max_days) if max_days else None
    dates: list[date] = []

    for month_dir in archive_dir.iterdir():
        if not month_dir.is_dir() or not re.match(r"\d{4}-\d{2}$", month_dir.name):
            continue
        for day_dir in month_dir.iterdir():
            if not day_dir.is_dir() or not re.match(r"\d{4}-\d{2}-\d{2}$", day_dir.name):
                continue
            try:
                d = date.fromisoformat(day_dir.name)
            except ValueError:
                continue
            if cutoff and d < cutoff:
                continue
            dates.append(d)

    dates.sort()
    return dates


# --- Entry point ---

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan archive/ for archived dates.")
    parser.add_argument(
        "vault_path",
        type=Path,
        help="Path to the Obsidian vault root directory",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Limit to last N days (default: 30)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    vault_root = args.vault_path.resolve()

    if not vault_root.is_dir():
        logger.error("Vault path does not exist: {}", vault_root)
        sys.exit(1)

    archive_dir = vault_root / "archive"
    dates = scan_dates(archive_dir, args.days)

    if not dates:
        logger.info("No archives found within the last {} days.", args.days)
        sys.exit(0)

    for d in dates:
        logger.info("{}", d.isoformat())

    logger.info(
        "--- {} days archived, from {} to {} ---",
        len(dates),
        dates[0].isoformat(),
        dates[-1].isoformat(),
    )


if __name__ == "__main__":
    main()
