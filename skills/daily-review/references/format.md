# 格式规范 — 回顾与标签

## 通用规范

适用于 vault 中所有 `.md` 笔记：

- **Frontmatter** 必须包含 `created`、`updated`、`tags`
  - `created` 和 `updated` 格式：`YYYY-MM-DD HH:MM:SS`，值用双引号包裹
  - `updated` 由 obsidian-linter 插件自动维护，创建时与 `created` 相同
  - `tags` 是 YAML 列表，至少一个标签
- 每日笔记的 frontmatter 额外包含 `date`（`YYYY-MM-DD`）
- tasks.md 的 frontmatter 额外包含 `reviewed`（`true`/`false`），默认 `false`
- `#` 只用于文件标题（每个文件恰好一个），正文从 `##` 开始
- 列表项使用 `-` 而非 `*`
- 内部链接用 `[[]]`，外部链接用 `[text](url)`
- 不在 `today/` 之外链接 `today/` 中的文件

## tasks.md 格式

Frontmatter tags 包含 `daily/tasks`，可追加内容相关标签。

四个固定分区：

```markdown
## 工作
- [ ] 任务项...

## 学习
- [ ] 任务项...

## 生活
- [ ] 任务项...

## 回顾
自由文本
```

任务格式：

```markdown
- [ ] 简单任务
- [ ] 关联 issue 的任务 [ISSUE-123](https://linear.app/team/ISSUE-123)
- [ ] 需要补充上下文的任务
  > [!note]- Context
  > 背景信息、思路、注意事项等
```

- 每个任务一行 checkbox，简洁为主
- Linear issue 链接可选附加
- 上下文用 `> [!note]- Context` 可折叠 callout

## 回顾区格式

`today/tasks.md` 中 `## 回顾` 区域为自由文本，简要总结完成情况和未完成原因。

示例：

```markdown
## 回顾
完成 4/6 项。API 文档和登录页 bug 已完成，code review 已参加，快递已取。权限模块重构在等后端确认，暂未启动。Rust 所有权看了一半，明天继续。
```

## 标签体系

### 基础标签（模板自动填充）

- `daily/tasks` — tasks.md
- `daily/knowledge` — knowledge.md
- `daily/ideas` — ideas.md

### 内容标签（回顾时追加）

回顾时根据当天实际内容追加标签，追加到 frontmatter `tags` 列表中，保留基础标签。

- 使用中文，专有名词保留原文（React、TypeScript、Go 等）
- 标签应具体反映当天内容主题，避免过于宽泛

### 标签去重原则

按 tasks → knowledge → ideas 顺序打标签时：

- 后面的文件生成候选时能看到前面已确定的标签
- 语义相近的概念应复用已有标签名（如 tasks 用了"健身"，knowledge 不应生成"锻炼"，应直接用"健身"）
- 同一标签出现在多个文件中完全没问题

## knowledge.md

每个知识点用 `##` 分隔：

```markdown
## 知识点标题

**来源**: 文章链接、书名、同事讨论等

要点内容...

**相关**: [[相关笔记]]
```

- `## 标题` — 必填，简明概括
- `**来源**` — 可选但推荐
- 正文 — 自由格式
- `**相关**` — 可选，wiki-link

## ideas.md 格式

每个想法用 `##` 分隔：

```markdown
## 想法标题

**状态**: 待探索

想法描述...

**下一步**: 具体的下一步行动
```

- `## 标题` — 必填
- `**状态**` — 必填：`待探索` / `探索中` / `已落地` / `已放弃`
- 正文 — 写清楚核心想法和价值
- `**下一步**` — 可选
