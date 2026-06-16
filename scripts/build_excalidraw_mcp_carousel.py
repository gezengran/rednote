#!/usr/bin/env python3
"""Generate Excalidraw files and PNG exports for Excalidraw+MCP carousel (3:4)."""

from __future__ import annotations

import base64
import json
import random
import struct
import time
import uuid
from pathlib import Path

import os
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "posts" / "excalidraw-mcp" / "excalidraw"
ASSETS = ROOT / "assets"

CANVAS_W = 1080
CANVAS_H = 1440

BG = "#f8fafb"
TITLE = "#3d5a80"
BODY = "#1a1a1a"
STROKE = "#3d5a80"
FONT_VIRGIL = 1  # Latin hand-drawn (Excalidraw title)
FONT_XIAOLAI = 5  # Xiaolai 小赖 — hand-drawn CJK (see 样本.excalidraw)
FONT_EXCALIFONT = 6  # mixed CJK + Latin footer

MENTAL_GYM_FEED = ASSETS / "178157809600-151.jpg"
P3_TEMPLATE_IMG = ASSETS / "2026-06-16 13.40.47.png"
P3_SIMPLE_IMG = ASSETS / "2026-06-16 13.48.24.png"


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
    opacity: int = 100,
) -> dict:
    el = _base_fields("rectangle", x, y, w, h)
    el["backgroundColor"] = bg
    el["strokeColor"] = stroke
    el["roughness"] = roughness
    el["opacity"] = opacity
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
    valign: str = "top",
    family: int = FONT_XIAOLAI,
    color: str = BODY,
    container_id: str | None = None,
) -> dict:
    lines = content.split("\n")
    line_h = int(size * 1.35)
    h = max(line_h * len(lines), size + 8)
    el = _base_fields("text", x, y, w, h)
    el["strokeColor"] = color
    el["text"] = content
    el["originalText"] = content
    el["fontSize"] = size
    el["fontFamily"] = family
    el["textAlign"] = align
    el["verticalAlign"] = valign
    el["baseline"] = size - 2
    el["containerId"] = container_id
    el["lineHeight"] = 1.25
    el["roughness"] = 0
    el["autoResize"] = container_id is not None
    return el


def rect_with_text(
    x: float,
    y: float,
    w: float,
    h: float,
    content: str,
    *,
    bg: str = "#ffffff",
    stroke: str = STROKE,
    roughness: int = 1,
    size: int = 36,
    align: str = "left",
    valign: str = "middle",
    family: int = FONT_XIAOLAI,
    color: str = BODY,
    padding: int = 20,
    opacity: int = 100,
) -> list[dict]:
    """Rectangle + unbound text overlay.

    Do not bind text to the rectangle (containerId). Bound labels export CJK in a
    system font instead of Excalidraw's hand-drawn Xiaolai fallback.
    """
    lines = content.split("\n")
    line_h = int(size * 1.35)
    text_h = max(line_h * len(lines), size + 8)
    text_w = w - padding * 2

    if valign == "middle":
        text_y = y + (h - text_h) / 2
    else:
        text_y = y + padding

    text_x = x + padding

    rect_el = _base_fields("rectangle", x, y, w, h)
    rect_el["backgroundColor"] = bg
    rect_el["strokeColor"] = stroke
    rect_el["roughness"] = roughness
    rect_el["opacity"] = opacity
    rect_el["roundness"] = {"type": 3}

    text_elem = text_el(
        content,
        text_x,
        text_y,
        text_w,
        size=size,
        align=align,
        valign="top",
        family=family,
        color=color,
        container_id=None,
    )
    text_elem["autoResize"] = False
    return [rect_el, text_elem]


def ellipse(
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    bg: str = "transparent",
    stroke: str = STROKE,
    roughness: int = 1,
    stroke_width: int = 2,
    stroke_style: str = "solid",
) -> dict:
    el = _base_fields("ellipse", x, y, w, h)
    el["backgroundColor"] = bg
    el["strokeColor"] = stroke
    el["roughness"] = roughness
    el["strokeWidth"] = stroke_width
    el["strokeStyle"] = stroke_style
    return el


def diamond(
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    bg: str = "#fff3bf",
    stroke: str = STROKE,
    roughness: int = 1,
    opacity: int = 100,
) -> dict:
    el = _base_fields("diamond", x, y, w, h)
    el["backgroundColor"] = bg
    el["strokeColor"] = stroke
    el["roughness"] = roughness
    el["opacity"] = opacity
    return el


def labeled_node(
    shape: str,
    x: float,
    y: float,
    w: float,
    h: float,
    label: str,
    *,
    bg: str = "#ffffff",
    stroke: str = STROKE,
    roughness: int = 1,
    size: int = 22,
    family: int = FONT_XIAOLAI,
    color: str = BODY,
) -> list[dict]:
    makers = {"rect": rect, "ellipse": ellipse, "diamond": diamond}
    els: list[dict] = [makers[shape](x, y, w, h, bg=bg, stroke=stroke, roughness=roughness)]
    lines = label.split("\n")
    line_h = int(size * 1.35)
    text_h = max(line_h * len(lines), size + 4)
    text_w = w - 12
    els.append(
        text_el(
            label,
            x + (w - text_w) / 2,
            y + (h - text_h) / 2,
            text_w,
            size=size,
            align="center",
            family=family,
            color=color,
        )
    )
    return els


def arrow_down(x: float, y: float, length: float) -> dict:
    return arrow_el(x, y, 0, length)


def arrow_right(x: float, y: float, length: float) -> dict:
    return arrow_el(x, y, length, 0)


def line_el(x: float, y: float, w: float, h: float, *, stroke: str = STROKE, roughness: int = 1) -> dict:
    el = _base_fields("line", x, y, w, h)
    el["strokeColor"] = stroke
    el["roughness"] = roughness
    el["points"] = [[0, 0], [w, h]]
    el["lastCommittedPoint"] = None
    return el


def image_size(path: Path) -> tuple[int, int]:
    """Read pixel width/height without extra deps (PNG + JPEG)."""
    data = path.read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", data[16:24])
        return int(w), int(h)
    if data[:2] == b"\xff\xd8":
        i = 2
        while i < len(data) - 8:
            if data[i] != 0xFF:
                break
            marker = data[i + 1]
            i += 2
            if marker in {0xD8, 0xD9}:
                continue
            seg_len = struct.unpack(">H", data[i : i + 2])[0]
            if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
                h, w = struct.unpack(">HH", data[i + 3 : i + 7])
                return int(w), int(h)
            i += seg_len
    raise ValueError(f"unsupported image: {path}")


def fit_contain(src_w: int, src_h: int, max_w: float, max_h: float) -> tuple[float, float]:
    scale = min(max_w / src_w, max_h / src_h)
    return src_w * scale, src_h * scale


def fit_stack_full_width(
    sources: list[tuple[int, int]],
    total_w: float,
    max_h: float,
    gap: float,
) -> tuple[float, list[tuple[float, float]]]:
    """Stack images vertically at full width, uniform scale, keep aspect ratio."""
    heights = [total_w * h / w for w, h in sources]
    total = sum(heights) + gap * max(0, len(sources) - 1)
    scale = 1.0 if total <= max_h else max_h / total
    sizes = [(total_w * scale, ht * scale) for ht in heights]
    block_h = sum(s[1] for s in sizes) + gap * max(0, len(sources) - 1)
    return block_h, sizes


def image_crop_rect(
    nat_w: int,
    nat_h: int,
    x: int,
    y: int,
    width: int,
    height: int,
) -> dict:
    return {
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "naturalWidth": nat_w,
        "naturalHeight": nat_h,
    }


def image_crop_template_p3(nat_w: int, nat_h: int) -> dict:
    """前期筹备 + 隐蔽工程 only; exclude title banner and 基础硬装 watermark."""
    # Tuned on 988×1310 source; scale proportionally for other sizes.
    y = round(nat_h * 365 / 1310)
    crop_h = round(nat_h * 466 / 1310)
    return image_crop_rect(nat_w, nat_h, 0, y, nat_w, crop_h)


def text_block_height(content: str, size: int, padding: int) -> float:
    lines = content.split("\n")
    line_h = int(size * 1.35)
    return max(line_h * len(lines), size + 8) + padding * 2


def image_el(
    file_id: str,
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    crop: dict | None = None,
) -> dict:
    el = _base_fields("image", x, y, w, h)
    el["strokeColor"] = "transparent"
    el["roughness"] = 0
    el["status"] = "saved"
    el["fileId"] = file_id
    el["scale"] = [1, 1]
    el["crop"] = crop
    return el


def arrow_el(x: float, y: float, w: float, h: float = 0) -> dict:
    el = _base_fields("arrow", x, y, w, h)
    el["strokeColor"] = STROKE
    el["roughness"] = 1
    el["points"] = [[0, 0], [w, h]]
    el["lastCommittedPoint"] = None
    el["startBinding"] = None
    el["endBinding"] = None
    el["startArrowhead"] = None
    el["endArrowhead"] = "arrow"
    return el


def frame_el(name: str, x: float, y: float, w: float, h: float) -> dict:
    el = _base_fields("frame", x, y, w, h)
    el["name"] = name
    el["strokeColor"] = "#bbb"
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


def build_p2(files: dict) -> list[dict]:
    """Visual showcase of Excalidraw primitives — layout aligned with P4."""
    pad = 36
    inner = CANVAS_W - pad * 2
    els: list[dict] = [frame_el("P2 Excalidraw 功能展示", 0, 0, CANVAS_W, CANVAS_H)]
    els.append(rect(0, 0, CANVAS_W, CANVAS_H, bg=BG, stroke="transparent", roughness=0))

    footer_text_h = 28
    footer_y = CANVAS_H - pad - footer_text_h
    footer_dash_y = footer_y - 14

    gap_title_main = 16
    gap_main_chips = 20
    gap_chips_footer = 18
    chips_h = 96

    title_y = 32
    els.append(text_el("Excalidraw", pad, title_y, 420, size=52, color=TITLE, family=FONT_VIRGIL))
    els.append(text_el("开源手绘白板", pad, title_y + 56, 420, size=28, color=BODY, family=FONT_VIRGIL))

    main_top = title_y + 96 + gap_title_main
    chips_y = footer_dash_y - gap_chips_footer - chips_h
    main_frame_h = chips_y - gap_main_chips - main_top
    main_x = pad
    main_w = inner

    els.append(rect(main_x, main_top, main_w, main_frame_h, bg="#ffffff", stroke=STROKE, roughness=2))
    els.append(
        text_el(
            "截图 + 两句话 + 一张图，搭一张笔记",
            main_x + 16,
            main_top + 10,
            main_w - 32,
            size=19,
            align="center",
            color=TITLE,
        )
    )

    step_col_x = main_x + 14
    mock_x = main_x + 88
    callout_x = main_x + main_w - 148
    mock_w = callout_x - mock_x - 20

    content_top = main_top + 42
    content_h = main_frame_h - 52
    els.append(text_el("步骤", step_col_x, main_top + 36, 36, size=15, color=TITLE))
    arrow_gap = 14
    arrow_len = 24
    box1_h = content_h * 0.22
    box2_h = content_h * 0.14
    box3_h = content_h - box1_h - box2_h - arrow_len * 2 - arrow_gap * 2

    step_nums = ["①", "②", "③"]
    boxes = [
        ("截图", "#d0ebff", 32),
        ("两句话", "#fff3bf", 34),
        ("一张图", "#ffd8a8", 30),
    ]
    callouts = ["手绘\n矩形框", "小赖\n手写字", "椭圆 ·\n箭头"]

    y = content_top
    for i, ((label, bg, size), callout, num) in enumerate(zip(boxes, callouts, step_nums)):
        if i == 0:
            bh = box1_h
        elif i == 1:
            bh = box2_h
        else:
            bh = box3_h
        cy = y + bh / 2

        els.append(
            text_el(
                num,
                step_col_x,
                cy - 12,
                32,
                size=20,
                align="center",
                color=TITLE,
                family=FONT_VIRGIL,
            )
        )
        els.extend(
            rect_with_text(
                mock_x,
                y,
                mock_w,
                bh,
                label,
                size=size,
                align="center",
                valign="middle",
                bg=bg,
                roughness=2,
            )
        )

        if i == 2:
            # Demo: ellipse + arrow annotate a region on the image (not note content)
            ann_x = mock_x + mock_w - 128
            ann_y = y + bh * 0.22
            els.append(
                ellipse(
                    ann_x,
                    ann_y,
                    76,
                    76,
                    bg="#fff5f5",
                    stroke="#e07a5f",
                    roughness=2,
                )
            )
            els.append(arrow_el(ann_x - 44, ann_y + 88, 38, -32))
            els.append(
                text_el(
                    "圈重点",
                    ann_x + 10,
                    ann_y + 24,
                    56,
                    size=15,
                    align="center",
                    color="#e07a5f",
                )
            )
            callout_y = ann_y + 28
            els.append(arrow_el(mock_x + mock_w + 6, callout_y, callout_x - mock_x - mock_w - 12, 0))
            els.append(text_el(callout, callout_x, callout_y - 20, 132, size=20, color=TITLE))
        else:
            els.append(arrow_el(mock_x + mock_w + 6, cy - 4, callout_x - mock_x - mock_w - 12, 0))
            els.append(text_el(callout, callout_x, cy - 22, 132, size=22, color=TITLE))

        if i < 2:
            next_bh = box2_h if i == 0 else box3_h
            els.append(arrow_el(mock_x + mock_w // 2 - 12, y + bh + 4, 0, arrow_len))
            y += bh + arrow_len + arrow_gap
        else:
            y += bh

    # Feature chips row
    chip_gap = 18
    chip_w = (inner - chip_gap * 2) / 3
    chip_x0 = pad
    chips = [
        ("圆角框", "#ffc9c9"),
        ("手写字", "#e5dbff"),
        ("JSON 文件", "#b2f2bb"),
    ]
    els.append(
        rect(pad, chips_y - 8, inner, chips_h + 16, bg="#ffffff", stroke=STROKE, roughness=2)
    )
    els.append(
        text_el(
            "核心元素",
            pad + 14,
            chips_y - 2,
            80,
            size=15,
            color=TITLE,
        )
    )
    for i, (label, bg) in enumerate(chips):
        cx = chip_x0 + i * (chip_w + chip_gap)
        els.extend(
            rect_with_text(
                cx,
                chips_y + 18,
                chip_w,
                chips_h - 22,
                label,
                size=28,
                align="center",
                valign="middle",
                bg=bg,
                roughness=2,
            )
        )
        if i < 2:
            els.append(arrow_el(cx + chip_w + 4, chips_y + chips_h // 2, chip_gap - 8, 0))

    dash = line_el(pad, footer_dash_y, inner, 0, stroke=STROKE, roughness=2)
    dash["strokeStyle"] = "dashed"
    dash["strokeWidth"] = 2
    els.append(dash)
    els.append(
        text_el(
            "不是海报模板商城\n元素是 JSON · 在自己手里",
            pad,
            footer_y,
            inner,
            size=26,
            align="center",
            color=TITLE,
            family=FONT_EXCALIFONT,
        )
    )
    return els


def build_p3(files: dict) -> list[dict]:
    pad = 36
    inner = CANVAS_W - pad * 2
    els: list[dict] = [frame_el("P3 不需要花模板", 0, 0, CANVAS_W, CANVAS_H)]
    els.append(rect(0, 0, CANVAS_W, CANVAS_H, bg=BG, stroke="transparent", roughness=0))

    body = (
        "我以前打开模板站\n"
        "找边框、找滤镜\n"
        "半小时还在调样式\n"
        "\n"
        "现在我常是：\n"
        "截图 + 两句话 + 一张图\n"
        "\n"
        "不是工具弱\n"
        "是这种内容，不需要花"
    )
    text_size = 26
    text_pad = 16
    text_y = 32
    text_h = text_block_height(body, text_size, text_pad)
    els.extend(
        rect_with_text(
            pad,
            text_y,
            inner,
            text_h,
            body,
            size=text_size,
            valign="top",
            padding=text_pad,
        )
    )

    footer_size = 24
    footer_h = 32
    footer_y = CANVAS_H - pad - footer_h
    label_h = 24
    label_gap = 6
    section_gap = 12
    frame_pad = 5
    stack_top = text_y + text_h + 14

    nat1 = image_size(P3_TEMPLATE_IMG)
    crop1 = image_crop_template_p3(*nat1)
    vis1 = (crop1["width"], crop1["height"])
    vis2 = image_size(P3_SIMPLE_IMG)

    chrome_h = (label_h + label_gap) * 2 + section_gap + frame_pad * 4 + 12
    images_max_h = footer_y - stack_top - chrome_h
    _, [(w1, h1), (w2, h2)] = fit_stack_full_width(
        [vis1, vis2], inner, images_max_h, section_gap
    )
    img_scale = 0.95
    w1, h1 = w1 * img_scale, h1 * img_scale
    w2, h2 = w2 * img_scale, h2 * img_scale

    id1, file1 = _file_entry(P3_TEMPLATE_IMG)
    id2, file2 = _file_entry(P3_SIMPLE_IMG)
    files[id1] = file1
    files[id2] = file2

    cur_y = stack_top
    els.append(text_el("花模板", pad, cur_y, inner, size=22, color=TITLE))
    cur_y += label_h + label_gap
    x1 = pad + (inner - w1) / 2
    els.append(
        rect(
            x1 - frame_pad,
            cur_y - frame_pad,
            w1 + frame_pad * 2,
            h1 + frame_pad * 2,
            bg="#ffffff",
            stroke=STROKE,
            roughness=1,
        )
    )
    els.append(image_el(id1, x1, cur_y, w1, h1, crop=crop1))
    cur_y += h1 + frame_pad * 2 + section_gap

    els.append(text_el("简单排版", pad, cur_y, inner, size=22, color=TITLE))
    cur_y += label_h + label_gap
    x2 = pad + (inner - w2) / 2
    els.append(
        rect(
            x2 - frame_pad,
            cur_y - frame_pad,
            w2 + frame_pad * 2,
            h2 + frame_pad * 2,
            bg="#ffffff",
            stroke=STROKE,
            roughness=1,
        )
    )
    els.append(image_el(id2, x2, cur_y, w2, h2))
    cur_y += h2 + frame_pad * 2

    els.append(
        text_el(
            "内容截图 + 两句话 + 一张图，够用",
            pad,
            footer_y,
            inner,
            size=footer_size,
            align="center",
            color=TITLE,
            family=FONT_EXCALIFONT,
        )
    )
    return els


def build_p4(files: dict) -> list[dict]:
    """Agent + MCP flow — showcase-style colored nodes and before/after vignettes."""
    pad = 36
    inner = CANVAS_W - pad * 2
    els: list[dict] = [frame_el("P4 Agent + MCP", 0, 0, CANVAS_W, CANVAS_H)]
    els.append(rect(0, 0, CANVAS_W, CANVAS_H, bg=BG, stroke="transparent", roughness=0))

    footer_text_h = 28
    footer_y = CANVAS_H - pad - footer_text_h
    footer_dash_y = footer_y - 14

    gap_intro_flow = 18
    gap_flow_panel = 20
    gap_panel_col = 18
    panel_title_h = 40
    panel_footer_h = 46

    intro = "以前：打开画布，自己拖元素\n\n现在：跟 Agent 说 → MCP 改画布 → 导出 PNG"
    intro_h = text_block_height(intro, 23, 14)
    intro_y = 32
    els.extend(
        rect_with_text(
            pad,
            intro_y,
            inner,
            intro_h,
            intro,
            size=23,
            valign="top",
            padding=14,
            bg="#ffffff",
            roughness=2,
        )
    )

    # Horizontal main flow inside swimlane frame (A + B)
    flow_top = intro_y + intro_h + gap_intro_flow
    flow_frame_h = 248
    flow_x0 = pad
    flow_w = inner

    els.append(
        rect(flow_x0, flow_top, flow_w, flow_frame_h, bg="#ffffff", stroke=STROKE, roughness=2)
    )
    els.append(
        text_el(
            "跟 Agent 说一句话，走完这条链路",
            flow_x0 + 16,
            flow_top + 10,
            flow_w - 32,
            size=19,
            align="center",
            color=TITLE,
        )
    )

    # Left "步骤" label + step numbers above each node (B)
    step_num_y = flow_top + 38
    els.append(text_el("步骤", flow_x0 + 14, step_num_y + 4, 40, size=16, color=TITLE))
    step_nums = ["①", "②", "③", "④", "⑤"]

    nodes_spec: list[tuple] = [
        ("ellipse", 68, 48, "你", "#d0ebff", FONT_XIAOLAI, 22),
        ("rect", 90, 52, "Agent", "#a5d8ff", FONT_VIRGIL, 23),
        ("diamond", 80, 66, "MCP", "#fff3bf", FONT_VIRGIL, 19),
        ("rect", 104, 52, "Excalidraw", "#ffd8a8", FONT_VIRGIL, 18),
        ("rect", 64, 44, "PNG", "#b2f2bb", FONT_VIRGIL, 21),
    ]
    arrow_tags = ["说", "", "改画布", "导出"]

    lane_left = flow_x0 + 56
    lane_w = flow_w - 72
    row_cy = flow_top + 128

    total_nw = sum(s[1] for s in nodes_spec)
    arrow_gap = (lane_w - total_nw) / (len(nodes_spec) - 1)

    x = lane_left
    for i, spec in enumerate(nodes_spec):
        shape, w, h, label, bg, fam, sz = spec
        nx = x
        ny = row_cy - h / 2

        els.append(
            text_el(
                step_nums[i],
                nx,
                step_num_y,
                w,
                size=20,
                align="center",
                color=TITLE,
                family=FONT_VIRGIL,
            )
        )
        els.extend(labeled_node(shape, nx, ny, w, h, label, bg=bg, roughness=2, size=sz, family=fam))

        if shape == "diamond":
            els.append(
                text_el(
                    "接线员",
                    nx,
                    ny + h + 2,
                    w,
                    size=14,
                    align="center",
                    color=BODY,
                )
            )

        if i < len(nodes_spec) - 1:
            ax = x + w + 6
            aw = max(arrow_gap - 12, 28)
            els.append(arrow_right(ax, row_cy - 6, aw))
            if arrow_tags[i]:
                els.append(
                    text_el(
                        arrow_tags[i],
                        ax + aw / 2 - 22,
                        row_cy + 8,
                        44,
                        size=15,
                        align="center",
                        color=TITLE,
                    )
                )
        x += w + arrow_gap

    # In-frame callout below pipeline
    callout_y = flow_top + flow_frame_h - 50
    els.append(
        rect(
            flow_x0 + 56,
            callout_y,
            flow_w - 112,
            40,
            bg="#f8fafb",
            stroke=STROKE,
            roughness=1,
        )
    )
    els.append(
        text_el(
            "任何支持 MCP 的 Agent 都能接 · 元素仍是 JSON",
            flow_x0 + 68,
            callout_y + 8,
            flow_w - 136,
            size=17,
            align="center",
            color=TITLE,
            family=FONT_EXCALIFONT,
        )
    )

    # Before / after vignettes — fill space down to footer
    panel_y = flow_top + flow_frame_h + gap_flow_panel
    panel_h = footer_dash_y - gap_flow_panel - panel_y
    panel_w = (inner - gap_panel_col) / 2
    left_x = pad
    right_x = pad + panel_w + gap_panel_col
    panel_body_h = panel_h - panel_title_h - panel_footer_h

    els.append(
        rect(left_x, panel_y, panel_w, panel_h, bg="#ffffff", stroke=STROKE, roughness=2)
    )
    els.append(
        text_el(
            "自己拖排版（手 + 画布）",
            left_x,
            panel_y + 12,
            panel_w,
            size=22,
            align="center",
            color=TITLE,
        )
    )
    # Messy manual layout — centered in panel body
    mess_h = 196
    my = panel_y + panel_title_h + (panel_body_h - mess_h) / 2
    mx = left_x + 28
    els.append(rect(mx, my, 82, 56, bg="#ffc9c9", stroke="#1e1e1e", roughness=2))
    els.append(rect(mx + 96, my + 44, 108, 48, bg="#d0ebff", stroke="#1e1e1e", roughness=2))
    els.append(rect(mx + 36, my + 108, 72, 58, bg="#fff3bf", stroke="#1e1e1e", roughness=2))
    els.append(ellipse(mx + 188, my + 8, 58, 58, bg="#e5dbff", stroke="#1e1e1e", roughness=2))
    els.append(arrow_el(mx + 78, my + 58, 52, 36))
    els.append(arrow_el(mx + 128, my + 124, -44, -28))
    dash_y = panel_y + panel_h - panel_footer_h + 8
    dash = line_el(mx + 8, dash_y, panel_w - 48, 0, stroke=STROKE, roughness=2)
    dash["strokeStyle"] = "dashed"
    els.append(dash)
    els.append(text_el("拖来拖去…", mx + 8, dash_y + 8, panel_w - 56, size=18, color=BODY))

    els.append(
        rect(right_x, panel_y, panel_w, panel_h, bg="#ffffff", stroke=STROKE, roughness=2)
    )
    els.append(
        text_el(
            "说话排版（Agent + MCP）",
            right_x,
            panel_y + 12,
            panel_w,
            size=22,
            align="center",
            color=TITLE,
        )
    )
    # Clean mini pipeline — centered in panel body
    rx = right_x + 36
    mini_w = panel_w - 72
    mini_h = 188
    ry = panel_y + panel_title_h + (panel_body_h - mini_h) / 2
    step = (mini_w - 52 * 3 - 28 * 2) / 2
    els.extend(labeled_node("ellipse", rx, ry, 52, 44, "说", bg="#d0ebff", roughness=2, size=18))
    els.append(arrow_right(rx + 54, ry + 18, step))
    els.extend(
        labeled_node("rect", rx + 54 + step, ry - 4, 52, 52, "AI", bg="#a5d8ff", roughness=2, size=20, family=FONT_VIRGIL)
    )
    els.append(arrow_right(rx + 54 + step + 54, ry + 18, step))
    els.extend(
        labeled_node("diamond", rx + 54 + step * 2 + 54, ry - 8, 52, 52, "MCP", bg="#fff3bf", roughness=2, size=16, family=FONT_VIRGIL)
    )
    ry2 = ry + 86
    els.append(arrow_down(rx + mini_w / 2 - 52, ry + 58, 22))
    els.extend(
        labeled_node(
            "rect",
            rx + (mini_w - 120) / 2,
            ry2,
            120,
            48,
            "画布",
            bg="#ffd8a8",
            roughness=2,
            size=20,
        )
    )
    els.append(arrow_down(rx + mini_w / 2 - 8, ry2 + 52, 18))
    els.extend(
        labeled_node(
            "rect",
            rx + (mini_w - 72) / 2,
            ry2 + 70,
            72,
            40,
            "PNG",
            bg="#b2f2bb",
            roughness=2,
            size=18,
            family=FONT_VIRGIL,
        )
    )

    # Footer pinned to bottom
    dash2 = line_el(pad, footer_dash_y, inner, 0, stroke=STROKE, roughness=2)
    dash2["strokeStyle"] = "dashed"
    els.append(dash2)
    els.append(
        text_el(
            "不限某一个软件 · 元素仍是 JSON",
            pad,
            footer_y,
            inner,
            size=21,
            align="center",
            color=TITLE,
            family=FONT_EXCALIFONT,
        )
    )
    return els


def export_pngs(excalidraw_paths: list[tuple[str, Path]]) -> list[Path]:
    """Export PNG via Excalidraw exportToBlob (Virgil + Xiaolai), same engine as excalidraw.com."""
    export_script = ROOT / "scripts" / "export_excalidraw_png.mjs"
    env = os.environ.copy()
    env["PLAYWRIGHT_BROWSERS_PATH"] = str(ROOT / ".playwright-browsers")

    paths: list[Path] = []
    for slug, png_name in excalidraw_paths:
        src = OUT_DIR / f"{slug}.excalidraw"
        dst = ASSETS / png_name
        subprocess.run(
            ["node", str(export_script), str(src), str(dst), "3"],
            check=True,
            env=env,
            cwd=ROOT,
        )
        paths.append(dst)
    return paths


def main() -> None:
    pages = [
        ("p2-what", build_p2, False),
        ("p3-no-template", build_p3, True),
        ("p4-mcp", build_p4, False),
    ]

    excalidraw_paths: list[Path] = []
    for slug, builder, uses_files in pages:
        files: dict[str, dict] = {}
        elements = builder(files)
        excalidraw_paths.append(save(slug, elements, files))

    all_files: dict[str, dict] = {}
    all_elements: list[dict] = []
    gap = 120
    for i, (_, builder, _) in enumerate(pages):
        ox = i * (CANVAS_W + gap)
        files: dict[str, dict] = {}
        els = builder(files)
        for el in els:
            if el["type"] != "frame":
                el = {**el, "x": el["x"] + ox}
            else:
                el = {**el, "x": ox}
            all_elements.append(el)
        all_files.update(files)
    excalidraw_paths.append(save("all-pages", all_elements, all_files))

    png_paths = export_pngs(
        [
            ("p2-what", "excalidraw-mcp-p2.png"),
            ("p3-no-template", "excalidraw-mcp-p3.png"),
            ("p4-mcp", "excalidraw-mcp-p4.png"),
        ]
    )

    print("Excalidraw:")
    for p in excalidraw_paths:
        print(f"  {p.relative_to(ROOT)}")
    print("PNG exports:")
    for p in png_paths:
        print(f"  {p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
