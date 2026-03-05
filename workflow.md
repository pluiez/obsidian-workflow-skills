---
tags:
  - meta
---

# 工作流

## 设计理念

- **关注点分离**：tasks、knowledge、ideas 是三个独立文件，编辑时互不干扰
- **固定工作台**：`today/` 永远是当前的工作入口，打开 vault 直接使用
- **回顾驱动归档**：每天必须完成回顾（review）才能归档，确保每一天都有总结沉淀
- **两级沉淀**：日常产出先在 `today/` 中积累，归档到 `archive/` 后，定期将有价值的内容整合为完整文章，存入 `articles/`
- **自动化轮转**：脚本自动处理初始化和防重复检查，无需手动操作
- **不要在 `today/` 之外的笔记中链接 `today/` 中的文件**，因为归档后路径会变化导致链接失效

## 目录结构

```
/
├── today/                  # 当日工作台（固定入口）
│   ├── tasks.md            #   今日任务
│   ├── knowledge.md        #   今日知识记录
│   └── ideas.md            #   今日灵感记录
│
├── archive/                # 历史归档（按月/日组织）
│   └── YYYY-MM/
│       └── YYYY-MM-DD/
│           ├── tasks.md
│           ├── knowledge.md
│           └── ideas.md
│
├── articles/               # 长文产出（知识沉淀的最终形态）
│
├── _meta/                  # Vault 元信息（本文件所在目录）
└── _attachments/           # 附件
```

`today/` 中可能出现额外文件（如临时草稿、截图等），归档时会一并移入对应日期目录。

## 归档定义

归档由以下两步组成：

1. 将 `today/tasks.md` 的 frontmatter 中 `reviewed` 属性设为 `true`
2. 将整个 `today/` 目录移动到 `archive/YYYY-MM/YYYY-MM-DD/`（日期取自 frontmatter 中的 `date` 字段）

归档后 `today/` 变为空目录，下次初始化时会创建新的工作台。

## 工作流概览

### 每日流程

**早晨 — 初始化**

开始新一天时，初始化 `today/` 工作区：创建当日文件、带入昨日遗留任务、规划今天的计划。如果前一天未完成回顾，需要先补做回顾才能初始化新的工作区。

**白天 — 更新**

随时以自然语言更新工作区：完成任务时勾选、学到新知识时记录到 knowledge、有灵感时记录到 ideas。每次更新都会先预览再确认写入。

**晚上 — 回顾**

一天结束时进行回顾，包含三个阶段：

1. **回顾总结**：统计任务完成情况，生成回顾文本写入 tasks.md
2. **内容补充**：检查是否有遗漏的 knowledge 或 ideas 需要补充
3. **打标签**：按 tasks → knowledge → ideas 的顺序，为三个文件追加内容相关的标签

回顾完成后自动归档 `today/` 到 `archive/`。

### 周期性流程

**知识沉淀 — 写文章**

定期（每周或每月）从 `archive/` 中的历史笔记中提炼选题，围绕主题整合材料，写成完整文章存入 `articles/`。

流程：确定时间范围 → 选题（推荐或自定义） → 撰写大纲 → 展开为完整文章 → 审阅定稿。

## 笔记规范

### 通用规范

- **Frontmatter** 必须包含 `created`、`updated`、`tags`
  - `created` 和 `updated` 格式：`YYYY-MM-DD HH:MM:SS`
  - `updated` 由 obsidian-linter 插件自动维护
- 每日笔记的 frontmatter 额外包含 `date` 字段（`YYYY-MM-DD`）
- tasks.md 的 frontmatter 额外包含 `reviewed` 字段（`true`/`false`）
- 一级标题 `#` 只用于文件标题，正文内容从 `##` 开始
- 列表项使用 `-` 而非 `*`
- 内部链接优先使用 wiki-link `[[]]`，外部链接使用标准 markdown `[text](url)`

### 标签体系

- `daily/tasks`、`daily/knowledge`、`daily/ideas` — 每日笔记基础标签（模板自动填充），回顾时追加内容相关标签
- `article` — 文章标签
- `meta` — vault 元信息文档

### 标签去重原则

按 tasks → knowledge → ideas 的顺序依次确定标签。后面的文件生成候选时，能看到前面已确定的标签，遇到语义相近的概念优先复用已有标签名（如 tasks 用了"健身"，knowledge 就不再生成"锻炼"），但同一标签跨文件重复使用完全没问题。

---

## 附录：交互模拟

以下是一个完整的 2 天工作流交互模拟，展示用户与 AI Agent 的实际对话。

### Day 1 — 周二早上

**#1 — 早晨初始化**（触发 `daily-workflow`）

> **用户**：开始今天的工作
>
> **Agent**：`today/` 为空，开始初始化新的工作区。
>
> 运行 `daily.py`... 检查通过，今日工作区创建成功（2026-03-03）。
>
> 已从最近一天的存档（2026-03-02）中读取遗留任务：
> - [ ] 完成 API 文档更新
> - [ ] 重构用户权限模块
>
> 已写入到今日 tasks.md。需要修改遗留任务的来源范围吗？
> - A) 不保留遗留任务
> - B) 改为最近 3 天的遗留任务
> - C) 改为最近一周的遗留任务
> - D) 我来指定范围
> - E) 不修改，继续下一步

**#2 — 确认遗留 + 添加今日计划**（`daily-workflow` 继续）

> **用户**：E
>
> **Agent**：好的，保留这 2 条遗留任务。今天有什么计划？
>
> **用户**：工作上要修复登录页的 bug，Linear 上的 FE-456，还有下午3点有个 code review 会议；学习上想把 Rust 所有权那章看完；生活上取个快递
>
> **Agent**：已整理今日完整任务列表，预览如下：
>
> ```
> ## 工作
> - [ ] 完成 API 文档更新（遗留自 03-02）
> - [ ] 重构用户权限模块（遗留自 03-02）
> - [ ] 修复登录页 bug [FE-456](https://linear.app/team/FE-456)
> - [ ] 下午3点 code review 会议
>
> ## 学习
> - [ ] 看完 Rust 所有权那章
>
> ## 生活
> - [ ] 取快递
> ```
>
> 确认写入？
> - A) 没问题，写入
> - B) 我要修改

**#3 — 确认写入**（`daily-workflow` 结束）

> **用户**：A
>
> **Agent**：已写入 tasks.md，今日工作区初始化完成。

### Day 1 — 白天

**#4 — 完成任务 + 记录知识**（触发 `daily-workflow`）

> **用户**：API 文档写完了。另外修 bug 的时候发现一个知识点，React 18 的 useEffect 在 Strict Mode 下会执行两次，是为了帮助发现副作用清理问题，来源是 React 官方文档 https://react.dev/reference/react/useEffect
>
> **Agent**：已整理你的更新，预览：
>
> **tasks.md**：勾选 `完成 API 文档更新（遗留自 03-02）`
>
> **knowledge.md** 追加：
> > ## React 18 Strict Mode 下 useEffect 双重执行
> >
> > **来源**: [React 官方文档](https://react.dev/reference/react/useEffect)
> >
> > React 18 的 Strict Mode 会在开发环境下对组件执行两次 mount/unmount 循环，目的是帮助发现副作用清理不完整的问题。如果 useEffect 中有订阅、定时器等需要清理的逻辑，必须在返回的 cleanup 函数中正确处理。
> >
> > **相关**: [[]]
>
> 确认写入？
> - A) 没问题，写入
> - B) 我要修改

> **用户**：A
>
> **Agent**：已写入。

**#5 — 记录灵感**（触发 `daily-workflow`）

> **用户**：突然想到一个主意，做一个 CLI 工具自动把 Linear issue 状态同步到 tasks.md 里，这样就不用手动勾了
>
> **Agent**：已整理，预览：
>
> **ideas.md** 追加：
> > ## Linear Issue 状态自动同步到 tasks.md
> >
> > **状态**: 待探索
> >
> > 做一个 CLI 工具，监听 Linear issue 的状态变化，当 issue 标记为 Done 时自动在 tasks.md 中勾选对应的 checkbox。可以通过 Linear 的 webhook 或轮询 GraphQL API 实现，减少手动操作、避免遗漏。
> >
> > **下一步**: 调研 Linear API，对比 webhook 和 GraphQL 轮询的优劣
>
> 确认写入？
> - A) 没问题，写入
> - B) 我要修改

> **用户**：A
>
> **Agent**：已写入。

**#6 — 补充任务 Context**（触发 `daily-workflow`）

> **用户**：再加个工作任务：重构权限模块的具体方案要等后端确认新的 RBAC 设计，文档在 Notion 上
>
> **Agent**：已整理，预览：
>
> **tasks.md** `## 工作` 下追加：
> > - [ ] 确认后端 RBAC 设计方案并启动权限模块重构
> >   > [!note]- Context
> >   > 需要先跟后端确认新的 RBAC 方案，设计文档在 Notion 上
>
> 确认写入？
> - A) 没问题，写入
> - B) 我要修改

> **用户**：等一下，不是新增任务，是给遗留的那条"重构用户权限模块"补充上下文

> **Agent**：明白了，更正预览：
>
> **tasks.md** 更新 `重构用户权限模块`：
> > - [ ] 重构用户权限模块（遗留自 03-02）
> >   > [!note]- Context
> >   > 需要先跟后端确认新的 RBAC 方案，设计文档在 Notion 上
>
> 确认写入？
> - A) 没问题，写入
> - B) 我要修改

> **用户**：A
>
> **Agent**：已写入。

### Day 1 — 晚上

**#7 — 晚间回顾**（触发 `daily-review`）

> **用户**：回顾一下今天
>
> **Agent**：读取 today/tasks.md，统计完成情况：
>
> 今日任务完成情况：4/7
> - [x] 完成 API 文档更新（遗留自 03-02）
> - [ ] 重构用户权限模块（遗留自 03-02）
> - [x] 修复登录页 bug FE-456
> - [x] 下午3点 code review 会议
> - [ ] 看完 Rust 所有权那章
> - [x] 取快递
>
> 草拟回顾：
> > 完成 4/7 项。API 文档更新和登录页 bug 已完成，code review 已参加，快递已取。权限模块重构在等后端确认 RBAC 方案，暂未启动。Rust 所有权看了一半，明天继续。
>
> 这样写可以吗？
> - A) 可以，直接写入
> - B) 我来修改/补充

**#8 — 确认回顾并补充**（`daily-review` 阶段 2）

> **用户**：加一句，code review 的时候学到了 Go defer 在 panic 时也会执行
>
> **Agent**：已更新回顾：
> > 完成 4/7 项。API 文档更新和登录页 bug 已完成，code review 已参加（学到了 Go defer 在 panic 时也会执行），快递已取。权限模块重构在等后端确认 RBAC 方案，暂未启动。Rust 所有权看了一半，明天继续。
>
> 已写入 `## 回顾`。
>
> 今天的 knowledge 记录了 1 条，ideas 记录了 1 条。还有需要补充的吗？
> - A) 补充 knowledge
> - B) 补充 ideas
> - C) 都补充
> - D) 不需要了

**#9 — 补充知识**（`daily-review` 阶段 2 继续）

> **用户**：A，把 Go defer 那个正式记一下，来源是同事 code review 分享
>
> **Agent**：已整理，预览：
>
> **knowledge.md** 追加：
> > ## Go defer 在 panic 时仍会执行
> >
> > **来源**: 同事 code review 分享
> >
> > Go 中 defer 语句注册的函数在函数 panic 时依然会被执行，执行顺序是 LIFO。这个特性可以用来做资源清理的兜底——比如关闭文件句柄、释放锁等。配合 recover() 可以在 defer 中捕获 panic 并做优雅降级。
> >
> > **相关**: [[]]
>
> 确认写入？
> - A) 没问题，写入
> - B) 我要修改

> **用户**：A

> **Agent**：已写入。还有其他需要补充的吗？
> - A) 继续补充
> - B) 不需要了，继续下一步

> **用户**：B

**#10 — 打标签**（`daily-review` 阶段 3）

> **Agent**：接下来给今天的三个文件打标签。先从 **tasks.md** 开始。
>
> 今天的任务涉及前端 bug 修复、API 文档、code review、Rust 学习、权限模块设计。你有想加的标签或关键词吗？
> - A) 我来提供关键词
> - B) 你来生成候选

> **用户**：B

> **Agent**：候选标签组（追加在 `daily/tasks` 之后）：
> 1. `前端`, `code-review`, `Rust`
> 2. `React`, `code-review`, `Rust`, `RBAC`
> 3. `前端`, `code-review`, `Rust`, `权限设计`
> 4. `编程`, `code-review`
> 5. 自定义（我来输入）
>
> 选择哪一组？

> **用户**：3

> **Agent**：tasks.md 标签已更新为 `[daily/tasks, 前端, code-review, Rust, 权限设计]`。
>
> 接下来是 **knowledge.md**。今天记录了 React useEffect 双重执行和 Go defer 两个知识点。前面已确定的标签有：`前端`, `code-review`, `Rust`, `权限设计`。候选标签组：
> 1. `React`, `Go`
> 2. `React`, `Go`, `错误处理`
> 3. `React-hooks`, `Go`, `错误处理`
> 4. `前端`, `Go`
> 5. 自定义（我来输入）
>
> 选择哪一组？

> **用户**：2

> **Agent**：knowledge.md 标签已更新为 `[daily/knowledge, React, Go, 错误处理]`。
>
> 最后是 **ideas.md**。记录了 Linear 同步工具的想法。前面已确定的标签有：`前端`, `code-review`, `Rust`, `权限设计`, `React`, `Go`, `错误处理`。候选标签组：
> 1. `工具`, `自动化`
> 2. `CLI`, `Linear`
> 3. `工具`, `Linear`, `自动化`
> 4. `CLI`, `自动化`, `Linear`
> 5. 自定义（我来输入）
>
> 选择哪一组？

> **用户**：3

> **Agent**：ideas.md 标签已更新为 `[daily/ideas, 工具, Linear, 自动化]`。

**#11 — 归档**（`daily-review` 收尾）

> **Agent**：标签全部完成。现在开始归档。
>
> 已将 tasks.md 的 `reviewed` 设为 `true`，并将 `today/` 归档到 `archive/2026-03/2026-03-03/`。today/ 已清空。
>
> 今日回顾完成。

### Day 2 — 周三早上

**#12 — 新一天初始化**（触发 `daily-workflow`）

> **用户**：新的一天
>
> **Agent**：`today/` 为空，开始初始化新的工作区。
>
> 运行 `daily.py`... 检查通过，今日工作区创建成功（2026-03-04）。
>
> 已从最近一天的存档（2026-03-03）中读取遗留任务：
> - [ ] 重构用户权限模块（遗留自 03-02）
> - [ ] 看完 Rust 所有权那章
>
> 已写入到今日 tasks.md。需要修改遗留任务的来源范围吗？
> - A) 不保留遗留任务
> - B) 改为最近 3 天的遗留任务
> - C) 改为最近一周的遗留任务
> - D) 我来指定范围
> - E) 不修改，继续下一步

**#13 — 调整遗留 + 计划**（`daily-workflow` 继续）

> **用户**：E。今天工作上要写单元测试覆盖登录模块、跟产品对需求 v2.1；生活上交水电费
>
> **Agent**：已整理今日完整任务列表，预览如下：
>
> ```
> ## 工作
> - [ ] 重构用户权限模块（遗留自 03-02）
>   > [!note]- Context
>   > 需要先跟后端确认新的 RBAC 方案，设计文档在 Notion 上
> - [ ] 写单元测试覆盖登录模块
> - [ ] 跟产品对需求 v2.1
>
> ## 学习
> - [ ] 看完 Rust 所有权那章（遗留自 03-03，已看一半）
>
> ## 生活
> - [ ] 交水电费
> ```
>
> 确认写入？
> - A) 没问题，写入
> - B) 我要修改

> **用户**：A
>
> **Agent**：已写入，今日工作区初始化完成。

### Day 2 — 白天

**#14 — 记录多条知识**（触发 `daily-workflow`）

> **用户**：今天学到两个东西。第一个是 TypeScript 5.4 新增了 NoInfer 工具类型，可以防止类型参数被意外推断，来源是 TS 5.4 release note。第二个是 HTTP 103 Early Hints 可以让浏览器提前加载资源，来源是 web.dev 文章 https://web.dev/early-hints
>
> **Agent**：已整理，预览：
>
> **knowledge.md** 追加两条：
> > ## TypeScript 5.4 NoInfer 工具类型
> >
> > **来源**: [TypeScript 5.4 Release Note](https://devblogs.microsoft.com/typescript/announcing-typescript-5-4/)
> >
> > TypeScript 5.4 新增了 `NoInfer<T>` 工具类型，用于阻止编译器从特定位置推断类型参数。在泛型函数中，当某个参数不应影响类型推断结果时，用 `NoInfer` 包裹它可以避免意外的类型收窄。
> >
> > **相关**: [[]]
>
> > ## HTTP 103 Early Hints
> >
> > **来源**: [web.dev](https://web.dev/early-hints)
> >
> > HTTP 103 Early Hints 是一种信息性状态码，允许服务器在最终响应之前先发送一个提示响应，告诉浏览器可以提前加载关键资源（如 CSS、字体）。这减少了资源加载的瀑布效应，改善了页面加载性能。
> >
> > **相关**: [[]]
>
> 确认写入？
> - A) 没问题，写入
> - B) 我要修改

> **用户**：A
>
> **Agent**：已写入。

**#15 — 勾选任务**（触发 `daily-workflow`）

> **用户**：单元测试写完了，需求也对完了
>
> **Agent**：已整理，预览：
>
> **tasks.md** 勾选：
> - [x] 写单元测试覆盖登录模块
> - [x] 跟产品对需求 v2.1
>
> 确认写入？
> - A) 没问题，写入
> - B) 我要修改

> **用户**：A
>
> **Agent**：已写入。

### Day 2 — 晚上

**#16 — 晚间回顾**（触发 `daily-review`）

> **用户**：收工了，总结一下
>
> **Agent**：今日任务完成情况：3/5
> - [ ] 重构用户权限模块（遗留自 03-02）
> - [x] 写单元测试覆盖登录模块
> - [x] 跟产品对需求 v2.1
> - [ ] 看完 Rust 所有权那章（遗留自 03-03）
> - [x] 交水电费
>
> 草拟回顾：
> > 完成 3/5 项。登录模块单元测试和需求 v2.1 对接已完成，水电费已交。权限模块仍在等后端 RBAC 方案确认。Rust 所有权那章还没抽出时间看。
>
> 这样写可以吗？
> - A) 可以，直接写入
> - B) 我来修改/补充

> **用户**：A

> **Agent**：已写入。今天的 knowledge 记录了 2 条，ideas 记录了 0 条。还有需要补充的吗？
> - A) 补充 knowledge
> - B) 补充 ideas
> - C) 都补充
> - D) 不需要了

> **用户**：D

**#17 — 打标签 + 归档**（`daily-review` 阶段 3 + 收尾）

> **Agent**：接下来打标签。先从 **tasks.md** 开始。候选标签组：
> 1. `测试`, `需求`, `Rust`
> 2. `前端`, `测试`, `Rust`, `权限设计`
> 3. `单元测试`, `产品`, `Rust`
> 4. `前端`, `测试`, `产品对接`
> 5. 自定义（我来输入）
>
> 选择哪一组？

> **用户**：2

> **Agent**：tasks.md 标签已更新。接下来是 **knowledge.md**。前面已确定：`前端`, `测试`, `Rust`, `权限设计`。候选标签组：
> 1. `TypeScript`, `HTTP`
> 2. `TypeScript`, `性能优化`
> 3. `TypeScript`, `HTTP`, `性能优化`
> 4. `类型系统`, `HTTP`
> 5. 自定义（我来输入）
>
> 选择哪一组？

> **用户**：1

> **Agent**：knowledge.md 标签已更新。ideas.md 今天没有新内容，跳过打标签。
>
> 标签全部完成。现在开始归档。
>
> 已将 tasks.md 的 `reviewed` 设为 `true`，并将 `today/` 归档到 `archive/2026-03/2026-03-04/`。today/ 已清空。
>
> 今日回顾完成。

### 周末 — 知识沉淀

**#18 — 启动知识沉淀**（触发 `write-article`）

> **用户**：帮我整理一下这周的笔记，写篇文章
>
> **Agent**：我先查看一下存档情况...
>
> 扫描 `archive/` 目录，最近 30 日内有 8 天存档（2026-02-24 至 2026-03-04）。要整理哪段时间的笔记？
> - A) 最近一周（03-02 ~ 03-04，3 天有存档）
> - B) 最近两周（02-24 ~ 03-04，8 天有存档）
> - C) 最近一个月
> - D) 我来指定范围

> **用户**：A

**#19 — 推荐选题**（`write-article` 继续）

> **Agent**：已扫描 03-02 至 03-04 的存档（knowledge + ideas），以下是推荐选题：
>
> 1. **前端开发中的隐蔽陷阱：React Strict Mode 与 Hydration 问题** — 本周记录了 React useEffect 双重执行等多个前端调试经验
> 2. **Go 语言错误处理的设计哲学：defer、panic 与 recover** — 从 defer 在 panic 时的行为展开，探讨 Go 的错误处理范式
> 3. **2024-2025 Web 新特性速览：TypeScript NoInfer、HTTP 103 Early Hints** — 整合本周学到的新 Web 技术
> 4. **从日常工具到效率提升：自动化工作流的想法与实践** — 围绕 Linear 同步工具等自动化灵感展开
>
> 选择一个选题？（也可以自定义）

> **用户**：3，不过标题改成"近期学到的 Web 新特性"

**#20 — 大纲确认**（`write-article` 继续）

> **Agent**：好的。已扫描相关存档材料，撰写大纲如下：
>
> ---
> **近期学到的 Web 新特性**
>
> **可用参考来源**：
> - `archive/2026-03/2026-03-03/knowledge.md` — React 18 Strict Mode useEffect 双重执行
> - `archive/2026-03/2026-03-04/knowledge.md` — TypeScript 5.4 NoInfer、HTTP 103 Early Hints
>
> **大纲**：
> 1. **引言** — 为什么要关注 Web 新特性，保持技术敏感度的价值
> 2. **TypeScript 5.4: NoInfer 工具类型** — 解决了什么问题、实际使用场景、与现有类型工具的对比
> 3. **HTTP 103 Early Hints** — 工作原理、性能收益、浏览器支持情况、与 preload/preconnect 的关系
> 4. **React 18 Strict Mode 的副作用检测** — 双重执行机制、为什么这样设计、开发者需要注意什么
> 5. **总结** — 这些新特性背后的共同趋势（开发体验与性能的平衡）
> ---
>
> 大纲可以吗？
> - A) 没问题，开始写
> - B) 我要调整

> **用户**：A

**#21 — 文章完成**（`write-article` 继续）

> **Agent**：文章已写完，保存至 `articles/近期学到的 Web 新特性.md`。
>
> 请审阅文章内容，有任何需要修改的地方吗？
> - A) 没问题，完成
> - B) 有修改意见

> **用户**：第三节 React 那里再加一点关于 cleanup 函数最佳实践的内容

> **Agent**：已补充 cleanup 函数最佳实践段落，更新完成。还有其他需要修改的吗？
> - A) 没问题，完成
> - B) 还有修改

> **用户**：A

> **Agent**：文章已定稿。知识沉淀完成。
