"""This file contains integration tests, sorted alphabetically."""

import importlib.util
import unittest
from pathlib import Path

MODULE_FILE = Path(__file__).joinpath("../../quickhtml/quickhtml.py").resolve()
SPEC = importlib.util.spec_from_file_location("quickhtml", MODULE_FILE)
QUICKHTML_MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(QUICKHTML_MODULE)
CONVERT = getattr(QUICKHTML_MODULE, "convert")


class HeadingAndNestedTagTest(unittest.TestCase):
    def test_blockquote(self):
        self.assertEqual(CONVERT("># This is a level 1 heading inside a blockquote."),
                         "<blockquote><h1>This is a level 1 heading inside a blockquote.</h1></blockquote>")

        self.assertEqual(CONVERT("> >## This is a level 2 heading inside a blockquote, inside another blockquote."),
                         "<blockquote><blockquote><h2>This is a level 2 heading inside a blockquote, inside another blockquote.</h2></blockquote></blockquote>")

        self.assertEqual(CONVERT("> > >### This is a level 3 heading, nested within three blockquotes."),
                         "<blockquote><blockquote><blockquote><h3>This is a level 3 heading, nested within three blockquotes.</h3></blockquote></blockquote></blockquote>")

    def test_unordered_list(self):
        self.assertEqual(CONVERT("- # This is a level 1 heading inside an unordered list."),
                         "<ul><li><h1>This is a level 1 heading inside an unordered list.</h1></li></ul>")

        self.assertEqual(CONVERT("- - ## This is a level 2 heading inside an unordered list, inside another unordered list."),
                         "<ul><li><ul><li><h2>This is a level 2 heading inside an unordered list, inside another unordered list.</h2></li></ul></li></ul>")

        self.assertEqual(CONVERT("- - - ### This is a level 3 heading, nested within three uls."),
                         "<ul><li><ul><li><ul><li><h3>This is a level 3 heading, nested within three uls.</h3></li></ul></li></ul></li></ul>")

    def test_ordered_list(self):
        self.assertEqual(CONVERT("1. # This is a level 1 heading inside an ordered list."),
                         "<ol><li><h1>This is a level 1 heading inside an ordered list.</h1></li></ol>")

        self.assertEqual(CONVERT("1. 1. ## This is a level 2 heading inside an ordered list, inside another ordered list."),
                         "<ol><li><ol><li><h2>This is a level 2 heading inside an ordered list, inside another ordered list.</h2></li></ol></li></ol>")

        self.assertEqual(CONVERT("1. 1. 1. ### This is a level 3 heading, nested within three uls."),
                         "<ol><li><ol><li><ol><li><h3>This is a level 3 heading, nested within three uls.</h3></li></ol></li></ol></li></ol>")

    def test_mixed_tags(self):
        self.assertEqual(CONVERT("- 1. ># This is a level 1 heading, nested within a blockquote, an ordered list, and an unordered list."),
                         "<ul><li><ol><li><blockquote><h1>This is a level 1 heading, nested within a blockquote, an ordered list, and an unordered list.</h1></blockquote></li></ol></li></ul>")

        self.assertEqual(CONVERT("1. - ># This is a level 1 heading, nested within a blockquote, an unordered list, and an ordered list."),
                         "<ol><li><ul><li><blockquote><h1>This is a level 1 heading, nested within a blockquote, an unordered list, and an ordered list.</h1></blockquote></li></ul></li></ol>")

        self.assertEqual(CONVERT(">- 1. # This is a level 1 heading, nested within an ordered list, an unordered list, and a blockquote."),
                         "<blockquote><ul><li><ol><li><h1>This is a level 1 heading, nested within an ordered list, an unordered list, and a blockquote.</h1></li></ol></li></ul></blockquote>")

        self.assertEqual(CONVERT("- >1. # This is a level 1 heading, nested within an ordered list, a blockquote, and an unordered list."),
                         "<ul><li><blockquote><ol><li><h1>This is a level 1 heading, nested within an ordered list, a blockquote, and an unordered list.</h1></li></ol></blockquote></li></ul>")

        self.assertEqual(CONVERT("1. >- # This is a level 1 heading, nested within an unordered list, a blockquote, and an ordered list."),
                         "<ol><li><blockquote><ul><li><h1>This is a level 1 heading, nested within an unordered list, a blockquote, and an ordered list.</h1></li></ul></blockquote></li></ol>")

        self.assertEqual(CONVERT(">1. - # This is a level 1 heading, nested within an unordered list, an ordered list, and a blockquote."),
                         "<blockquote><ol><li><ul><li><h1>This is a level 1 heading, nested within an unordered list, an ordered list, and a blockquote.</h1></li></ul></li></ol></blockquote>")


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

    def test_nested_tag_and_paragraph(self):
        self.assertEqual(CONVERT("""
- This is a level 1 unordered list item.
- This is a level 1 unordered list item.
This is a paragraph.
- This is a level 1 unordered list item.
        """), "<ul><li>This is a level 1 unordered list item.</li><li>This is a level 1 unordered list item.</li></ul><p>This is a paragraph.</p><ul><li>This is a level 1 unordered list item.</li></ul>")

        self.assertEqual(CONVERT("""
1. This is a level 1 ordered list item.
1. This is a level 1 ordered list item.
This is a paragraph.
1. This is a level 1 ordered list item.
        """), "<ol><li>This is a level 1 ordered list item.</li><li>This is a level 1 ordered list item.</li></ol><p>This is a paragraph.</p><ol><li>This is a level 1 ordered list item.</li></ol>")

        self.assertEqual(CONVERT("""
> This is a level 1 blockquote.
> This is a level 1 blockquote.
This is a paragraph.
> This is a level 1 blockquote.
        """), "<blockquote><p>This is a level 1 blockquote.</p><p>This is a level 1 blockquote.</p></blockquote><p>This is a paragraph.</p><blockquote><p>This is a level 1 blockquote.</p></blockquote>")

        self.assertEqual(CONVERT("""
- This is a level 1 unordered list item.
1. This is a level 1 ordered list item.
This is a paragraph.
> This is a level 1 blockquote.
        """), "<ul><li>This is a level 1 unordered list item.</li></ul><ol><li>This is a level 1 ordered list item.</li></ol><p>This is a paragraph.</p><blockquote><p>This is a level 1 blockquote.</p></blockquote>")

        self.assertEqual(CONVERT("""
1. This is a level 1 ordered list item.
- This is a level 1 unordered list item.
This is a paragraph.
> This is a level 1 blockquote.
        """), "<ol><li>This is a level 1 ordered list item.</li></ol><ul><li>This is a level 1 unordered list item.</li></ul><p>This is a paragraph.</p><blockquote><p>This is a level 1 blockquote.</p></blockquote>")

        self.assertEqual(CONVERT("""
> This is a level 1 blockquote.
- This is a level 1 unordered list item.
This is a paragraph.
1. This is a level 1 ordered list item.
        """), "<blockquote><p>This is a level 1 blockquote.</p></blockquote><ul><li>This is a level 1 unordered list item.</li></ul><p>This is a paragraph.</p><ol><li>This is a level 1 ordered list item.</li></ol>")

        self.assertEqual(CONVERT("""
- This is a level 1 unordered list item.
> This is a level 1 blockquote.
This is a paragraph.
1. This is a level 1 ordered list item.
        """), "<ul><li>This is a level 1 unordered list item.</li></ul><blockquote><p>This is a level 1 blockquote.</p></blockquote><p>This is a paragraph.</p><ol><li>This is a level 1 ordered list item.</li></ol>")

        self.assertEqual(CONVERT("""
1. This is a level 1 ordered list item.
> This is a level 1 blockquote.
This is a paragraph.
- This is a level 1 unordered list item.
        """), "<ol><li>This is a level 1 ordered list item.</li></ol><blockquote><p>This is a level 1 blockquote.</p></blockquote><p>This is a paragraph.</p><ul><li>This is a level 1 unordered list item.</li></ul>")

        self.assertEqual(CONVERT("""
> This is a level 1 blockquote.
1. This is a level 1 ordered list item.
This is a paragraph.
- This is a level 1 unordered list item.
        """), "<blockquote><p>This is a level 1 blockquote.</p></blockquote><ol><li>This is a level 1 ordered list item.</li></ol><p>This is a paragraph.</p><ul><li>This is a level 1 unordered list item.</li></ul>")

    def test_nested_tag_and_line_break(self):
        self.assertEqual(CONVERT("""
- This is a level 1 unordered list item.
- This is a level 1 unordered list item.
<br>
- This is a level 1 unordered list item.
        """), "<ul><li>This is a level 1 unordered list item.</li><li>This is a level 1 unordered list item.</li></ul><br><ul><li>This is a level 1 unordered list item.</li></ul>")

        self.assertEqual(CONVERT("""
1. This is a level 1 ordered list item.
1. This is a level 1 ordered list item.
<br>
1. This is a level 1 ordered list item.
        """), "<ol><li>This is a level 1 ordered list item.</li><li>This is a level 1 ordered list item.</li></ol><br><ol><li>This is a level 1 ordered list item.</li></ol>")

        self.assertEqual(CONVERT("""
> This is a level 1 blockquote.
> This is a level 1 blockquote.
<br>
> This is a level 1 blockquote.
        """), "<blockquote><p>This is a level 1 blockquote.</p><p>This is a level 1 blockquote.</p></blockquote><br><blockquote><p>This is a level 1 blockquote.</p></blockquote>")

        self.assertEqual(CONVERT("""
- This is a level 1 unordered list item.
1. This is a level 1 ordered list item.
<br>
> This is a level 1 blockquote.
        """), "<ul><li>This is a level 1 unordered list item.</li></ul><ol><li>This is a level 1 ordered list item.</li></ol><br><blockquote><p>This is a level 1 blockquote.</p></blockquote>")

        self.assertEqual(CONVERT("""
1. This is a level 1 ordered list item.
- This is a level 1 unordered list item.
<br>
> This is a level 1 blockquote.
        """), "<ol><li>This is a level 1 ordered list item.</li></ol><ul><li>This is a level 1 unordered list item.</li></ul><br><blockquote><p>This is a level 1 blockquote.</p></blockquote>")

        self.assertEqual(CONVERT("""
> This is a level 1 blockquote.
- This is a level 1 unordered list item.
<br>
1. This is a level 1 ordered list item.
        """), "<blockquote><p>This is a level 1 blockquote.</p></blockquote><ul><li>This is a level 1 unordered list item.</li></ul><br><ol><li>This is a level 1 ordered list item.</li></ol>")

        self.assertEqual(CONVERT("""
- This is a level 1 unordered list item.
> This is a level 1 blockquote.
<br>
1. This is a level 1 ordered list item.
        """), "<ul><li>This is a level 1 unordered list item.</li></ul><blockquote><p>This is a level 1 blockquote.</p></blockquote><br><ol><li>This is a level 1 ordered list item.</li></ol>")

        self.assertEqual(CONVERT("""
1. This is a level 1 ordered list item.
> This is a level 1 blockquote.
<br>
- This is a level 1 unordered list item.
        """), "<ol><li>This is a level 1 ordered list item.</li></ol><blockquote><p>This is a level 1 blockquote.</p></blockquote><br><ul><li>This is a level 1 unordered list item.</li></ul>")

        self.assertEqual(CONVERT("""
> This is a level 1 blockquote.
1. This is a level 1 ordered list item.
<br>
- This is a level 1 unordered list item.
        """), "<blockquote><p>This is a level 1 blockquote.</p></blockquote><ol><li>This is a level 1 ordered list item.</li></ol><br><ul><li>This is a level 1 unordered list item.</li></ul>")

    def test_nested_tag_and_empty_line(self):
        self.assertEqual(CONVERT("""
- This is a level 1 unordered list item.
- This is a level 1 unordered list item.

- This is a level 1 unordered list item.
        """), "<ul><li>This is a level 1 unordered list item.</li><li>This is a level 1 unordered list item.</li></ul><ul><li>This is a level 1 unordered list item.</li></ul>")

        self.assertEqual(CONVERT("""
1. This is a level 1 ordered list item.
1. This is a level 1 ordered list item.

1. This is a level 1 ordered list item.
        """), "<ol><li>This is a level 1 ordered list item.</li><li>This is a level 1 ordered list item.</li></ol><ol><li>This is a level 1 ordered list item.</li></ol>")

        self.assertEqual(CONVERT("""
> This is a level 1 blockquote.
> This is a level 1 blockquote.

> This is a level 1 blockquote.
        """), "<blockquote><p>This is a level 1 blockquote.</p><p>This is a level 1 blockquote.</p></blockquote><blockquote><p>This is a level 1 blockquote.</p></blockquote>")

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


class ParagraphAndInlineTagTest(unittest.TestCase):
    def test_code(self):
        self.assertEqual(CONVERT("`This is some code` followed by more text."),
                         "<p><code>This is some code</code> followed by more text.</p>")

    def test_link(self):
        self.assertEqual(CONVERT("[This is a link](Link URL.) followed by more text."),
                         "<p><a href=\"Link URL.\">This is a link</a> followed by more text.</p>")

    def test_image(self):
        self.assertEqual(CONVERT("![This is an image](Image path or URL.) followed by more text."),
                         "<p><img src=\"Image path or URL.\" alt=\"This is an image\"> followed by more text.</p>")


if __name__ == '__main__':
    unittest.main()
