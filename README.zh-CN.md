# Obsidian Workflow Skills

**中文** | [English](README.md)

一组 AI Agent 技能（Skills），为 Obsidian vault 提供结构化的每日工作流：任务管理、知识记录、灵感捕捉、每日回顾与归档、以及从历史笔记中沉淀文章。

设计理念：

- **关注点分离** — tasks、knowledge、ideas 三个独立文件，编辑互不干扰
- **固定工作台** — `today/` 永远是当前入口，打开 vault 直接使用
- **回顾驱动归档** — 必须完成回顾才能归档，确保每天有总结沉淀
- **两级沉淀** — 日常产出在 `today/` 积累 → 归档到 `archive/` → 定期整合为 `articles/`
- **自动化轮转** — 脚本处理初始化、归档等操作，无需手动管理文件

## 1. 项目结构

```
obsidian-workflow-skills/
├── workflow.md                     # 工作流设计文档与交互模拟
└── skills/
    ├── daily-workflow/             # 技能：每日工作流
    │   ├── SKILL.md                #   技能定义
    │   ├── scripts/
    │   │   └── daily.py            #   工作区初始化脚本
    │   ├── templates/              #   每日笔记模板
    │   │   ├── daily-tasks.md
    │   │   ├── daily-knowledge.md
    │   │   └── daily-ideas.md
    │   └── references/
    │       └── format.md           #   每日笔记格式规范
    ├── daily-review/               # 技能：每日回顾
    │   ├── SKILL.md                #   技能定义
    │   ├── scripts/
    │   │   └── archive.py          #   归档脚本
    │   └── references/
    │       └── format.md           #   回顾与标签格式规范
    └── write-article/              # 技能：知识沉淀（写文章）
        ├── SKILL.md                #   技能定义
        ├── scripts/
        │   └── scan_archive.py     #   存档扫描脚本
        └── references/
            ├── format.md           #   文章格式规范
            └── example-article.md  #   文章示例
```

## 2. 三个技能

### 2.1 daily-workflow — 每日工作流

管理 `today/` 工作区的初始化和日常更新。

**初始化流程**（早晨）：运行 `daily.py` 创建当日工作区 → 从最近存档中读取遗留任务 → 引导用户规划今日计划并写入 `tasks.md`。脚本会自动处理过期工作区的归档、防重复初始化、未回顾拦截等边界情况。

**更新流程**（白天）：用户随时用自然语言更新——勾选已完成的任务、记录学到的知识、捕捉灵感想法。每次更新都会先预览再确认写入。

触发示例：「开始今天的工作」「加个任务」「学到个东西」「搞定了」

### 2.2 daily-review — 每日回顾

引导用户完成每日回顾，包含三个阶段：

1. **回顾总结** — 统计任务完成情况，生成简洁客观的回顾文本写入 `tasks.md`
2. **内容补充** — 检查是否有遗漏的 knowledge 或 ideas 需要补充
3. **打标签** — 按 tasks → knowledge → ideas 顺序为三个文件追加内容标签，跨文件去重

完成后自动运行 `archive.py` 将 `today/` 归档到 `archive/YYYY-MM/YYYY-MM-DD/`。

触发示例：「回顾一下今天」「收工了」「总结一下」

### 2.3 write-article — 知识沉淀

从 `archive/` 历史笔记中提炼选题，整合材料写成文章存入 `articles/`。

流程：确定时间范围 → 扫描存档推荐选题 → 撰写大纲 → 展开为完整文章 → 审阅定稿。文章不是简单的笔记拼接，而是跨天整合、补充背景、形成连贯叙事。

触发示例：「写篇文章」「整理一下笔记」「沉淀一下」

## 3. Vault 目录结构

使用这些技能的 Obsidian vault 需要遵循以下结构：

```
vault/
├── today/                  # 当日工作台（固定入口）
│   ├── tasks.md            #   今日任务（工作/学习/生活/回顾）
│   ├── knowledge.md        #   今日知识记录
│   └── ideas.md            #   今日灵感记录
├── archive/                # 历史归档（按月/日组织）
│   └── YYYY-MM/
│       └── YYYY-MM-DD/
│           ├── tasks.md
│           ├── knowledge.md
│           └── ideas.md
└── articles/               # 长文产出
```

## 4. 安装与使用

### 4.1 环境要求

- Python 3.10+
- [loguru](https://github.com/Delgan/loguru)

```bash
pip install loguru
```

### 4.2 作为 Agent 技能使用

将本仓库中的技能目录（`skills/daily-workflow/`、`skills/daily-review/`、`skills/write-article/`）注册到支持 SKILL.md 规范的 AI Agent（如 Cursor、Codex）中。Agent 会根据用户意图自动触发对应技能，按 SKILL.md 中定义的流程与用户交互。

### 4.3 单独运行脚本

每个技能包含的 Python 脚本也可以独立运行：

```bash
# 初始化今日工作区
python skills/daily-workflow/scripts/daily.py /path/to/vault

# 归档（回顾完成后）
python skills/daily-review/scripts/archive.py /path/to/vault

# 扫描存档（查看有哪些天已归档）
python skills/write-article/scripts/scan_archive.py /path/to/vault [--days N]
```

### 4.4 Obsidian 插件依赖

- [obsidian-linter](https://github.com/platers/obsidian-linter) — 自动维护 frontmatter 中的 `updated` 时间戳

## 5. 许可证

[GPL-3.0](LICENSE)
