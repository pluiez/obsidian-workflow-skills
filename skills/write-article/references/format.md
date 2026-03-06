# 格式规范 — 文章

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

## 文章格式

存放目录：`articles/`，文件名为文章标题。

```markdown
---
created: "YYYY-MM-DD HH:MM:SS"
updated: "YYYY-MM-DD HH:MM:SS"
tags:
  - article
  - 内容相关标签
sources:
  - archive/YYYY-MM/YYYY-MM-DD/knowledge.md
  - archive/YYYY-MM/YYYY-MM-DD/ideas.md
---

# 文章标题

## 引言

开篇概述...

## 章节标题

正文内容...

## 章节标题

正文内容...

## 总结

总结与思考...

---
Related: [[相关文章或笔记A]] · [[相关文章或笔记B]]
```

### Frontmatter 字段

- `created` / `updated` — 格式 `YYYY-MM-DD HH:MM:SS`，`updated` 由 obsidian-linter 维护
- `tags` — 至少包含 `article`，再追加内容相关标签
- `sources` — 列出作为素材的存档文件路径，便于溯源

### 正文规范

- `#` 只用于文章标题，正文从 `##` 开始
- 列表项使用 `-`
- 内部链接用 `[[]]`，外部链接用 `[text](url)`
- 底部用 `Related:` 链接到相关的文章或笔记
