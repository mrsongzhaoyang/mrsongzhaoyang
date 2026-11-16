#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""本地预览：用 GitHub 官方 Markdown 渲染接口 + 官方样式，尽量还原 README 的真实效果。

    python3 tools/build_preview.py     # 产物 preview/rendered.html

只用于本地验收，不需要提交到仓库。
"""

from __future__ import annotations

import json
import os
import re
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREVIEW = os.path.join(ROOT, "preview")
CSS_URL = "https://cdn.jsdelivr.net/npm/github-markdown-css@5/github-markdown-dark.css"


def fetch(url: str, data: bytes | None = None, headers: dict | None = None,
          retries: int = 4) -> bytes:
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=data, headers=headers or {})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read()
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"fetch failed: {url}: {last}")


def github_markdown(text: str) -> str:
    payload = json.dumps({"text": text, "mode": "gfm", "context": "mrsongzhaoyang"}).encode()
    body = fetch(
        "https://api.github.com/markdown",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/vnd.github+json",
            "User-Agent": "profile-preview",
        },
    )
    return body.decode("utf-8")


def local_css() -> str:
    path = os.path.join(PREVIEW, "github-markdown-dark.css")
    if not os.path.exists(path) or os.path.getsize(path) < 1000:
        css = fetch(CSS_URL).decode("utf-8")
        with open(path, "w", encoding="utf-8") as f:
            f.write(css)
    with open(path, encoding="utf-8") as f:
        return f.read()


def main() -> None:
    os.makedirs(PREVIEW, exist_ok=True)
    with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as f:
        md = f.read()

    html = github_markdown(md)
    # 相对路径在本地预览里要指向站根
    html = re.sub(r'src="(?!https?:|/)([^"]+)"', r'src="/\1"', html)
    html = re.sub(r'href="(?!https?:|#|/)([^"]+\.(?:svg|yml|py))"', r'href="#"', html)

    page = f"""<!DOCTYPE html>
<html lang="zh-CN" data-color-mode="dark" data-dark-theme="dark">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>README 预览 · mrsongzhaoyang</title>
<style>
/*__GITHUB_MD_CSS__*/
</style>
<style>
  html, body {{ background:#0d1117; }}
  body {{ margin:0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji"; }}
  .page {{ max-width: 1012px; margin: 0 auto; padding: 32px 32px 80px; }}
  .repo-head {{ display:flex; align-items:center; gap:8px; color:#8b949e; font-size:14px; margin-bottom:16px;
                border-bottom:1px solid #30363d; padding-bottom:12px; }}
  .repo-head b {{ color:#e6edf3; font-weight:600; }}
  .box {{ border:1px solid #30363d; border-radius:6px; }}
  .box-head {{ border-bottom:1px solid #30363d; padding:10px 16px; font-size:14px; color:#8b949e; display:flex; gap:8px; align-items:center; }}
  .markdown-body {{ padding: 32px; }}
  .markdown-body img {{ max-width:100%; }}
</style>
</head>
<body>
<div class="page">
  <div class="repo-head"><b>mrsongzhaoyang</b> / <b>mrsongzhaoyang</b> <span style="border:1px solid #30363d;border-radius:2em;padding:0 7px;font-size:12px">Public</span></div>
  <div class="box">
    <div class="box-head"><span>📄</span> README.md</div>
    <article class="markdown-body">
{html}
    </article>
  </div>
</div>
</body>
</html>
"""

    page = page.replace("/*__GITHUB_MD_CSS__*/", local_css())
    out = os.path.join(PREVIEW, "rendered.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    print("preview:", out)
    print("html bytes:", len(html))


if __name__ == "__main__":
    main()
