#!/usr/bin/env python3
"""Render every Mermaid block in a file with headless Chrome and report errors.

Usage: render_check.py <file.md|file.mmd> [--screenshot out.png]
Exit:  0 all blocks rendered · 1 a block failed · 2 Chrome unavailable

Needs network access for the pinned Mermaid build on jsdelivr.
Set CHROME=/path/to/chrome if Chrome is not in a standard location.
"""
import html, json, os, re, shutil, subprocess, sys, tempfile

MERMAID = "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs"
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
]


def find_chrome():
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    for c in CHROME_CANDIDATES:
        if os.path.isabs(c) and os.access(c, os.X_OK):
            return c
        if not os.path.isabs(c) and shutil.which(c):
            return shutil.which(c)
    return None


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    path = args[0]
    shot = args[args.index("--screenshot") + 1] if "--screenshot" in args else None

    text = open(path, encoding="utf-8").read()
    blocks = [text] if path.endswith(".mmd") else re.findall(r"```mermaid\n(.*?)```", text, re.S)
    if not blocks:
        print(json.dumps({"ok": False, "error": "no mermaid blocks found"}))
        sys.exit(1)

    chrome = find_chrome()
    if not chrome:
        print(json.dumps({"ok": None, "skipped": "chrome unavailable", "blocks": len(blocks)}))
        sys.exit(2)

    body = "".join(f'<pre class="mermaid" id="b{i}">{html.escape(b)}</pre>' for i, b in enumerate(blocks))
    page = f"""<!doctype html><meta charset="utf-8">
<body style="margin:24px;background:#fff;font-family:-apple-system,sans-serif">{body}
<pre id="status">PENDING</pre>
<script type="module">
import mermaid from '{MERMAID}';
mermaid.initialize({{ startOnLoad: false }});
const results = [];
for (const el of document.querySelectorAll('pre.mermaid')) {{
  try {{ await mermaid.parse(el.textContent); results.push({{ block: +el.id.slice(1) + 1, ok: true }}); }}
  catch (e) {{ results.push({{ block: +el.id.slice(1) + 1, ok: false, error: String(e.message || e).slice(0, 400) }}); }}
}}
try {{ await mermaid.run({{ suppressErrors: true }}); }} catch (e) {{}}
document.getElementById('status').textContent = JSON.stringify(results);
</script>"""

    with tempfile.TemporaryDirectory() as tmp:
        html_path = os.path.join(tmp, "render.html")
        open(html_path, "w", encoding="utf-8").write(page)
        url = "file://" + html_path
        base = [chrome, "--headless=new", "--disable-gpu", "--virtual-time-budget=15000"]
        dom = subprocess.run(base + ["--dump-dom", url], capture_output=True, text=True, timeout=90).stdout
        if shot:
            subprocess.run(base + ["--hide-scrollbars", "--window-size=1400,2600",
                                   f"--screenshot={os.path.abspath(shot)}", url],
                           capture_output=True, timeout=90)

    m = re.search(r'<pre id="status">(.*?)</pre>', dom, re.S)
    raw = html.unescape(m.group(1)) if m else "PENDING"
    if raw == "PENDING":
        print(json.dumps({"ok": False, "error": "render did not finish (network or CDN unavailable?)"}))
        sys.exit(1)
    results = json.loads(raw)
    ok = all(r["ok"] for r in results)
    print(json.dumps({"ok": ok, "blocks": results, "screenshot": shot}, ensure_ascii=False))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
