"""Build SChinese.tra from source/SChinese.trs.

TRS format: UTF-8 text; lines starting with // are comments; remaining lines
form (source, translation) pairs in order. Trailing spaces are significant —
do not let editors strip them.

Usage: python tools/build_tra.py [output_path]   (default: dist/SChinese.tra)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tra

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRS = os.path.join(ROOT, "source", "SChinese.trs")


def parse_trs(path):
    pairs = []
    pending = None
    with open(path, encoding="utf-8", newline="") as f:
        for raw in f:
            line = raw.rstrip("\r\n")
            if line.startswith("//"):
                continue
            if pending is None:
                pending = line
            else:
                pairs.append((pending, line))
                pending = None
    if pending is not None:
        raise SystemExit(f"TRS has an unpaired trailing source line: {pending[:60]!r}")
    return pairs


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "dist", "SChinese.tra")
    pairs_txt = parse_trs(TRS)
    pairs = [(s.encode("cp1252"), t.encode("utf-8")) for s, t in pairs_txt]
    blob = tra.compile_tra(pairs)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "wb") as f:
        f.write(blob)
    check = tra.parse(out)
    assert check["game_uid"] == tra.GAME_UID
    assert check["sopts"] == [(b"encoding", b"UTF-8")]
    assert len(check["pairs"]) == len(pairs), (len(check["pairs"]), len(pairs))
    n_untranslated = sum(1 for _, t in pairs_txt if not t)
    print(f"built {out}: {len(blob)} bytes, {len(pairs)} pairs, "
          f"{n_untranslated} untranslated, encoding=UTF-8  [self-check OK]")


if __name__ == "__main__":
    main()
