# mac_roman_py

Decodes and encodes bytes using the Mac Roman character set, the default
encoding for classic Mac OS.

## Usage

```python
from mac_roman_py import decode, encode

text = decode(b"Hello, \x80 world")
print(text)  # Hello, Ä world

raw = encode("Hello, Ä world")
print(raw)  # b'Hello, \x80 world'
```

## Why this exists

Python's built-in `mac_roman` codec is implemented in C and its exact table is
not part of the language specification. A parser that needs to read a classic
Mac resource fork, a HyperCard stack, or an old text file should not depend on
the host interpreter's codec table staying the same across versions or
platforms. This library ships its own explicit table, so a byte decodes to the
same character everywhere.

The trade-off is that `encode` is strict: a character that is not in Mac Roman
raises `UnicodeEncodeError` rather than silently substituting a fallback. That
keeps round-tripping honest. If you need to write lossy text, catch the error
and substitute yourself.

## Edge case

Byte 0xDB is the euro sign (U+20AC) in Mac Roman, not a currency symbol from
the original 1984 table. Apple added it in Mac OS 8.5. This library follows the
later mapping, which is what modern tools expect. The old pre-euro byte 0xDB
mapped to the generic currency sign (U+00A4); that code point is not encodable
here.
