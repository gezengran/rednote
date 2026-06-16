# Excalidraw + MCP 小红书轮播 · 成品包

竖版 3:4（1080×1440）。风格：Mental Gym 同系字卡 · `#F8FAFB` 背景 / `#3D5A80` 标题 / `#1A1A1A` 正文 · Excalidraw 手绘框。

**系列定位：** Mental Gym 续 · 工具篇。科普 Excalidraw 是什么、为何不用花模板、Agent + MCP 如何省事。**不是**安装教程，**不是**开箱即用文档。

**账号理念（`core.md`）：** 怪人观察口吻；技术（MCP）当彩蛋，内容表达优先。

---

## 素材清单（已生成）

| 文件 | 用途 |
|------|------|
| `assets/178157809600-151.jpg` | **笔记分享图**（信息流封面，直接上传，不另生成） |
| `assets/excalidraw-mcp-p2.png` | 轮播内页 1 · Excalidraw 功能展示（手绘框/字/箭头） |
| `assets/excalidraw-mcp-p3.png` | 轮播内页 2 · 不需要花模板 |
| `assets/excalidraw-mcp-p4.png` | 轮播内页 3 · Agent + MCP |
| `posts/excalidraw-mcp/excalidraw/p2-what.excalidraw` | P2 源文件（Excalidraw 功能展示） |
| `posts/excalidraw-mcp/excalidraw/p3-no-template.excalidraw` | P3 源文件 |
| `posts/excalidraw-mcp/excalidraw/p4-mcp.excalidraw` | P4 源文件 |
| `posts/excalidraw-mcp/excalidraw/all-pages.excalidraw` | 三页横向排布，可一次改完 |

**发笔记顺序：** 分享图 `178157809600-151.jpg` → 轮播 `p2` → `p3` → `p4`（共 3 张内页）

**重新生成（改文案后）：**

```bash
# 首次：安装 Playwright Chromium（导出 PNG 用）
npm run playwright:install

# 生成 .excalidraw + 导出 PNG（Virgil + 小赖，与 excalidraw.com 同引擎）
python3 scripts/build_excalidraw_mcp_carousel.py
```

单页导出：

```bash
node scripts/export_excalidraw_png.mjs posts/excalidraw-mcp/excalidraw/p2-what.excalidraw assets/excalidraw-mcp-p2.png 3
```

## 发笔记 · 复制即用

### 标题

```
上篇那张封面，是用 Excalidraw 排的
```

### 正文（全文）

```
不是模板站不好，是我这种内容——截图 + 两句话 + 一张图——用 Excalidraw 反而更快。

上篇 Mental Gym 封面就是这么来的。这篇不讲安装，说说这个白板是什么、以及 Agent + MCP 怎么省事。

你更常：自己拖排版，还是让 Agent 帮你改画布？
```

### 话题标签

`#Excalidraw` `#MCP` `#AI工具` `#小红书创作` `#怪人观察` `#MentalGym`

---

## 4 页文案 + 拼版

### 封面 · 笔记分享图（直接用已发笔记截图）

**文件：** `assets/178157809600-151.jpg` — 上篇 Mental Gym **已发笔记**信息流卡片，不叠字、不另生成。读者一眼能对上「上篇那张封面」。

**不出现：** npx、配置文件、客户端名称

---

### P2 · Excalidraw 功能展示

**职责：** 用画布元素**展示**工具能力，而非文字罗列

**拼版：** 白底 + 迷你页面 mock（截图框 → 文本框 → 图框）+ 右侧标注（手绘矩形 / Virgil 字 / 椭圆箭头）+ 底部三芯片（圆角框 · 手写字 · JSON）

**核心元素（图上可见）：**
- 手绘圆角矩形框
- Virgil 手写字（标题、标注、底句）
- 箭头连线
- 椭圆高亮
- 虚线分隔

**底句：**
```
不是海报模板商城
元素是 JSON · 在自己手里
```

**导出：** 已由 `scripts/export_excalidraw_png.mjs` 走 Excalidraw `exportToBlob`（Virgil + 小赖手绘体）

---

### P3 · 怪人内容，不需要花模板

**职责：** 行为对比（C），P1 仅作例证，不讲拼版步骤

**拼版：** 字卡 + 可选小图：从 `178157809600-151.jpg` 裁建筑图条，或 `P1.png` 轮播首屏条（仅示意「截图 + 字 + 一张图」叠层）

**图上字：**
```
我以前打开模板站
找边框、找滤镜
半小时还在调样式

现在我常是：
截图 + 两句话 + 一张图

不是工具弱
是这种内容，不需要花
```

**写法约束（已定）：**
- 不点名贬损「稿定 / Canva」
- 只说「模板站 / 那一类工具」「不适合这种内容」
- 不上篇拼版教程

---

### P4 · Agent + MCP：更方便在哪

**职责：** 技术彩蛋（B + D 各半句）；全文唯一偏「工具链」的一页

**拼版：** 字卡 + **左右或上下简对比**（手绘箭头即可，不要软件截图）

**图上字：**
```
以前：打开画布，自己拖元素

现在：跟 Agent 说
它调 MCP 改画布，再导出 PNG

MCP = Agent 和 Excalidraw 之间的接线员

任何支持 MCP 的 Agent 都能接
不限某一个软件
```

**对比图（D）示意：**
```
┌─────────────┐     ┌─────────────┐
│  自己拖排版   │  →  │  说话排版    │
│  （手 + 画布） │     │ （Agent+MCP）│
└─────────────┘     └─────────────┘
```

**不出现：** prompt 全文、npx、`.cursor/mcp.json`、逐步安装

---

## MCP 与 PNG 导出

### 重要：`export_scene` 与真实 PNG

| 模式 | `export_scene` PNG | 说明 |
|------|-------------------|------|
| **Standalone**（默认，无 canvas server） | ❌ | 返回提示「需要 canvas server」 |
| **Connected**（canvas server 已启） | ⚠️ | 返回元素 JSON，**不是**位图文件 |
| **批量成品导出**（推荐） | ✅ | `scripts/export_excalidraw_png.mjs` → Excalidraw 官方渲染引擎 |

本篇 `assets/excalidraw-mcp-p*.png` 均用 **`export_excalidraw_png.mjs`** 导出（Virgil + 小赖，scale=3）。

### Connected 模式（MCP 实时画布 / SVG）

1. 复制 `.env.example` → `.env`，填入 `EXCALIDRAW_API_KEY`（`openssl rand -hex 32`）

2. 启动 canvas server：

```bash
./scripts/start_excalidraw_canvas.sh
# 浏览器打开 http://127.0.0.1:3000
```

3. `.cursor/mcp.json` 通过 `scripts/run_excalidraw_mcp.sh` 读取同一 `.env`

4. **重启 Cursor** → Settings → MCP 刷新 excalidraw

5. 对话中用 MCP 创建/修改元素；`export_scene` **format=svg** 可拿简化 SVG（无完整手绘字体）

### MCP 配置（`.cursor/mcp.json`）

密钥不进仓库，放在项目根 `.env`（见 `.env.example`）。MCP 经包装脚本启动：

```json
{
  "mcpServers": {
    "excalidraw": {
      "command": "/path/to/rednote/scripts/run_excalidraw_mcp.sh",
      "env": {
        "PATH": "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
      }
    }
  }
}
```

### 双模式工作流

| 阶段 | 做法 |
|------|------|
| 新选题 / 探索 | Agent + MCP 直接排版、试布局 |
| 成熟页型 | `build_excalidraw_mcp_carousel.py` scaffold → MCP 微调 |
| **PNG 导出** | `export_excalidraw_png.mjs`（非 MCP `export_scene` PNG） |

### 内页 Excalidraw 规格

- 画布：1080 × 1440（3:4）
- 字体：`fontFamily: 1`（Virgil + 中文自动用小赖 Xiaolai）
- 参考：`scripts/build_excalidraw_mcp_carousel.py`

---

## 自检清单（发前）

- [x] 封面直接用 `178157809600-151.jpg`，与轮播内页为不同文件
- [x] 全文无 npx / 配置文件 / 某单一 Agent 品牌软广
- [x] P2、P3 未贬损具体国内平台
- [x] P4 对比图可一眼看懂「更方便」
- [x] 新读者读首段能理解「上篇是什么」（Mental Gym 封面）
- [x] 语气符合怪人观察，非测评号、非教程号

---

## 推敲备忘（归档）

| 决策 | 结论 |
|------|------|
| MCP 路径 | 开源本地 [excalidraw-mcp-server](https://github.com/debu-sinha/excalidraw-mcp-server)；通用 MCP，不限 Cursor |
| 创作双模式 | 脚本 scaffold + MCP 微调；本篇由 `build_excalidraw_mcp_carousel.py` 生成 |
| 叙事 | C 为主（怪人工作流）、A 为辅（审美 vs 模板工具） |
| 页数 | 1 分享图 + 3 轮播内页 |
| 封面 | 直接上传 `178157809600-151.jpg`，不生成 |
| P2 | 功能展示页（手绘元素），非 bullet list |
