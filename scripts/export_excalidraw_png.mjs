#!/usr/bin/env node
/**
 * Export .excalidraw → PNG using Excalidraw's exportToBlob (Virgil + Xiaolai).
 * Same rendering path as excalidraw.com — not Pillow / not MCP standalone SVG.
 *
 * Usage:
 *   node scripts/export_excalidraw_png.mjs <input.excalidraw> <output.png> [scale]
 */

import { createServer } from "node:http";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, "..");
process.env.PLAYWRIGHT_BROWSERS_PATH = resolve(ROOT, ".playwright-browsers");

const { chromium } = await import("playwright");

const inputPath = resolve(process.argv[2] ?? "");
const outputPath = resolve(process.argv[3] ?? "");
const scale = Number(process.argv[4] ?? 3);

if (!inputPath || !outputPath) {
  console.error(
    "Usage: node scripts/export_excalidraw_png.mjs <input.excalidraw> <output.png> [scale]",
  );
  process.exit(1);
}

const doc = JSON.parse(readFileSync(inputPath, "utf8"));
const elements = doc.elements.filter((e) => e.type !== "frame" && !e.isDeleted);
const files = doc.files ?? {};
const background = doc.appState?.viewBackgroundColor ?? "#f8fafb";

const html = `<!DOCTYPE html>
<html><head><meta charset="utf-8"></head><body>
<script type="module">
import { exportToBlob } from "https://esm.sh/@excalidraw/excalidraw@0.18.1";

window.exportExcalidrawPng = async (payload) => {
  const blob = await exportToBlob({
    elements: payload.elements,
    files: payload.files,
    appState: {
      exportBackground: true,
      viewBackgroundColor: payload.background,
      exportWithDarkMode: false,
    },
    mimeType: "image/png",
    quality: 1,
    exportPadding: 0,
    exportScale: payload.scale,
  });
  const buf = await blob.arrayBuffer();
  return Array.from(new Uint8Array(buf));
};
window.ready = true;
</script></body></html>`;

function serveHtml() {
  return new Promise((resolvePromise, reject) => {
    const server = createServer((_req, res) => {
      res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
      res.end(html);
    });
    server.listen(0, "127.0.0.1", () => {
      const { port } = server.address();
      resolvePromise({ server, url: `http://127.0.0.1:${port}/` });
    });
    server.on("error", reject);
  });
}

const { server, url } = await serveHtml();
const browser = await chromium.launch({ headless: true });
try {
  const page = await browser.newPage();
  await page.goto(url, { waitUntil: "networkidle", timeout: 120_000 });
  await page.waitForFunction(() => window.ready === true, { timeout: 120_000 });

  const bytes = await page.evaluate(
    async (payload) => window.exportExcalidrawPng(payload),
    { elements, files, background, scale },
  );

  writeFileSync(outputPath, Buffer.from(bytes));
  console.log(`Exported ${outputPath} (${elements.length} elements, scale=${scale})`);
} finally {
  await browser.close();
  server.close();
}
