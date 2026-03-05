# 示例文章

以下是一篇从存档笔记中整合而成的文章示例，展示期望的格式和深度。

```markdown
---
created: "2026-03-05 14:30:00"
updated: "2026-03-05 14:30:00"
tags:
  - article
  - TypeScript
  - HTTP
  - React
sources:
  - archive/2026-03/2026-03-03/knowledge.md
  - archive/2026-03/2026-03-04/knowledge.md
---

# 近期学到的 Web 新特性

## 引言

前端技术迭代很快，每周都能遇到一些值得记录的新特性。这篇文章整理了最近一周在日常开发中接触到的三个 Web 新特性，从类型系统到网络协议到框架行为，覆盖面不大但每个都有实际应用价值。

## TypeScript 5.4: NoInfer 工具类型

TypeScript 5.4 引入了 `NoInfer<T>` 工具类型，解决了一个长期存在的痛点：泛型函数中某个参数不应影响类型推断，但编译器会"好心"地从它推断出过于宽泛或错误的类型。

典型场景是带默认值的配置函数：

// 示例代码...

`NoInfer` 告诉编译器"不要从这个位置推断 T"，让类型推断只依赖于开发者期望的来源。

## HTTP 103 Early Hints

HTTP 103 是一种信息性状态码，允许服务器在最终响应（200）之前先发送一个提示，告诉浏览器可以提前加载关键资源。

与 `<link rel="preload">` 的区别在于时机——Early Hints 在 HTML 到达之前就能触发资源加载，减少了瀑布效应。

## React 18 Strict Mode 的副作用检测

React 18 的 Strict Mode 在开发环境下会对组件执行两次 mount/unmount 循环。这不是 bug，而是刻意为之——帮助开发者发现 useEffect 中未正确清理的副作用。

如果你的 effect 在 Strict Mode 下表现异常，说明 cleanup 函数可能有遗漏。

## 总结

这三个特性背后有一个共同趋势：工具和框架越来越倾向于在开发阶段主动暴露潜在问题，而非等到生产环境出事。TypeScript 的 NoInfer 防止类型推断失控，Early Hints 优化加载时序，React Strict Mode 提前暴露副作用问题。拥抱这些"严格"的默认行为，长期来看能省下不少调试时间。

---
Related: [[]] · [[]]
```

注意要点：
- frontmatter 中 `sources` 列出了素材来源，便于溯源
- 文章不是简单复制粘贴笔记，而是整合、补充背景、形成连贯叙事
- 每个章节有实际深度，不只是一句话概括
- 总结部分提炼了共同趋势，而非重复各节内容
