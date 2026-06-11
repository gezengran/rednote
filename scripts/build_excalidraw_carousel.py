#!/usr/bin/env python3
"""Generate Excalidraw files for Mental Gym Xiaohongshu carousel (3:4)."""

from __future__ import annotations

import base64
import json
import random
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "posts" / "mental-gym" / "excalidraw"
ASSETS = ROOT / "assets"
SOURCES = ROOT / "sources"

CANVAS_W = 1080
CANVAS_H = 1440

# V1 冷色未来诊所 · Excalidraw 手写体 + 圆润艺术描边
BG = "#f8fafb"
TITLE = "#3d5a80"
BODY = "#1a1a1a"
STROKE = "#3d5a80"
FONT_HAND = 1  # Virgil 手写体


def _id() -> str:
    return uuid.uuid4().hex[:16]


def _seed() -> int:
    return random.randint(1, 2**31 - 1)


def _now() -> int:
    return int(time.time() * 1000)


def _file_entry(path: Path) -> tuple[str, dict]:
    file_id = _id()
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    ts = _now()
    return file_id, {
        "mimeType": mime,
        "id": file_id,
        "dataURL": f"data:{mime};base64,{data}",
        "created": ts,
        "lastRetrieved": ts,
    }


def _base_fields(el_type: str, x: float, y: float, w: float, h: float) -> dict:
    return {
        "id": _id(),
        "type": el_type,
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "angle": 0,
        "strokeColor": "#1e1e1e",
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "seed": _seed(),
        "version": 1,
        "versionNonce": _seed(),
        "isDeleted": False,
        "boundElements": None,
        "updated": _now(),
        "link": None,
        "locked": False,
    }


def rect(
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    bg: str = "#ffffff",
    stroke: str = STROKE,
    roughness: int = 1,
) -> dict:
    el = _base_fields("rectangle", x, y, w, h)
    el["backgroundColor"] = bg
    el["strokeColor"] = stroke
    el["roughness"] = roughness
    el["roundness"] = {"type": 3}
    return el


def text_el(
    content: str,
    x: float,
    y: float,
    w: float,
    *,
    size: int = 36,
    align: str = "left",
    family: int = FONT_HAND,
    color: str = BODY,
) -> dict:
    lines = content.split("\n")
    line_h = int(size * 1.35)
    h = max(line_h * len(lines), size + 8)
    el = _base_fields("text", x, y, w, h)
    el["strokeColor"] = color
    el["backgroundColor"] = "transparent"
    el["text"] = content
    el["originalText"] = content
    el["fontSize"] = size
    el["fontFamily"] = family
    el["textAlign"] = align
    el["verticalAlign"] = "top"
    el["baseline"] = size - 2
    el["containerId"] = None
    el["lineHeight"] = 1.25
    el["roughness"] = 0
    return el


def image_el(
    file_id: str,
    x: float,
    y: float,
    w: float,
    h: float,
) -> dict:
    el = _base_fields("image", x, y, w, h)
    el["strokeColor"] = "transparent"
    el["roughness"] = 0
    el["status"] = "saved"
    el["fileId"] = file_id
    el["scale"] = [1, 1]
    return el


def frame_el(name: str, x: float, y: float, w: float, h: float) -> dict:
    el = _base_fields("frame", x, y, w, h)
    el["name"] = name
    el["strokeColor"] = "#bbb"
    el["backgroundColor"] = "transparent"
    el["strokeWidth"] = 2
    el["roughness"] = 0
    return el


def save(name: str, elements: list[dict], files: dict[str, dict]) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {
            "gridSize": None,
            "viewBackgroundColor": BG,
            "zoom": {"value": 0.6},
            "scrollX": 0,
            "scrollY": 0,
        },
        "files": files,
    }
    path = OUT_DIR / f"{name}.excalidraw"
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


REDDIT_QUOTE = (
    "Reading Endurance.\n"
    "There will be 'mental gyms' for this in 15 years."
)


def build_p1(files: dict) -> list[dict]:
    pad = 60
    inner = CANVAS_W - pad * 2
    els: list[dict] = [frame_el("P1 封面+钩子", 0, 0, CANVAS_W, CANVAS_H)]
    els.append(rect(0, 0, CANVAS_W, CANVAS_H, bg=BG, stroke="transparent", roughness=0))

    quote_y = 72
    quote_h = 248
    els.append(rect(pad, quote_y, inner, quote_h))
    els.append(
        text_el(
            "来自 Reddit",
            pad + 32,
            quote_y + 24,
            inner - 64,
            size=22,
            color=TITLE,
        )
    )
    els.append(
        text_el(
            REDDIT_QUOTE,
            pad + 32,
            quote_y + 68,
            inner - 64,
            size=30,
        )
    )

    # 中文区与 Reddit 区同结构：标签左对齐 + 正文左对齐；CJK 同字号视觉更大，正文 32 而非 38
    text_x = pad + 32
    text_w = inner - 64
    hook_y = quote_y + quote_h + 36
    hook_h = 200
    els.append(rect(pad, hook_y, inner, hook_h))
    els.append(
        text_el(
            "有人预言：",
            text_x,
            hook_y + 24,
            text_w,
            size=22,
            color=TITLE,
        )
    )
    els.append(
        text_el(
            "15 年后会有「心理健身房」\n我当真了。",
            text_x,
            hook_y + 64,
            text_w,
            size=32,
        )
    )

    ext_id, ext_file = _file_entry(ASSETS / "mental-gym-p1-cover-exterior.png")
    files[ext_id] = ext_file
    img_y = hook_y + hook_h + 36
    img_h = CANVAS_H - img_y - pad
    els.append(image_el(ext_id, pad, img_y, inner, img_h))
    return els


def build_p2(files: dict) -> list[dict]:
    pad = 40
    els: list[dict] = [frame_el("P2 三个训练器", 0, 0, CANVAS_W, CANVAS_H)]

    bg_id, bg_file = _file_entry(ASSETS / "mental-gym-p2-concept-v1-realistic.png")
    files[bg_id] = bg_file
    els.append(image_el(bg_id, 0, 0, CANVAS_W, int(CANVAS_H * 0.62)))

    bar_y = int(CANVAS_H * 0.58)
    els.append(rect(0, bar_y, CANVAS_W, CANVAS_H - bar_y, bg="#ffffffee", stroke="transparent", roughness=0))
    els.append(
        text_el(
            "没有跑步机，没有哑铃\n只有注意力训练器\n\n"
            "① 阅读跑步机 — 分心就暂停\n"
            "② 抗干扰舱 — 通知弹但不能点\n"
            "③ 深度思考台 — 20 分钟不许问 AI",
            pad,
            bar_y + 30,
            CANVAS_W - pad * 2,
            size=32,
        )
    )
    return els


def build_p3(files: dict) -> list[dict]:
    pad = 40
    els: list[dict] = [frame_el("P3 用进废退", 0, 0, CANVAS_W, CANVAS_H)]

    bg_id, bg_file = _file_entry(ASSETS / "mental-gym-p3-reading-treadmill.png")
    files[bg_id] = bg_file
    els.append(image_el(bg_id, 0, 0, CANVAS_W, int(CANVAS_H * 0.65)))

    bar_y = int(CANVAS_H * 0.6)
    els.append(rect(0, bar_y, CANVAS_W, CANVAS_H - bar_y, bg=BG, stroke="transparent", roughness=0))
    els.append(
        text_el(
            "持续注意力是一条神经通路\n用进废退\n\n我们现在的生活\n几乎在系统性「不练」它",
            pad,
            bar_y + 40,
            CANVAS_W - pad * 2,
            size=36,
            color=TITLE,
        )
    )
    return els


def build_text_card(name: str, lines: list[str], *, title: str | None = None) -> list[dict]:
    pad = 80
    els: list[dict] = [frame_el(name, 0, 0, CANVAS_W, CANVAS_H)]
    els.append(rect(0, 0, CANVAS_W, CANVAS_H, bg=BG, stroke="transparent", roughness=0))

    y = 200
    if title:
        els.append(text_el(title, pad, y, CANVAS_W - pad * 2, size=48, align="center", color=TITLE))
        y += 120

    if title and not lines:
        col_w = (CANVAS_W - pad * 2 - 40) // 2
        left_x = pad
        right_x = pad + col_w + 40
        row_h = 100
        start_y = y + 40

        els.append(text_el("现在", left_x, start_y - 60, col_w, size=36, align="center", color=TITLE))
        els.append(text_el("未来", right_x, start_y - 60, col_w, size=36, align="center", color=TITLE))

        pairs = [("刷短视频", "注意力训练"), ("AI 帮总结", "自己读完"), ("快速切换", "持续专注")]
        for i, (left, right) in enumerate(pairs):
            ry = start_y + i * row_h
            els.append(rect(left_x, ry, col_w, row_h - 20, bg="#ffffff", roughness=1))
            els.append(rect(right_x, ry, col_w, row_h - 20, bg="#ffffff", roughness=1))
            els.append(text_el(left, left_x + 20, ry + 24, col_w - 40, size=32, align="center"))
            els.append(text_el(right, right_x + 20, ry + 24, col_w - 40, size=32, align="center"))
    elif lines:
        body = "\n".join(lines)
        els.append(
            text_el(
                body,
                pad,
                (CANVAS_H - len(lines) * 60) // 2,
                CANVAS_W - pad * 2,
                size=42,
                align="center",
            )
        )

    return els


def main() -> None:
    pages = [
        ("p1-cover", build_p1, True),
        ("p2-trainers", build_p2, True),
        ("p3-neuro", build_p3, True),
        ("p4-compare", lambda f: build_text_card("P4 现实对照", [], title="现在 → 未来"), False),
        (
            "p5-metaphor",
            lambda f: build_text_card(
                "P5 肌肉失忆",
                ["注意力像久不练的腿", "刚走两步，就想坐"],
            ),
            False,
        ),
        (
            "p6-closing",
            lambda f: build_text_card(
                "P6 结尾",
                ["如果真有 mental gym", "练的不是智力", "是不被打断的能力"],
            ),
            False,
        ),
    ]

    paths: list[Path] = []
    for slug, builder, uses_files in pages:
        files: dict[str, dict] = {}
        elements = builder(files)
        paths.append(save(slug, elements, files))

    # Combined file: all frames in one canvas for batch editing
    all_files: dict[str, dict] = {}
    all_elements: list[dict] = []
    gap = 120
    for i, (slug, builder, _) in enumerate(pages):
        ox = i * (CANVAS_W + gap)
        els = builder(all_files)
        for el in els:
            if el["type"] != "frame":
                el = {**el, "x": el["x"] + ox}
            else:
                el = {**el, "x": ox, "name": f"{el.get('name', slug)}"}
            all_elements.append(el)
    paths.append(save("all-pages", all_elements, all_files))

    print("Generated:")
    for p in paths:
        print(f"  {p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
