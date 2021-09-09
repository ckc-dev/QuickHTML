"""This file contains integration tests, sorted alphabetically."""

import importlib.util
import unittest
from pathlib import Path

MODULE_FILE = Path(__file__).joinpath("../../quickhtml/quickhtml.py").resolve()
SPEC = importlib.util.spec_from_file_location("quickhtml", MODULE_FILE)
QUICKHTML_MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(QUICKHTML_MODULE)
CONVERT = getattr(QUICKHTML_MODULE, "convert")


class NestedTagTest(unittest.TestCase):
    def test_mixed_tags(self):
        self.assertEqual(CONVERT("""
- This is a level 1 unordered list item.
1. This is a level 1 ordered list item.
> This is a level 1 blockquote.
        """), "<ul><li>This is a level 1 unordered list item.</li></ul><ol><li>This is a level 1 ordered list item.</li></ol><blockquote><p>This is a level 1 blockquote.</p></blockquote>")

        self.assertEqual(CONVERT("""
1. This is a level 1 ordered list item.
- This is a level 1 unordered list item.
> This is a level 1 blockquote.
        """), "<ol><li>This is a level 1 ordered list item.</li></ol><ul><li>This is a level 1 unordered list item.</li></ul><blockquote><p>This is a level 1 blockquote.</p></blockquote>")

        self.assertEqual(CONVERT("""
> This is a level 1 blockquote.
- This is a level 1 unordered list item.
1. This is a level 1 ordered list item.
        """), "<blockquote><p>This is a level 1 blockquote.</p></blockquote><ul><li>This is a level 1 unordered list item.</li></ul><ol><li>This is a level 1 ordered list item.</li></ol>")

        self.assertEqual(CONVERT("""
- This is a level 1 unordered list item.
> This is a level 1 blockquote.
1. This is a level 1 ordered list item.
        """), "<ul><li>This is a level 1 unordered list item.</li></ul><blockquote><p>This is a level 1 blockquote.</p></blockquote><ol><li>This is a level 1 ordered list item.</li></ol>")

        self.assertEqual(CONVERT("""
1. This is a level 1 ordered list item.
> This is a level 1 blockquote.
- This is a level 1 unordered list item.
        """), "<ol><li>This is a level 1 ordered list item.</li></ol><blockquote><p>This is a level 1 blockquote.</p></blockquote><ul><li>This is a level 1 unordered list item.</li></ul>")

        self.assertEqual(CONVERT("""
> This is a level 1 blockquote.
1. This is a level 1 ordered list item.
- This is a level 1 unordered list item.
        """), "<blockquote><p>This is a level 1 blockquote.</p></blockquote><ol><li>This is a level 1 ordered list item.</li></ol><ul><li>This is a level 1 unordered list item.</li></ul>")

        self.assertEqual(CONVERT("""
- This is a level 1 unordered list item.
 1. This is a level 2 ordered list item, inside an unordered list.
>>> This is a level 3 blockquote, inside an ordered list.
        """), "<ul><li>This is a level 1 unordered list item.</li><ol><li>This is a level 2 ordered list item, inside an unordered list.</li><blockquote><p>This is a level 3 blockquote, inside an ordered list.</p></blockquote></ol></ul>")

        self.assertEqual(CONVERT("""
  - This is a level 1 unordered list item.
 1. This is a level 1 ordered list item.
> This is a level 1 blockquote.
        """), "<ul><li>This is a level 1 unordered list item.</li></ul><ol><li>This is a level 1 ordered list item.</li></ol><blockquote><p>This is a level 1 blockquote.</p></blockquote>")

        self.assertEqual(CONVERT("""
- This is a level 1 unordered list item.
 1. This is a level 2 ordered list item.
>>> This is a level 3 blockquote.
 1. This is a level 2 ordered list item.
- This is a level 1 unordered list item.
        """), "<ul><li>This is a level 1 unordered list item.</li><ol><li>This is a level 2 ordered list item.</li><blockquote><p>This is a level 3 blockquote.</p></blockquote><li>This is a level 2 ordered list item.</li></ol><li>This is a level 1 unordered list item.</li></ul>")

        self.assertEqual(CONVERT("""
  - This is a level 1 unordered list item.
 1. This is a level 1 ordered list item.
> This is a level 1 blockquote.
 1. This is a level 2 ordered list item.
  - This is a level 3 unordered list item.
        """), "<ul><li>This is a level 1 unordered list item.</li></ul><ol><li>This is a level 1 ordered list item.</li></ol><blockquote><p>This is a level 1 blockquote.</p><ol><li>This is a level 2 ordered list item.</li><ul><li>This is a level 3 unordered list item.</li></ul></ol></blockquote>")

        self.assertEqual(CONVERT("""
- This is a level 1 unordered list item.
 1. This is a level 2 ordered list item.
>>> This is a level 3 blockquote.
>>> This is a level 3 blockquote.
>>> This is a level 3 blockquote.
        """), "<ul><li>This is a level 1 unordered list item.</li><ol><li>This is a level 2 ordered list item.</li><blockquote><p>This is a level 3 blockquote.</p><p>This is a level 3 blockquote.</p><p>This is a level 3 blockquote.</p></blockquote></ol></ul>")

        self.assertEqual(CONVERT("""
- This is a level 1 unordered list item.
 1. This is a level 2 ordered list item.
>>> This is a level 3 blockquote.
  1. This is a level 3 ordered list.
  - This is a level 3 unordered list.
        """), "<ul><li>This is a level 1 unordered list item.</li><ol><li>This is a level 2 ordered list item.</li><blockquote><p>This is a level 3 blockquote.</p></blockquote><ol><li>This is a level 3 ordered list.</li></ol><ul><li>This is a level 3 unordered list.</li></ul></ol></ul>")

        self.assertEqual(CONVERT("""
- This is a level 1 unordered list item.
 1. This is a level 2 ordered list item.
 - This is a level 2 unordered list item.
>> This is a level 2 blockquote.
  - This is a level 3 unordered list item.
        """), "<ul><li>This is a level 1 unordered list item.</li><ol><li>This is a level 2 ordered list item.</li></ol><ul><li>This is a level 2 unordered list item.</li></ul><blockquote><p>This is a level 2 blockquote.</p><ul><li>This is a level 3 unordered list item.</li></ul></blockquote></ul>")

        self.assertEqual(CONVERT("""
  - This is a level 1 unordered list item.
  1. This is a level 1 ordered list item.
>>> This is a level 1 blockquote.
 - This is a level 1 unordered list item.
1. This is a level 1 ordered list item.
        """), "<ul><li>This is a level 1 unordered list item.</li></ul><ol><li>This is a level 1 ordered list item.</li></ol><blockquote><p>This is a level 1 blockquote.</p></blockquote><ul><li>This is a level 1 unordered list item.</li></ul><ol><li>This is a level 1 ordered list item.</li></ol>")

        self.assertEqual(CONVERT("""
- This is a level 1 unordered list item.
 1. This is a level 2 ordered list item.
>>> This is a level 3 blockquote.
>>> This is a level 3 blockquote.
  - This is a level 3 unordered list item.
 1. This is a level 2 ordered list item.
> This is a level 1 blockquote.
        """), "<ul><li>This is a level 1 unordered list item.</li><ol><li>This is a level 2 ordered list item.</li><blockquote><p>This is a level 3 blockquote.</p><p>This is a level 3 blockquote.</p></blockquote><ul><li>This is a level 3 unordered list item.</li></ul><li>This is a level 2 ordered list item.</li></ol></ul><blockquote><p>This is a level 1 blockquote.</p></blockquote>")

        self.assertEqual(CONVERT("""
  - This is a level 1 unordered list item.
 1. This is a level 1 ordered list item.
> This is a level 1 blockquote.
- This is a level 1 unordered list item.
- This is a level 1 unordered list item.
 1. This is a level 2 ordered list item.
  - This is a level 3 unordered list item.
        """), "<ul><li>This is a level 1 unordered list item.</li></ul><ol><li>This is a level 1 ordered list item.</li></ol><blockquote><p>This is a level 1 blockquote.</p></blockquote><ul><li>This is a level 1 unordered list item.</li><li>This is a level 1 unordered list item.</li><ol><li>This is a level 2 ordered list item.</li><ul><li>This is a level 3 unordered list item.</li></ul></ol></ul>")

    def test_inner_mixed_tags(self):
        self.assertEqual(CONVERT("- 1. > This is a blockquote inside an ordered list, inside an unordered list."),
                         "<ul><li><ol><li><blockquote><p>This is a blockquote inside an ordered list, inside an unordered list.</p></blockquote></li></ol></li></ul>")
        self.assertEqual(CONVERT("1. - > This is a blockquote inside an unordered list, inside an ordered list."),
                         "<ol><li><ul><li><blockquote><p>This is a blockquote inside an unordered list, inside an ordered list.</p></blockquote></li></ul></li></ol>")
        self.assertEqual(CONVERT("> - 1. This is an ordered list item, inside an unordered list, inside a blockquote."),
                         "<blockquote><ul><li><ol><li>This is an ordered list item, inside an unordered list, inside a blockquote.</li></ol></li></ul></blockquote>")
        self.assertEqual(CONVERT("- > 1. This is an ordered list item, inside a blockquote, inside an unordered list."),
                         "<ul><li><blockquote><ol><li>This is an ordered list item, inside a blockquote, inside an unordered list.</li></ol></blockquote></li></ul>")
        self.assertEqual(CONVERT("1. > - This is an unordered list item, inside a blockquote, inside an ordered list."),
                         "<ol><li><blockquote><ul><li>This is an unordered list item, inside a blockquote, inside an ordered list.</li></ul></blockquote></li></ol>")
        self.assertEqual(CONVERT("> 1. - This is an unordered list item, inside an ordered list, inside a blockquote."),
                         "<blockquote><ol><li><ul><li>This is an unordered list item, inside an ordered list, inside a blockquote.</li></ul></li></ol></blockquote>")


if __name__ == '__main__':
    unittest.main()
