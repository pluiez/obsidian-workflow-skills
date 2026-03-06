# 格式规范 — 每日笔记

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

## tasks.md

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

## knowledge.md

Frontmatter tags 包含 `daily/knowledge`，可追加内容相关标签。

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

## ideas.md

Frontmatter tags 包含 `daily/ideas`，可追加内容相关标签。

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
