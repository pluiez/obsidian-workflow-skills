#!/usr/bin/env python3
"""
Archive script for daily-review.

Sets reviewed=true in today/tasks.md frontmatter, then moves today/ to
archive/YYYY-MM/YYYY-MM-DD/ using the date from frontmatter.

All preconditions are validated before any file mutations occur.

Usage:
    python archive.py <vault_path>
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import date
from pathlib import Path

from loguru import logger

# --- Constants ---

DATE_PATTERN = re.compile(r'^date:\s*"(\d{4}-\d{2}-\d{2})"\s*$', re.MULTILINE)
REVIEWED_PATTERN = re.compile(r'^reviewed:\s*(true|false)\s*$', re.MULTILINE)


# --- Frontmatter helpers ---

def read_frontmatter_field(filepath: Path, pattern: re.Pattern) -> str | None:
    """Extract a field value from YAML frontmatter by regex. Returns None if missing."""
    if not filepath.is_file():
        return None
    text = filepath.read_text(encoding="utf-8")
    match = pattern.search(text)
    return match.group(1) if match else None


def set_reviewed_true(filepath: Path) -> None:
    """Set reviewed: true in frontmatter. Raises ValueError if field not found."""
    text = filepath.read_text(encoding="utf-8")
    new_text, count = REVIEWED_PATTERN.subn("reviewed: true", text)
    if count == 0:
        raise ValueError(f"No 'reviewed' field found in {filepath}")
    filepath.write_text(new_text, encoding="utf-8")


# --- Precondition checks ---

def validate_preconditions(today_dir: Path, tasks_file: Path) -> date:
    """
    Validate all preconditions before any file mutation.
    Returns the archive date on success, exits on failure.
    """
    # Check today/ exists and has content
    if not today_dir.is_dir() or not any(today_dir.iterdir()):
        logger.error("today/ is empty or does not exist. Nothing to archive.")
        sys.exit(1)

    # Check tasks.md exists
    if not tasks_file.is_file():
        logger.error("today/tasks.md does not exist.")
        sys.exit(1)

    # Read and validate date from frontmatter
    date_str = read_frontmatter_field(tasks_file, DATE_PATTERN)
    if date_str is None:
        logger.error("Could not read date from today/tasks.md frontmatter.")
        sys.exit(1)

    try:
        archive_date = date.fromisoformat(date_str)
    except ValueError:
        logger.error("Invalid date format in frontmatter: {}", date_str)
        sys.exit(1)

    # Check reviewed field exists (so set_reviewed_true won't fail)
    reviewed_str = read_frontmatter_field(tasks_file, REVIEWED_PATTERN)
    if reviewed_str is None:
        logger.error("No 'reviewed' field found in today/tasks.md frontmatter.")
        sys.exit(1)

    if reviewed_str == "true":
        logger.warning("today/tasks.md is already marked as reviewed.")

    return archive_date


# --- File operations ---

def archive_today(today_dir: Path, archive_dir: Path, target_date: date) -> Path:
    """Move today/ to archive/YYYY-MM/YYYY-MM-DD/."""
    month_dir = archive_dir / target_date.strftime("%Y-%m")
    date_dir = month_dir / target_date.isoformat()

    if date_dir.exists():
        logger.warning("Archive target already exists: {}", date_dir)
        logger.info("Merging files into existing archive directory...")
        for item in today_dir.iterdir():
            dest = date_dir / item.name
            if dest.exists():
                logger.info("Skipping {} (already archived)", item.name)
            else:
                shutil.move(str(item), str(dest))
        # Remove today/ if empty after merge
        if not any(today_dir.iterdir()):
            today_dir.rmdir()
    else:
        month_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(today_dir), str(date_dir))

    return date_dir


# --- Entry point ---

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Archive today/ workspace in an Obsidian vault."
    )
    parser.add_argument(
        "vault_path",
        type=Path,
        help="Path to the Obsidian vault root directory",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    vault_root = args.vault_path.resolve()

    if not vault_root.is_dir():
        logger.error("Vault path does not exist: {}", vault_root)
        sys.exit(1)

    today_dir = vault_root / "today"
    archive_dir = vault_root / "archive"
    tasks_file = today_dir / "tasks.md"

    # Phase 1: Validate everything before touching any files
    archive_date = validate_preconditions(today_dir, tasks_file)

    # Phase 2: Execute mutations (all preconditions already verified)
    logger.info("Step 1: Setting reviewed=true in today/tasks.md...")
    set_reviewed_true(tasks_file)
    logger.info("Done.")

    logger.info("Step 2: Archiving today/ (date: {})...", archive_date.isoformat())
    archive_path = archive_today(today_dir, archive_dir, archive_date)
    logger.info("Archived to: {}", archive_path)
    logger.info("Archive complete. today/ has been cleared.")


if __name__ == "__main__":
    main()
