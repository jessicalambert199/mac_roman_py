import unittest

from mac_roman_py import decode, encode
from mac_roman_py.core import _HIGH


class TestDecode(unittest.TestCase):
    def test_ascii_is_identity(self):
        self.assertEqual(decode(b"Hello, world!"), "Hello, world!")

    def test_empty_input(self):
        self.assertEqual(decode(b""), "")

    def test_every_byte_decodes(self):
        # The decoder must accept all 256 byte values without raising.
        result = decode(bytes(range(256)))
        self.assertEqual(len(result), 256)
        self.assertEqual(result[0], "\x00")
        self.assertEqual(result[127], "\x7f")

    def test_high_half_matches_declared_table(self):
        # The exported _HIGH table is the source of truth for 0x80-0xFF.
        self.assertEqual(decode(bytes(range(0x80, 0x100))), "".join(_HIGH))

    def test_known_mac_roman_characters(self):
        # Spot checks against the published Mac Roman mapping.
        self.assertEqual(decode(b"\x80"), "\u00c4")  # A-dieresis
        self.assertEqual(decode(b"\xa5"), "\u2022")  # bullet
        self.assertEqual(decode(b"\xd5"), "\u2019")  # right single quote
        self.assertEqual(decode(b"\xdb"), "\u20ac")  # euro sign
        self.assertEqual(decode(b"\xff"), "\u02c7")  # caron

    def test_bytearray_is_accepted(self):
        self.assertEqual(decode(bytearray(b"\x80")), "\u00c4")

    def test_non_bytes_raises_type_error(self):
        with self.assertRaises(TypeError):
            decode("not bytes")  # type: ignore[arg-type]


class TestEncode(unittest.TestCase):
    def test_ascii_is_identity(self):
        self.assertEqual(encode("Hello, world!"), b"Hello, world!")

    def test_empty_input(self):
        self.assertEqual(encode(""), b"")

    def test_round_trip_all_bytes(self):
        original = bytes(range(256))
        self.assertEqual(encode(decode(original)), original)

    def test_known_characters(self):
        self.assertEqual(encode("\u00c4"), b"\x80")
        self.assertEqual(encode("\u2022"), b"\xa5")
        self.assertEqual(encode("\u2019"), b"\xd5")
        self.assertEqual(encode("\u20ac"), b"\xdb")
        self.assertEqual(encode("\u02c7"), b"\xff")

    def test_unmappable_character_raises(self):
        # U+4E00 (CJK) is not in Mac Roman.
        with self.assertRaises(UnicodeEncodeError) as ctx:
            encode("a\u4e00b")
        self.assertEqual(ctx.exception.start, 1)
        self.assertEqual(ctx.exception.end, 2)
        self.assertEqual(ctx.exception.object, "a\u4e00b")

    def test_unmappable_character_at_start(self):
        with self.assertRaises(UnicodeEncodeError) as ctx:
            encode("\u4e00")
        self.assertEqual(ctx.exception.start, 0)
        self.assertEqual(ctx.exception.end, 1)

    def test_non_str_raises_type_error(self):
        with self.assertRaises(TypeError):
            encode(b"not str")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
