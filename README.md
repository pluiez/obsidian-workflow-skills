# Obsidian Workflow Skills

**English** | [中文](README.zh-CN.md)

A set of AI Agent skills for structured daily workflows in Obsidian: task management, knowledge recording, idea capture, daily review with archiving, and distilling archived notes into long-form articles.

Design principles:

- **Separation of concerns** — tasks, knowledge, and ideas live in three separate files to avoid editing conflicts
- **Fixed workspace** — `today/` is always the current entry point; open the vault and start working immediately
- **Review-driven archiving** — archiving requires a completed review, ensuring every day has a summary
- **Two-level distillation** — daily output accumulates in `today/` → archived to `archive/` → periodically distilled into `articles/`
- **Automated rotation** — scripts handle initialization, archiving, and safety checks with no manual file management

## 1. Project Structure

```
obsidian-workflow-skills/
├── workflow.md                     # Workflow design doc & interaction examples
└── skills/
    ├── daily-workflow/             # Skill: daily workflow
    │   ├── SKILL.md                #   Skill definition
    │   ├── scripts/
    │   │   └── daily.py            #   Workspace initialization script
    │   ├── templates/              #   Daily note templates
    │   │   ├── daily-tasks.md
    │   │   ├── daily-knowledge.md
    │   │   └── daily-ideas.md
    │   └── references/
    │       └── format.md           #   Daily note format spec
    ├── daily-review/               # Skill: daily review
    │   ├── SKILL.md                #   Skill definition
    │   ├── scripts/
    │   │   └── archive.py          #   Archive script
    │   └── references/
    │       └── format.md           #   Review & tagging format spec
    └── write-article/              # Skill: knowledge distillation (articles)
        ├── SKILL.md                #   Skill definition
        ├── scripts/
        │   └── scan_archive.py     #   Archive scanner script
        └── references/
            ├── format.md           #   Article format spec
            └── example-article.md  #   Example article
```

## 2. Skills

### 2.1 daily-workflow — Daily Workflow

Manages initialization and daily updates of the `today/` workspace.

**Initialization** (morning): runs `daily.py` to create the day's workspace → loads carry-over tasks from the latest archive → guides the user through planning today's tasks and writes them to `tasks.md`. The script handles edge cases such as archiving stale workspaces, preventing duplicate initialization, and blocking when a review is pending.

**Updates** (daytime): the user updates the workspace at any time using natural language — check off completed tasks, record knowledge, capture ideas. Every update is previewed before writing.

### 2.2 daily-review — Daily Review

Guides the user through an end-of-day review in three phases:

1. **Review summary** — tallies task completion and generates a concise, objective review written to `tasks.md`
2. **Content supplement** — checks for any missed knowledge or ideas to add
3. **Tagging** — adds content-based tags to all three files in order (tasks → knowledge → ideas), deduplicating across files

After completion, `archive.py` automatically moves `today/` to `archive/YYYY-MM/YYYY-MM-DD/`.

### 2.3 write-article — Knowledge Distillation

Distills topics from archived notes in `archive/` and produces long-form articles saved to `articles/`.

Workflow: choose a time range → scan archives and suggest topics → draft an outline → expand into a full article → review and finalize. Articles are not simple note concatenations — they integrate across days, add background context, and form a coherent narrative.

## 3. Vault Directory Structure

The Obsidian vault using these skills must follow this layout:

```
vault/
├── today/                  # Current-day workspace (fixed entry point)
│   ├── tasks.md            #   Today's tasks (work / study / life / review)
│   ├── knowledge.md        #   Today's knowledge notes
│   └── ideas.md            #   Today's ideas
├── archive/                # Historical archive (organized by month/day)
│   └── YYYY-MM/
│       └── YYYY-MM-DD/
│           ├── tasks.md
│           ├── knowledge.md
│           └── ideas.md
└── articles/               # Long-form articles
```

## 4. Installation & Usage

### 4.1 Requirements

- Python 3.10+
- [loguru](https://github.com/Delgan/loguru)

```bash
pip install loguru
```

### 4.2 As Agent Skills

Register the skill directories (`skills/daily-workflow/`, `skills/daily-review/`, `skills/write-article/`) with an AI agent that supports the SKILL.md convention (e.g. Cursor, Codex). The agent will automatically trigger the appropriate skill based on user intent and follow the workflow defined in each SKILL.md.

### 4.3 Running Scripts Standalone

Each skill's Python script can also be run independently:

```bash
# Initialize today's workspace
python skills/daily-workflow/scripts/daily.py /path/to/vault

# Archive (after review is complete)
python skills/daily-review/scripts/archive.py /path/to/vault

# Scan archive (list archived dates)
python skills/write-article/scripts/scan_archive.py /path/to/vault [--days N]
```

### 4.4 Obsidian Plugin Dependency

- [obsidian-linter](https://github.com/platers/obsidian-linter) — automatically maintains the `updated` timestamp in frontmatter

## 5. License

[GPL-3.0](LICENSE)
