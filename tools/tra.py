"""AGS 3.6.1 TRA compiler/decompiler for the Gemini Rue Simplified Chinese patch.

Format notes (verified byte-identical against the shipped German.tra/Polish.tra):
- signature "AGSTranslation\\0"
- blocks: int32 id + int32 size
  id=2 GameID   : int32 uid, int32 len, encrypted game name
  id=1 Dict     : repeated (int32 len + encrypted bytes) source/translation pairs,
                  no NUL terminators in this build, terminated by an empty pair
  id=3 TextOpts : int32 normal font, int32 speech font, int32 right-to-left (-1 = keep)
  id=0 ext      : 16-byte padded name "ext_sopts", int64 size,
                  StringMap {int32 count, (int32 len + bytes) key/value ...}
- file ends with int32 -1 followed by 4 zero bytes
- "encryption" is a cyclic byte-add of b"Avis Durgan"
"""
import struct

KEY = b"Avis Durgan"
SIG = b"AGSTranslation\x00"

GAME_UID = 8939140
GAME_NAME = b"Gemini Rue"
EXT_NAME_RAW = b"ext_sopts" + b"\x00" * 7
DICT_TERM = b"\x00" * 8
TAIL = b"\x00" * 4


def dec(data: bytes) -> bytes:
    return bytes((b - KEY[i % 11]) & 0xFF for i, b in enumerate(data))


def enc(data: bytes) -> bytes:
    return bytes((b + KEY[i % 11]) & 0xFF for i, b in enumerate(data))


def compile_tra(pairs, game_uid=GAME_UID, game_name=GAME_NAME,
                textopts=(-1, -1, -1), sopts=((b"encoding", b"UTF-8"),)):
    """pairs: iterable of (source_bytes, translation_bytes)."""
    o = bytearray()
    o += SIG
    name_e = enc(game_name)
    body = struct.pack("<ii", game_uid, len(name_e)) + name_e
    o += struct.pack("<ii", 2, len(body)) + body
    d = bytearray()
    for s, t in pairs:
        se, te = enc(s), enc(t)
        d += struct.pack("<i", len(se)) + se
        d += struct.pack("<i", len(te)) + te
    d += DICT_TERM
    o += struct.pack("<ii", 1, len(d)) + bytes(d)
    body = struct.pack("<3i", *textopts)
    o += struct.pack("<ii", 3, len(body)) + body
    e = bytearray()
    e += struct.pack("<i", len(sopts))
    for k, v in sopts:
        e += struct.pack("<i", len(k)) + k
        e += struct.pack("<i", len(v)) + v
    o += struct.pack("<i", 0) + EXT_NAME_RAW + struct.pack("<q", len(e)) + bytes(e)
    o += struct.pack("<i", -1)
    o += TAIL
    return bytes(o)


def parse(path):
    """Decompile a .tra; returns dict with pairs and metadata (self-check helper)."""
    with open(path, "rb") as f:
        b = f.read()
    assert b[:15] == SIG, "bad signature"
    pos = 15
    out = {"pairs": [], "game_uid": None, "game_name": None,
           "textopts": None, "sopts": []}
    while pos < len(b):
        (bid,) = struct.unpack_from("<i", b, pos)
        pos += 4
        if bid == -1:
            break
        if bid == 0:
            pos += 16
            (sz,) = struct.unpack_from("<q", b, pos)
            pos += 8
            data = b[pos:pos + sz]
            pos += sz
            p = 0
            (count,) = struct.unpack_from("<i", data, p); p += 4
            for _ in range(count):
                (kl,) = struct.unpack_from("<i", data, p); p += 4
                k = data[p:p + kl]; p += kl
                (vl,) = struct.unpack_from("<i", data, p); p += 4
                v = data[p:p + vl]; p += vl
                out["sopts"].append((k, v))
            continue
        (sz,) = struct.unpack_from("<i", b, pos)
        pos += 4
        data = b[pos:pos + sz]
        pos += sz
        if bid == 2:
            (uid,) = struct.unpack_from("<i", data, 0)
            (nl,) = struct.unpack_from("<i", data, 4)
            out["game_uid"] = uid
            out["game_name"] = dec(data[8:8 + nl])
        elif bid == 1:
            p = 0
            while p < sz:
                (l1,) = struct.unpack_from("<i", data, p); p += 4
                s1 = data[p:p + l1]; p += l1
                (l2,) = struct.unpack_from("<i", data, p); p += 4
                s2 = data[p:p + l2]; p += l2
                if l1 == 0 and l2 == 0:
                    break
                out["pairs"].append((dec(s1), dec(s2)))
        elif bid == 3:
            out["textopts"] = list(struct.unpack_from(f"<{sz // 4}i", data, 0))
    return out
