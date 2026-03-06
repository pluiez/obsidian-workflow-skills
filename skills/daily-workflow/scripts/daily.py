#!/usr/bin/env python3
"""
Daily workflow automation script for Obsidian vault.

Handles today/ workspace initialization with safety checks:
1. If today/ is non-empty and its date == today → already initialized, refuse
2. If today's date matches the latest archive date → already archived today, refuse
3. If today/ is non-empty and date is in the past → archive, then create fresh
4. If today/ is empty or doesn't exist → create fresh
5. If today/ has a future date → warn and exit

Usage:
    python daily.py <vault_path>
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import date, datetime
from pathlib import Path

from loguru import logger

# --- Constants ---

DAILY_FILES = ["tasks.md", "knowledge.md", "ideas.md"]
TEMPLATE_MAP = {
    "tasks.md": "daily-tasks.md",
    "knowledge.md": "daily-knowledge.md",
    "ideas.md": "daily-ideas.md",
}
DATE_PATTERN = re.compile(r'^date:\s*"(\d{4}-\d{2}-\d{2})"\s*$', re.MULTILINE)
REVIEWED_PATTERN = re.compile(r'^reviewed:\s*(true|false)\s*$', re.MULTILINE)


# --- Frontmatter helpers ---

def read_date_from_frontmatter(filepath: Path) -> date | None:
    """Extract date field from YAML frontmatter. Returns None if missing or invalid."""
    if not filepath.is_file():
        return None
    text = filepath.read_text(encoding="utf-8")
    match = DATE_PATTERN.search(text)
    if not match:
        return None
    try:
        return date.fromisoformat(match.group(1))
    except ValueError:
        return None


def read_reviewed_from_frontmatter(filepath: Path) -> bool | None:
    """Extract reviewed field from YAML frontmatter. Returns None if missing."""
    if not filepath.is_file():
        return None
    text = filepath.read_text(encoding="utf-8")
    match = REVIEWED_PATTERN.search(text)
    if not match:
        return None
    return match.group(1) == "true"


# --- Directory inspection ---

def detect_today_date(today_dir: Path) -> date | None:
    """Read date from the first daily file that has one."""
    for filename in DAILY_FILES:
        d = read_date_from_frontmatter(today_dir / filename)
        if d is not None:
            return d
    return None


def get_latest_archive_date(archive_dir: Path) -> date | None:
    """Get the most recent date from archive/ directory structure."""
    if not archive_dir.is_dir():
        return None
    dates: list[date] = []
    for month_dir in archive_dir.iterdir():
        if not month_dir.is_dir() or not re.match(r"\d{4}-\d{2}$", month_dir.name):
            continue
        for day_dir in month_dir.iterdir():
            if not day_dir.is_dir() or not re.match(r"\d{4}-\d{2}-\d{2}$", day_dir.name):
                continue
            try:
                dates.append(date.fromisoformat(day_dir.name))
            except ValueError:
                continue
    return max(dates) if dates else None


def is_dir_empty(path: Path) -> bool:
    """Check if directory doesn't exist or has no children."""
    if not path.exists():
        return True
    return not any(path.iterdir())


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
        if is_dir_empty(today_dir):
            today_dir.rmdir()
    else:
        month_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(today_dir), str(date_dir))

    return date_dir


def resolve_templates_dir() -> Path:
    """Locate the templates/ directory relative to this script."""
    return Path(__file__).resolve().parent.parent / "templates"


def create_workspace(today_dir: Path, target_date: date) -> None:
    """Create fresh today/ workspace from templates."""
    templates_dir = resolve_templates_dir()
    today_dir.mkdir(parents=True, exist_ok=True)
    date_str = target_date.isoformat()
    datetime_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for filename, template_name in TEMPLATE_MAP.items():
        template_path = templates_dir / template_name
        if not template_path.is_file():
            logger.warning("Template not found: {}", template_path)
            continue
        content = template_path.read_text(encoding="utf-8")
        content = content.replace("{{date}}", date_str)
        content = content.replace("{{datetime}}", datetime_str)
        (today_dir / filename).write_text(content, encoding="utf-8")


# --- Workflow logic ---

def handle_nonempty_today(
    today_dir: Path, archive_dir: Path, today: date
) -> None:
    """Handle case where today/ already has content: validate, archive if stale, create fresh."""
    existing_date = detect_today_date(today_dir)

    if existing_date is None:
        logger.error("today/ is non-empty but no date found in frontmatter.")
        files = [f.name for f in today_dir.iterdir() if f.is_file()]
        logger.error("Files in today/: {}", ", ".join(files) if files else "(none)")
        logger.error("Please check that each file's frontmatter contains a valid 'date' field.")
        sys.exit(1)

    if existing_date > today:
        logger.error("today/ has a future date: {}, but today is {}.",
                      existing_date.isoformat(), today.isoformat())
        logger.error(
            "Please correct the 'date' field in frontmatter, "
            "or back up today/ and delete it to reinitialize."
        )
        sys.exit(1)

    if existing_date == today:
        logger.info("today/ is already initialized for {}.", today.isoformat())
        logger.info("Nothing to do — workspace is current.")
        sys.exit(0)

    # existing_date < today: check reviewed before archiving
    reviewed = read_reviewed_from_frontmatter(today_dir / "tasks.md")
    days_ago = (today - existing_date).days
    if reviewed is False:
        logger.error(
            "today/ contains work from {} ({} day(s) ago), today is {}.",
            existing_date.isoformat(), days_ago, today.isoformat(),
        )
        logger.error("This workspace has not been reviewed yet.")
        logger.error("Please complete the daily review before initializing a new workspace.")
        logger.info("Hint: use the daily-review skill to review and archive.")
        sys.exit(1)

    # All checks passed — archive then create
    logger.info("Step 1: Archiving today/ (date: {})...", existing_date.isoformat())
    archive_path = archive_today(today_dir, archive_dir, existing_date)
    logger.info("Archived to: {}", archive_path)

    logger.info("Step 2: Creating fresh today/ for {}...", today.isoformat())
    create_workspace(today_dir, today)
    logger.info("Done.")


def handle_empty_today(
    today_dir: Path, archive_dir: Path, today: date
) -> None:
    """Handle case where today/ is empty or doesn't exist: validate, create fresh."""
    latest_archive = get_latest_archive_date(archive_dir)
    if latest_archive == today:
        logger.error("today's date ({}) already exists in archive.", today.isoformat())
        logger.error("Cannot initialize — today has already been archived.")
        logger.info("If this is a mistake, manually remove the archive entry.")
        sys.exit(1)

    logger.info("Creating today/ for {}...", today.isoformat())
    create_workspace(today_dir, today)
    logger.info("Done.")


# --- Entry point ---

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Initialize today/ workspace in an Obsidian vault."
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
    today = date.today()

    logger.info("Daily workflow script — {}", today.isoformat())
    logger.info("Vault: {}", vault_root)

    if is_dir_empty(today_dir):
        handle_empty_today(today_dir, archive_dir, today)
    else:
        handle_nonempty_today(today_dir, archive_dir, today)

    logger.info("Today's workspace is ready:")
    for filename in DAILY_FILES:
        logger.info("  today/{}", filename)


if __name__ == "__main__":
    main()
