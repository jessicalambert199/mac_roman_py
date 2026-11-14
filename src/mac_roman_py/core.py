"""Decode and encode bytes using the Mac Roman character set.

The Mac Roman encoding maps each byte 0x00-0xFF to a Unicode code point.
Bytes 0x00-0x7F match ASCII. Bytes 0x80-0xFF are mapped through a fixed
table. This module implements that mapping directly so it does not depend on
Python's built-in codecs, whose Mac Roman table is not guaranteed to be
identical across implementations.
"""

from __future__ import annotations

# The Mac Roman high half (0x80-0xFF) maps to these Unicode code points.
_HIGH = (
    "\u00c4\u00c5\u00c7\u00c9\u00d1\u00d6\u00dc\u00e1\u00e0\u00e2\u00e4\u00e3\u00e5\u00e7\u00e9\u00e8"
    "\u00ea\u00eb\u00ed\u00ec\u00ee\u00ef\u00f1\u00f3\u00f2\u00f4\u00f6\u00f5\u00fa\u00f9\u00fb\u00fc"
    "\u2020\u00b0\u00a2\u00a3\u00a7\u2022\u00b6\u00df\u00ae\u00a9\u2122\u00b4\u00a8\u2260\u00c6\u00d8"
    "\u221e\u00b1\u2264\u2265\u00a5\u00b5\u2202\u2211\u220f\u03c0\u222b\u00aa\u00ba\u03a9\u00e6\u00f8"
    "\u00bf\u00a1\u00ac\u221a\u0192\u2248\u2206\u00ab\u00bb\u2026\u00a0\u00c0\u00c3\u00d5\u0152\u0153"
    "\u2013\u2014\u201c\u201d\u2018\u2019\u00f7\u25ca\u00ff\u0178\u2044\u20ac\u2039\u203a\ufb01\ufb02"
    "\u2021\u00b7\u201a\u201e\u2030\u00c2\u00ca\u00c1\u00cb\u00c8\u00cd\u00ce\u00cf\u00cc\u00d3\u00d4"
    "\uf8ff\u00d2\u00da\u00db\u00d9\u0131\u02c6\u02dc\u00af\u02d8\u02d9\u02da\u00b8\u02dd\u02db\u02c7"
)

# Build the decode table and the reverse encode table once at import time.
_DECODE_TABLE = [chr(i) for i in range(0x80)] + list(_HIGH)

_ENCODE_TABLE: dict[str, int] = {}
for _i, _ch in enumerate(_DECODE_TABLE):
    # The first occurrence wins. Mac Roman has no duplicate code points in the
    # high half, so this is unambiguous in practice; the guard keeps the
    # invariant explicit if the table is ever edited.
    if _ch not in _ENCODE_TABLE:
        _ENCODE_TABLE[_ch] = _i


def decode(data: bytes) -> str:
    """Decode Mac Roman bytes into a Unicode string.

    Every byte value 0x00-0xFF is valid in Mac Roman, so this function never
    raises for byte input. Passing a non-bytes value raises ``TypeError``.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("decode() requires a bytes-like object")
    return "".join(_DECODE_TABLE[b] for b in data)


def encode(text: str) -> bytes:
    """Encode a Unicode string into Mac Roman bytes.

    Characters that do not exist in Mac Roman raise ``UnicodeEncodeError``.
    The error object reports the offending character and its position so the
    caller can decide how to recover.
    """
    if not isinstance(text, str):
        raise TypeError("encode() requires a str")
    out = bytearray()
    for index, ch in enumerate(text):
        try:
            out.append(_ENCODE_TABLE[ch])
        except KeyError:
            raise UnicodeEncodeError(
                "mac_roman",
                text,
                index,
                index + 1,
                f"character {ch!r} is not in the Mac Roman table",
            ) from None
    return bytes(out)
