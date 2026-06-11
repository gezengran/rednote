# Mental Gym 小红书轮播 · 成品包

竖版 3:4（建议 1080×1440）。风格：V1 冷色未来诊所 · 写实摄影感。

## 素材清单

| 文件 | 用途 |
|------|------|
| `assets/mental-gym-p1-cover-exterior.png` | P1 底图（可选，见下方拼版） |
| `sources/2026-06-11 16.01.49.png` | P1 Reddit 截图 |
| `assets/mental-gym-p2-concept-v1-realistic.png` | P2 场内三器械全景 |
| `assets/mental-gym-p3-reading-treadmill.png` | P3 阅读跑步机特写 |
| `assets/mental-gym-p3b-distraction-booth.png` | 备用（可替换 P3 或作封面备选） |

P4–P6 在稿定/Canva 做纯字卡，文案见下。

---

## 6 页文案 + 拼版

### P1 · 封面 + 钩子

**拼版：** 上半 Reddit 截图，下半白底 + 大字（或整页截图铺满，底部渐变遮罩压字）

**图上字（15–30 字）：**
```
有人预言：
15 年后会有「心理健身房」
我当真了。
```

**正文首段（发笔记时用）：**
```
看到一条评论说，15 年后可能会出现 mental gyms——专门练阅读耐力的那种。

我第一反应：太科幻了。
想了想：好像我们已经需要了。
```

---

### P2 · 三个训练器

**底图：** `mental-gym-p2-concept-v1-realistic.png`

**图上字：**
```
没有跑步机，没有哑铃
只有注意力训练器

① 阅读跑步机 — 分心就暂停
② 抗干扰舱 — 通知弹但不能点
③ 深度思考台 — 20 分钟不许问 AI
```

---

### P3 · 用进废退

**底图：** `mental-gym-p3-reading-treadmill.png`

**图上字：**
```
持续注意力是一条神经通路
用进废退

我们现在的生活
几乎在系统性「不练」它
```

---

### P4 · 现实对照（T1 纯字卡）

**稿定拼版：** 白底 #F8FAFB，标题 + 两列表格，字体建议思源黑体/苹方

**标题：**
```
现在 → 未来
```

**表格：**

| 现在 | 未来 |
|------|------|
| 刷短视频 | 注意力训练 |
| AI 帮总结 | 自己读完 |
| 快速切换 | 持续专注 |

---

### P5 · D3 怪比喻（M3 肌肉失忆）

**稿定拼版：** 同 P4 色板，居中大字，留白多

**图上字：**
```
注意力像久不练的腿
刚走两步，就想坐
```

---

### P6 · 结尾升华

**图上字：**
```
如果真有 mental gym
练的不是智力
是不被打断的能力
```

---

## 笔记标题（选一）

1. `15 年后可能会有「心理健身房」`
2. `如果肌肉能练，注意力为什么不能？`
3. `未来真有一种地方，叫 Mental Gym`

## 话题标签

`#注意力` `#专注力` `#心理健身房` `#阅读耐力` `#怪人观察` `#未来设想`

## Excalidraw 拼版（推荐）

已生成 6 页 + 1 个合集文件，路径：`posts/mental-gym/excalidraw/`

| 文件 | 内容 |
|------|------|
| `p1-cover.excalidraw` | Reddit 截图 + 钩子字 + 外立面 |
| `p2-trainers.excalidraw` | 场内全景 + 三训练器文案 |
| `p3-neuro.excalidraw` | 阅读跑步机 + 用进废退 |
| `p4-compare.excalidraw` | 现在 vs 未来字卡 |
| `p5-metaphor.excalidraw` | 肌肉失忆比喻 |
| `p6-closing.excalidraw` | 结尾升华 |
| `all-pages.excalidraw` | 六页横向排布，可一次改完 |

**打开方式：**

1. 打开 [excalidraw.com](https://excalidraw.com)
2. 菜单 → **Open** → 选择本地 `.excalidraw` 文件
3. 微调手绘边框、字号后 → **Export image** → PNG（建议 3x 导出）

**重新生成（改文案后）：**

```bash
python3 scripts/build_excalidraw_carousel.py
```

## MCP 说明

项目已配置 `.cursor/mcp.json`（[excalidraw-mcp-server](https://github.com/debu-sinha/excalidraw-mcp-server)）。

启用步骤：

1. 需已安装 Node.js（`brew install node`）；MCP 使用绝对路径 `/opt/homebrew/bin/npx`
2. **重启 Cursor** 或 Settings → MCP → 刷新 excalidraw
3. 新对话中说「用 Excalidraw 画 P4 对比表」即可调用 MCP 工具

**常见日志说明：**

| 日志 | 是否致命 | 含义 |
|------|----------|------|
| `spawn npx ENOENT` | 是 | 未安装 Node，或路径不对 |
| `npm warn deprecated uuid@9.0.1` | **否** | npm 弃用警告，Cursor 标成 error 可忽略 |
| 连接卡 ~30 秒后失败 | 是 | `npx -y` 首次下载包太慢，已改为直接调用二进制 |
| `Canvas server not reachable, standalone mode` | **否** | 无浏览器同步，MCP 绘图仍可用 |

`mcp.json` 应使用：`"command": "/opt/homebrew/bin/excalidraw-mcp-server"`（已全局安装，秒启）。

## 稿定操作提示（备选）

1. 新建画布 1080×1440（3:4）
2. P1：导入 Reddit 截图 + 钩子字，或外立面图 + 顶部小字「灵感来自一条评论」
3. P2–P3：导入对应 PNG，底部加半透明白条压字
4. P4–P6：空白画布 + 字，色值参考 `#F8FAFB` 背景、`#3D5A80` 标题、`#1A1A1A` 正文
