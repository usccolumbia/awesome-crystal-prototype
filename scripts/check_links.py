#!/usr/bin/env python3
"""Check that every external URL in README.md still resolves (network access required).

    python scripts/check_links.py [--timeout 20] [--workers 8]

HEAD is tried first, then GET. HTTP 403/429 answers are reported as 'blocked' and do not fail the run, because publishers
often reject scripted requests. Results are cached in .link_cache.json so reruns only retry failures.
"""
import argparse, json, re, sys, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = {"User-Agent": "Mozilla/5.0 (awesome-crystal-prototype link checker)"}


def check(url, timeout):
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return url, r.status, ""
        except urllib.error.HTTPError as e:
            if method == "GET" or e.code in (403, 429):
                return url, e.code, str(e.reason)
        except Exception as e:
            if method == "GET":
                return url, 0, type(e).__name__ + ": " + str(e)[:80]
    return url, 0, "unknown"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--timeout", type=int, default=20); ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    urls = sorted(set(re.findall(r"\]\((https?://[^)\s]+)\)", (ROOT / "README.md").read_text())))
    cache_p = ROOT / ".link_cache.json"
    cache = json.loads(cache_p.read_text()) if cache_p.exists() else {}
    todo = [u for u in urls if cache.get(u, {}).get("status") not in range(200, 400)]
    with ThreadPoolExecutor(a.workers) as ex:
        for u, st, msg in ex.map(lambda u: check(u, a.timeout), todo):
            cache[u] = {"status": st, "note": msg}
    cache_p.write_text(json.dumps(cache, indent=1))
    bad = [(u, cache[u]) for u in urls if cache[u]["status"] not in range(200, 400)]
    blocked = [b for b in bad if b[1]["status"] in (403, 429)]
    failed = [b for b in bad if b[1]["status"] not in (403, 429)]
    print(f"{len(urls)} URLs: {len(urls)-len(bad)} ok, {len(blocked)} blocked (403/429), {len(failed)} failed")
    for u, c in blocked:
        print("  blocked", c["status"], u)
    for u, c in failed:
        print("  FAILED ", c["status"], u, c["note"])
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
