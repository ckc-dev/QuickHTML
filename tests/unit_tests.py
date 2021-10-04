"""This file contains unit tests, sorted alphabetically."""

import importlib.util
import unittest
from pathlib import Path

MODULE_FILE = Path(__file__).joinpath("../../quickhtml/quickhtml.py").resolve()
SPEC = importlib.util.spec_from_file_location("quickhtml", MODULE_FILE)
QUICKHTML_MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(QUICKHTML_MODULE)
CONVERT = getattr(QUICKHTML_MODULE, "convert")


class BlockquoteTest(unittest.TestCase):
    def test_empty_blockquotes(self):
        self.assertEqual(CONVERT(">"), "<p>></p>")
        self.assertEqual(CONVERT(">>"), "<p>>></p>")
        self.assertEqual(CONVERT(">>>"), "<p>>>></p>")

    def test_blockquote(self):
        self.assertEqual(CONVERT(">This is a blockquote."),
                         "<blockquote><p>This is a blockquote.</p></blockquote>")
        self.assertEqual(CONVERT(">>This is a blockquote."),
                         "<blockquote><p>This is a blockquote.</p></blockquote>")
        self.assertEqual(CONVERT(">>>This is a blockquote."),
                         "<blockquote><p>This is a blockquote.</p></blockquote>")

    def test_extra_leading_space(self):
        self.assertEqual(CONVERT("   >This a blockquote with 3 extra leading spaces."),
                         "<blockquote><p>This a blockquote with 3 extra leading spaces.</p></blockquote>")
        self.assertEqual(CONVERT("   >>This a blockquote with 3 extra leading spaces."),
                         "<blockquote><p>This a blockquote with 3 extra leading spaces.</p></blockquote>")
        self.assertEqual(CONVERT("   >>>This a blockquote with 3 extra leading spaces."),
                         "<blockquote><p>This a blockquote with 3 extra leading spaces.</p></blockquote>")

    def test_extra_trailing_space(self):
        self.assertEqual(CONVERT(">This a blockquote with 5 extra trailing spaces.     "),
                         "<blockquote><p>This a blockquote with 5 extra trailing spaces.</p><br></blockquote>")
        self.assertEqual(CONVERT(">>This a blockquote with 5 extra trailing spaces.     "),
                         "<blockquote><p>This a blockquote with 5 extra trailing spaces.</p><br></blockquote>")
        self.assertEqual(CONVERT(">>>This a blockquote with 5 extra trailing spaces.     "),
                         "<blockquote><p>This a blockquote with 5 extra trailing spaces.</p><br></blockquote>")

    def test_extra_space(self):
        self.assertEqual(CONVERT(">     This a blockquote with 5 extra spaces.     "),
                         "<blockquote><p>This a blockquote with 5 extra spaces.</p><br></blockquote>")
        self.assertEqual(CONVERT(">>     This a blockquote with 5 extra spaces.     "),
                         "<blockquote><p>This a blockquote with 5 extra spaces.</p><br></blockquote>")
        self.assertEqual(CONVERT(">>>     This a blockquote with 5 extra spaces.     "),
                         "<blockquote><p>This a blockquote with 5 extra spaces.</p><br></blockquote>")

    def test_multiline(self):
        self.assertEqual(CONVERT(""">This is a level 1 blockquote.
                                    >This is a level 1 blockquote.
                                    >This is a level 1 blockquote."""), "<blockquote><p>This is a level 1 blockquote.</p><p>This is a level 1 blockquote.</p><p>This is a level 1 blockquote.</p></blockquote>")

        self.assertEqual(CONVERT("""
>This is a level 1 blockquote.
>This is a level 1 blockquote.
>This is a level 1 blockquote.
        """), "<blockquote><p>This is a level 1 blockquote.</p><p>This is a level 1 blockquote.</p><p>This is a level 1 blockquote.</p></blockquote>")

        self.assertEqual(CONVERT("""
>>>>>This is a level 1 blockquote.
>>>>>This is a level 1 blockquote.
>>>>>This is a level 1 blockquote.
        """), "<blockquote><p>This is a level 1 blockquote.</p><p>This is a level 1 blockquote.</p><p>This is a level 1 blockquote.</p></blockquote>")

        self.assertEqual(CONVERT("""
>This is a level 1 blockquote.
>>This is a level 2 blockquote.
>>>This is a level 3 blockquote.
        """), "<blockquote><p>This is a level 1 blockquote.</p><blockquote><p>This is a level 2 blockquote.</p><blockquote><p>This is a level 3 blockquote.</p></blockquote></blockquote></blockquote>")

        self.assertEqual(CONVERT("""
   >This is a level 1 blockquote.
   >>This is a level 2 blockquote.
   >>>This is a level 3 blockquote.
        """), "<blockquote><p>This is a level 1 blockquote.</p><blockquote><p>This is a level 2 blockquote.</p><blockquote><p>This is a level 3 blockquote.</p></blockquote></blockquote></blockquote>")

        self.assertEqual(CONVERT("""
>>>>>This is a level 1 blockquote.
>>>>>>>>This is a level 2 blockquote.
>>>>>>>>>>>This is a level 3 blockquote.
        """), "<blockquote><p>This is a level 1 blockquote.</p><blockquote><p>This is a level 2 blockquote.</p><blockquote><p>This is a level 3 blockquote.</p></blockquote></blockquote></blockquote>")

        self.assertEqual(CONVERT("""
>This is a level 1 blockquote.
>This is a level 1 blockquote.
>>>>>>>>>>>>>>>>>>>>This is a level 2 blockquote.
>This is a level 1 blockquote.
            """), "<blockquote><p>This is a level 1 blockquote.</p><p>This is a level 1 blockquote.</p><blockquote><p>This is a level 2 blockquote.</p></blockquote><p>This is a level 1 blockquote.</p></blockquote>")

        self.assertEqual(CONVERT("""
>This is a level 1 blockquote.
>This is a level 1 blockquote.
>This is a level 1 blockquote.
>>This is a level 2 blockquote.
>>This is a level 2 blockquote.
>>>This is a level 3 blockquote.
        """), "<blockquote><p>This is a level 1 blockquote.</p><p>This is a level 1 blockquote.</p><p>This is a level 1 blockquote.</p><blockquote><p>This is a level 2 blockquote.</p><p>This is a level 2 blockquote.</p><blockquote><p>This is a level 3 blockquote.</p></blockquote></blockquote></blockquote>")

        self.assertEqual(CONVERT("""
>This is a level 1 blockquote.
>This is a level 1 blockquote.
>This is a level 1 blockquote.
>>This is a level 2 blockquote.
>>This is a level 2 blockquote.
>>>This is a level 3 blockquote.
>>This is a level 2 blockquote.
>>This is a level 2 blockquote.
>This is a level 1 blockquote.
>This is a level 1 blockquote.
>This is a level 1 blockquote.
        """), "<blockquote><p>This is a level 1 blockquote.</p><p>This is a level 1 blockquote.</p><p>This is a level 1 blockquote.</p><blockquote><p>This is a level 2 blockquote.</p><p>This is a level 2 blockquote.</p><blockquote><p>This is a level 3 blockquote.</p></blockquote><p>This is a level 2 blockquote.</p><p>This is a level 2 blockquote.</p></blockquote><p>This is a level 1 blockquote.</p><p>This is a level 1 blockquote.</p><p>This is a level 1 blockquote.</p></blockquote>")

        self.assertEqual(CONVERT("""
>This is a level 1 blockquote.
>This is a level 1 blockquote.
>This is a level 1 blockquote.
>>This is a level 2 blockquote.
>>This is a level 2 blockquote.
>>>This is a level 3 blockquote.
>>>>This is a level 4 blockquote.
>This is a level 1 blockquote.
        """), "<blockquote><p>This is a level 1 blockquote.</p><p>This is a level 1 blockquote.</p><p>This is a level 1 blockquote.</p><blockquote><p>This is a level 2 blockquote.</p><p>This is a level 2 blockquote.</p><blockquote><p>This is a level 3 blockquote.</p><blockquote><p>This is a level 4 blockquote.</p></blockquote></blockquote></blockquote><p>This is a level 1 blockquote.</p></blockquote>")

        self.assertEqual(CONVERT("""
>>>This is a level 1 blockquote.
>>This is a level 1 blockquote.
>This is a level 1 blockquote.
        """), "<blockquote><p>This is a level 1 blockquote.</p></blockquote><blockquote><p>This is a level 1 blockquote.</p></blockquote><blockquote><p>This is a level 1 blockquote.</p></blockquote>")

        self.assertEqual(CONVERT("""
>>>This is a level 1 blockquote.
>>This is a level 1 blockquote.
>This is a level 1 blockquote.
>This is a level 1 blockquote.
>>This is a level 2 blockquote.
>>>This is a level 3 blockquote.
        """), "<blockquote><p>This is a level 1 blockquote.</p></blockquote><blockquote><p>This is a level 1 blockquote.</p></blockquote><blockquote><p>This is a level 1 blockquote.</p><p>This is a level 1 blockquote.</p><blockquote><p>This is a level 2 blockquote.</p><blockquote><p>This is a level 3 blockquote.</p></blockquote></blockquote></blockquote>")

    def test_should_not_be_affected(self):
        self.assertEqual(CONVERT("This should not be affected. >"),
                         "<p>This should not be affected. ></p>")
        self.assertEqual(CONVERT("This > should > not > be > affected."),
                         "<p>This > should > not > be > affected.</p>")


class CodeBlockTest(unittest.TestCase):
    def test_code_block(self):
        self.assertEqual(CONVERT("    This is some text inside a code block."),
                         "<pre><code>This is some text inside a code block.</code></pre>")

    def test_ignore_inline_tags(self):
        self.assertEqual(CONVERT("    These _are_ some *words* that _would_ be *in* italics _if_ they *weren't* inside _a_ code *block*."),
                         "<pre><code>These _are_ some *words* that _would_ be *in* italics _if_ they *weren't* inside _a_ code *block*.</code></pre>")
        self.assertEqual(CONVERT("    These __are__ some **words** that __would__ be **in** bold __if__ they **weren't** inside __a__ code **block**."),
                         "<pre><code>These __are__ some **words** that __would__ be **in** bold __if__ they **weren't** inside __a__ code **block**.</code></pre>")
        self.assertEqual(CONVERT("    [This](would be a link if it wasn't inside a code block.)"),
                         "<pre><code>[This](would be a link if it wasn't inside a code block.)</code></pre>")
        self.assertEqual(CONVERT("    ![This](would be an image if it wasn't inside a code block.)"),
                         "<pre><code>![This](would be an image if it wasn't inside a code block.)</code></pre>")

    def test_extra_leading_space(self):
        self.assertEqual(CONVERT("     This is some text inside a code block with an extra leading space."),
                         "<pre><code> This is some text inside a code block with an extra leading space.</code></pre>")
        self.assertEqual(CONVERT("      This is some text inside a code block with 2 extra leading spaces."),
                         "<pre><code>  This is some text inside a code block with 2 extra leading spaces.</code></pre>")
        self.assertEqual(CONVERT("       This is some text inside a code block with 3 extra leading spaces."),
                         "<pre><code>   This is some text inside a code block with 3 extra leading spaces.</code></pre>")

    def test_extra_trailing_space(self):
        self.assertEqual(CONVERT("    This is some text inside a code block with an extra trailing space. "),
                         "<pre><code>This is some text inside a code block with an extra trailing space. </code></pre>")
        self.assertEqual(CONVERT("    This is some text inside a code block with 2 extra trailing spaces.  "),
                         "<pre><code>This is some text inside a code block with 2 extra trailing spaces.  </code></pre>")
        self.assertEqual(CONVERT("    This is some text inside a code block with 3 extra trailing spaces.   "),
                         "<pre><code>This is some text inside a code block with 3 extra trailing spaces.   </code></pre>")

    def test_extra_space(self):
        self.assertEqual(CONVERT("     This is some text inside a code block with an extra space. "),
                         "<pre><code> This is some text inside a code block with an extra space. </code></pre>")
        self.assertEqual(CONVERT("      This is some text inside a code block with 2 extra spaces.  "),
                         "<pre><code>  This is some text inside a code block with 2 extra spaces.  </code></pre>")
        self.assertEqual(CONVERT("       This is some text inside a code block with 3 extra spaces.   "),
                         "<pre><code>   This is some text inside a code block with 3 extra spaces.   </code></pre>")

    def test_should_not_be_affected(self):
        self.assertEqual(CONVERT(" This should not be affected."),
                         "<p>This should not be affected.</p>")
        self.assertEqual(CONVERT("  This should not be affected."),
                         "<p>This should not be affected.</p>")
        self.assertEqual(CONVERT("   This should not be affected."),
                         "<p>This should not be affected.</p>")
        self.assertEqual(CONVERT("This should not be affected.    "),
                         "<p>This should not be affected.</p><br>")


class CodeTest(unittest.TestCase):
    def test_empty_code(self):
        self.assertEqual(CONVERT("``"), "<p>``</p>")

    def test_code(self):
        self.assertEqual(CONVERT("`This is some text denoted as code.`"),
                         "<code>This is some text denoted as code.</code>")
        self.assertEqual(CONVERT("This is a `word` denoted as code."),
                         "<p>This is a <code>word</code> denoted as code.</p>")
        self.assertEqual(CONVERT("These are some letters denoted as `c`o`d`e."),
                         "<p>These are some letters denoted as <code>c</code>o<code>d</code>e.</p>")
        self.assertEqual(CONVERT("``This is some code containing `backticks`.``"),
                         "<code>This is some code containing `backticks`.</code>")

    def test_ignore_inline_tags(self):
        self.assertEqual(CONVERT("`These _are_ some *words* that _would_ be *in* italics _if_ they *weren't* denoted _as_ code.`"),
                         "<code>These _are_ some *words* that _would_ be *in* italics _if_ they *weren't* denoted _as_ code.</code>")
        self.assertEqual(CONVERT("`These __are__ some **words** that __would__ be **in** bold __if__ they **weren't** denoted __as__ code.`"),
                         "<code>These __are__ some **words** that __would__ be **in** bold __if__ they **weren't** denoted __as__ code.</code>")
        self.assertEqual(CONVERT("`[This](would be a link if it wasn't denoted as code.)`"),
                         "<code>[This](would be a link if it wasn't denoted as code.)</code>")
        self.assertEqual(CONVERT("`![This](would be an image if it wasn't denoted as code.)`"),
                         "<code>![This](would be an image if it wasn't denoted as code.)</code>")

    def test_extra_leading_space(self):
        self.assertEqual(CONVERT("   `This is some text denoted as code with 3 extra leading spaces.`"),
                         "<code>This is some text denoted as code with 3 extra leading spaces.</code>")
        self.assertEqual(CONVERT("   This is a `word` denoted as code with 3 extra leading spaces."),
                         "<p>This is a <code>word</code> denoted as code with 3 extra leading spaces.</p>")
        self.assertEqual(CONVERT("   These are some letters denoted as `c`o`d`e with 3 extra leading spaces."),
                         "<p>These are some letters denoted as <code>c</code>o<code>d</code>e with 3 extra leading spaces.</p>")
        self.assertEqual(CONVERT("   ``This is some code containing `backticks` with 3 extra leading spaces.``"),
                         "<code>This is some code containing `backticks` with 3 extra leading spaces.</code>")

    def test_extra_trailing_space(self):
        self.assertEqual(CONVERT("`This is some text denoted as code with 5 extra trailing spaces.`     "),
                         "<code>This is some text denoted as code with 5 extra trailing spaces.</code><br>")
        self.assertEqual(CONVERT("This is a `word` denoted as code with 5 extra trailing spaces.     "),
                         "<p>This is a <code>word</code> denoted as code with 5 extra trailing spaces.</p><br>")
        self.assertEqual(CONVERT("These are some letters denoted as `c`o`d`e with 5 extra trailing spaces.     "),
                         "<p>These are some letters denoted as <code>c</code>o<code>d</code>e with 5 extra trailing spaces.</p><br>")
        self.assertEqual(CONVERT("``This is some code containing `backticks` with 5 extra trailing spaces.``     "),
                         "<code>This is some code containing `backticks` with 5 extra trailing spaces.</code><br>")

    def test_extra_space(self):
        self.assertEqual(CONVERT("`     This is some text denoted as code with 5 extra spaces.     `"),
                         "<code>This is some text denoted as code with 5 extra spaces.</code>")
        self.assertEqual(CONVERT("This is a `     word     ` denoted as code with 5 extra spaces."),
                         "<p>This is a <code>word</code> denoted as code with 5 extra spaces.</p>")
        self.assertEqual(CONVERT("These are some letters denoted as `     c     `o`     d     `e with 5 extra spaces."),
                         "<p>These are some letters denoted as <code>c</code>o<code>d</code>e with 5 extra spaces.</p>")
        self.assertEqual(CONVERT("``     This is some code containing `backticks` with 5 extra spaces.     ``"),
                         "<code>This is some code containing `backticks` with 5 extra spaces.</code>")

    def test_should_not_be_affected(self):
        self.assertEqual(CONVERT("`This should not be affected."),
                         "<p>`This should not be affected.</p>")
        self.assertEqual(CONVERT("This should not be affected.`"),
                         "<p>This should not be affected.`</p>")
        self.assertEqual(CONVERT("``This should not be affected."),
                         "<p>``This should not be affected.</p>")
        self.assertEqual(CONVERT("This should not be affected.``"),
                         "<p>This should not be affected.``</p>")


class EmphasisTest(unittest.TestCase):
    def test_italic(self):
        self.assertEqual(CONVERT("*This is some italic text.*"),
                         "<p><em>This is some italic text.</em></p>")
        self.assertEqual(CONVERT("_This is some italic text._"),
                         "<p><em>This is some italic text.</em></p>")

        self.assertEqual(CONVERT("This is an *italic* word."),
                         "<p>This is an <em>italic</em> word.</p>")
        self.assertEqual(CONVERT("This is an _italic_ word."),
                         "<p>This is an <em>italic</em> word.</p>")

        self.assertEqual(CONVERT("These are some i*t*a*l*i*c* letters."),
                         "<p>These are some i<em>t</em>a<em>l</em>i<em>c</em> letters.</p>")
        self.assertEqual(CONVERT("These are some i_t_a_l_i_c_ letters."),
                         "<p>These are some i<em>t</em>a<em>l</em>i<em>c</em> letters.</p>")
        self.assertEqual(CONVERT("These are some i*t*a_l_i*c* letters."),
                         "<p>These are some i<em>t</em>a<em>l</em>i<em>c</em> letters.</p>")
        self.assertEqual(CONVERT("These are some i_t_a*l*i_c_ letters."),
                         "<p>These are some i<em>t</em>a<em>l</em>i<em>c</em> letters.</p>")

        self.assertEqual(CONVERT("_Some_ _italic_ _words._"),
                         "<p><em>Some</em> <em>italic</em> <em>words.</em></p>")
        self.assertEqual(CONVERT("*Some* *italic* *words.*"),
                         "<p><em>Some</em> <em>italic</em> <em>words.</em></p>")
        self.assertEqual(CONVERT("_Some_ *italic* _words._"),
                         "<p><em>Some</em> <em>italic</em> <em>words.</em></p>")
        self.assertEqual(CONVERT("*Some* _italic_ *words.*"),
                         "<p><em>Some</em> <em>italic</em> <em>words.</em></p>")

    def test_bold(self):
        self.assertEqual(CONVERT("**This is some bold text.**"),
                         "<p><strong>This is some bold text.</strong></p>")
        self.assertEqual(CONVERT("__This is some bold text.__"),
                         "<p><strong>This is some bold text.</strong></p>")

        self.assertEqual(CONVERT("This is a **bold** word."),
                         "<p>This is a <strong>bold</strong> word.</p>")
        self.assertEqual(CONVERT("This is a __bold__ word."),
                         "<p>This is a <strong>bold</strong> word.</p>")

        self.assertEqual(CONVERT("These are some b**o**l**d** letters."),
                         "<p>These are some b<strong>o</strong>l<strong>d</strong> letters.</p>")
        self.assertEqual(CONVERT("These are some b__o__l__d__ letters."),
                         "<p>These are some b<strong>o</strong>l<strong>d</strong> letters.</p>")
        self.assertEqual(CONVERT("These are some b**o**l__d__ letters."),
                         "<p>These are some b<strong>o</strong>l<strong>d</strong> letters.</p>")
        self.assertEqual(CONVERT("These are some b__o__l**d** letters."),
                         "<p>These are some b<strong>o</strong>l<strong>d</strong> letters.</p>")

        self.assertEqual(CONVERT("__Some__ __bold__ __words.__"),
                         "<p><strong>Some</strong> <strong>bold</strong> <strong>words.</strong></p>")
        self.assertEqual(CONVERT("**Some** **bold** **words.**"),
                         "<p><strong>Some</strong> <strong>bold</strong> <strong>words.</strong></p>")
        self.assertEqual(CONVERT("__Some__ **bold** __words.__"),
                         "<p><strong>Some</strong> <strong>bold</strong> <strong>words.</strong></p>")
        self.assertEqual(CONVERT("**Some** __bold__ **words.**"),
                         "<p><strong>Some</strong> <strong>bold</strong> <strong>words.</strong></p>")

    def test_bold_italic(self):
        self.assertEqual(CONVERT("***This is some bold and italic text.***"),
                         "<p><em><strong>This is some bold and italic text.</strong></em></p>")
        self.assertEqual(CONVERT("___This is some bold and italic text.___"),
                         "<p><em><strong>This is some bold and italic text.</strong></em></p>")
        self.assertEqual(CONVERT("**_This is some bold and italic text._**"),
                         "<p><strong><em>This is some bold and italic text.</em></strong></p>")
        self.assertEqual(CONVERT("__*This is some bold and italic text.*__"),
                         "<p><strong><em>This is some bold and italic text.</em></strong></p>")
        self.assertEqual(CONVERT("*__This is some bold and italic text.__*"),
                         "<p><em><strong>This is some bold and italic text.</strong></em></p>")
        self.assertEqual(CONVERT("_**This is some bold and italic text.**_"),
                         "<p><em><strong>This is some bold and italic text.</strong></em></p>")

        self.assertEqual(CONVERT("This is a bold and italic ***word***."),
                         "<p>This is a bold and italic <em><strong>word</strong></em>.</p>")
        self.assertEqual(CONVERT("This is a bold and italic ___word___."),
                         "<p>This is a bold and italic <em><strong>word</strong></em>.</p>")
        self.assertEqual(CONVERT("This is a bold and italic **_word_**."),
                         "<p>This is a bold and italic <strong><em>word</em></strong>.</p>")
        self.assertEqual(CONVERT("This is a bold and italic __*word*__."),
                         "<p>This is a bold and italic <strong><em>word</em></strong>.</p>")
        self.assertEqual(CONVERT("This is a bold and italic *__word__*."),
                         "<p>This is a bold and italic <em><strong>word</strong></em>.</p>")
        self.assertEqual(CONVERT("This is a bold and italic _**word**_."),
                         "<p>This is a bold and italic <em><strong>word</strong></em>.</p>")

        self.assertEqual(CONVERT("These are some ***b***o***l***d a***n***d i***t***a***l***i***c*** letters."),
                         "<p>These are some <em><strong>b</strong></em>o<em><strong>l</strong></em>d a<em><strong>n</strong></em>d i<em><strong>t</strong></em>a<em><strong>l</strong></em>i<em><strong>c</strong></em> letters.</p>")
        self.assertEqual(CONVERT("These are some ___b___o___l___d a___n___d i___t___a___l___i___c___ letters."),
                         "<p>These are some <em><strong>b</strong></em>o<em><strong>l</strong></em>d a<em><strong>n</strong></em>d i<em><strong>t</strong></em>a<em><strong>l</strong></em>i<em><strong>c</strong></em> letters.</p>")
        self.assertEqual(CONVERT("These are some **_b_**o**_l_**d a**_n_**d i**_t_**a**_l_**i**_c_** letters."),
                         "<p>These are some <strong><em>b</em></strong>o<strong><em>l</em></strong>d a<strong><em>n</em></strong>d i<strong><em>t</em></strong>a<strong><em>l</em></strong>i<strong><em>c</em></strong> letters.</p>")
        self.assertEqual(CONVERT("These are some __*b*__o__*l*__d a__*n*__d i__*t*__a__*l*__i__*c*__ letters."),
                         "<p>These are some <strong><em>b</em></strong>o<strong><em>l</em></strong>d a<strong><em>n</em></strong>d i<strong><em>t</em></strong>a<strong><em>l</em></strong>i<strong><em>c</em></strong> letters.</p>")
        self.assertEqual(CONVERT("These are some *__b__*o*__l__*d a*__n__*d i*__t__*a*__l__*i*__c__* letters."),
                         "<p>These are some <em><strong>b</strong></em>o<em><strong>l</strong></em>d a<em><strong>n</strong></em>d i<em><strong>t</strong></em>a<em><strong>l</strong></em>i<em><strong>c</strong></em> letters.</p>")
        self.assertEqual(CONVERT("These are some _**b**_o_**l**_d a_**n**_d i_**t**_a_**l**_i_**c**_ letters."),
                         "<p>These are some <em><strong>b</strong></em>o<em><strong>l</strong></em>d a<em><strong>n</strong></em>d i<em><strong>t</strong></em>a<em><strong>l</strong></em>i<em><strong>c</strong></em> letters.</p>")
        self.assertEqual(CONVERT("These are some *__b__*o_**l**_d a__*n*__d i***t***a___l___i**_c_** letters."),
                         "<p>These are some <em><strong>b</strong></em>o<em><strong>l</strong></em>d a<strong><em>n</em></strong>d i<em><strong>t</strong></em>a<em><strong>l</strong></em>i<strong><em>c</em></strong> letters.</p>")

        self.assertEqual(CONVERT("***Some*** ***bold*** ***and*** ***italic*** ***words.***"),
                         "<p><em><strong>Some</strong></em> <em><strong>bold</strong></em> <em><strong>and</strong></em> <em><strong>italic</strong></em> <em><strong>words.</strong></em></p>")
        self.assertEqual(CONVERT("___Some___ ___bold___ ___and___ ___italic___ ___words.___"),
                         "<p><em><strong>Some</strong></em> <em><strong>bold</strong></em> <em><strong>and</strong></em> <em><strong>italic</strong></em> <em><strong>words.</strong></em></p>")
        self.assertEqual(CONVERT("**_Some_** **_bold_** **_and_** **_italic_** **_words._**"),
                         "<p><strong><em>Some</em></strong> <strong><em>bold</em></strong> <strong><em>and</em></strong> <strong><em>italic</em></strong> <strong><em>words.</em></strong></p>")
        self.assertEqual(CONVERT("__*Some*__ __*bold*__ __*and*__ __*italic*__ __*words.*__"),
                         "<p><strong><em>Some</em></strong> <strong><em>bold</em></strong> <strong><em>and</em></strong> <strong><em>italic</em></strong> <strong><em>words.</em></strong></p>")
        self.assertEqual(CONVERT("*__Some__* *__bold__* *__and__* *__italic__* *__words.__*"),
                         "<p><em><strong>Some</strong></em> <em><strong>bold</strong></em> <em><strong>and</strong></em> <em><strong>italic</strong></em> <em><strong>words.</strong></em></p>")
        self.assertEqual(CONVERT("_**Some**_ _**bold**_ _**and**_ _**italic**_ _**words.**_"),
                         "<p><em><strong>Some</strong></em> <em><strong>bold</strong></em> <em><strong>and</strong></em> <em><strong>italic</strong></em> <em><strong>words.</strong></em></p>")

    def test_should_not_be_affected(self):
        self.assertEqual(CONVERT("*This should not be affected_"),
                         "<p>*This should not be affected_</p>")
        self.assertEqual(CONVERT("**This should not be affected__"),
                         "<p>**This should not be affected__</p>")
        self.assertEqual(CONVERT("***This should not be affected___"),
                         "<p>***This should not be affected___</p>")
        self.assertEqual(CONVERT("_This should not be affected*"),
                         "<p>_This should not be affected*</p>")
        self.assertEqual(CONVERT("__This should not be affected**"),
                         "<p>__This should not be affected**</p>")
        self.assertEqual(CONVERT("___This should not be affected***"),
                         "<p>___This should not be affected***</p>")

        self.assertEqual(CONVERT("*This should not be affected *"),
                         "<p>*This should not be affected *</p>")
        self.assertEqual(CONVERT("**This should not be affected **"),
                         "<p>**This should not be affected **</p>")
        self.assertEqual(CONVERT("***This should not be affected ***"),
                         "<p>***This should not be affected ***</p>")
        self.assertEqual(CONVERT("_This should not be affected _"),
                         "<p>_This should not be affected _</p>")
        self.assertEqual(CONVERT("__This should not be affected __"),
                         "<p>__This should not be affected __</p>")
        self.assertEqual(CONVERT("___This should not be affected ___"),
                         "<p>___This should not be affected ___</p>")

        self.assertEqual(CONVERT("_ This should not be affected_"),
                         "<p>_ This should not be affected_</p>")
        self.assertEqual(CONVERT("__ This should not be affected__"),
                         "<p>__ This should not be affected__</p>")
        self.assertEqual(CONVERT("___ This should not be affected___"),
                         "<p>___ This should not be affected___</p>")

        self.assertEqual(CONVERT("*This should not be affected"),
                         "<p>*This should not be affected</p>")
        self.assertEqual(CONVERT("**This should not be affected"),
                         "<p>**This should not be affected</p>")
        self.assertEqual(CONVERT("***This should not be affected"),
                         "<p>***This should not be affected</p>")
        self.assertEqual(CONVERT("_This should not be affected"),
                         "<p>_This should not be affected</p>")
        self.assertEqual(CONVERT("__This should not be affected"),
                         "<p>__This should not be affected</p>")
        self.assertEqual(CONVERT("___This should not be affected"),
                         "<p>___This should not be affected</p>")

        self.assertEqual(CONVERT("This should not be affected*"),
                         "<p>This should not be affected*</p>")
        self.assertEqual(CONVERT("This should not be affected**"),
                         "<p>This should not be affected**</p>")
        self.assertEqual(CONVERT("This should not be affected***"),
                         "<p>This should not be affected***</p>")
        self.assertEqual(CONVERT("This should not be affected_"),
                         "<p>This should not be affected_</p>")
        self.assertEqual(CONVERT("This should not be affected__"),
                         "<p>This should not be affected__</p>")
        self.assertEqual(CONVERT("This should not be affected___"),
                         "<p>This should not be affected___</p>")

        self.assertEqual(CONVERT("This should not be affected *"),
                         "<p>This should not be affected *</p>")
        self.assertEqual(CONVERT("This should not be affected **"),
                         "<p>This should not be affected **</p>")
        self.assertEqual(CONVERT("This should not be affected ***"),
                         "<p>This should not be affected ***</p>")
        self.assertEqual(CONVERT("This should not be affected ****"),
                         "<p>This should not be affected ****</p>")
        self.assertEqual(CONVERT("This should not be affected *****"),
                         "<p>This should not be affected *****</p>")
        self.assertEqual(CONVERT("This should not be affected ******"),
                         "<p>This should not be affected ******</p>")
        self.assertEqual(CONVERT("This should not be affected _"),
                         "<p>This should not be affected _</p>")
        self.assertEqual(CONVERT("This should not be affected __"),
                         "<p>This should not be affected __</p>")
        self.assertEqual(CONVERT("This should not be affected ___"),
                         "<p>This should not be affected ___</p>")
        self.assertEqual(CONVERT("This should not be affected ____"),
                         "<p>This should not be affected ____</p>")
        self.assertEqual(CONVERT("This should not be affected _____"),
                         "<p>This should not be affected _____</p>")
        self.assertEqual(CONVERT("This should not be affected ______"),
                         "<p>This should not be affected ______</p>")

        self.assertEqual(CONVERT("This should not be affected * *"),
                         "<p>This should not be affected * *</p>")
        self.assertEqual(CONVERT("This should not be affected ** **"),
                         "<p>This should not be affected ** **</p>")
        self.assertEqual(CONVERT("This should not be affected *** ***"),
                         "<p>This should not be affected *** ***</p>")
        self.assertEqual(CONVERT("This should not be affected _ _"),
                         "<p>This should not be affected _ _</p>")
        self.assertEqual(CONVERT("This should not be affected __ __"),
                         "<p>This should not be affected __ __</p>")
        self.assertEqual(CONVERT("This should not be affected ___ ___"),
                         "<p>This should not be affected ___ ___</p>")


class EmptyLineTest(unittest.TestCase):
    def test_empty_line(self):
        self.assertEqual(CONVERT(""), "")
        self.assertEqual(CONVERT("     "), "")
        self.assertEqual(CONVERT("\t\t\t"), "")
        self.assertEqual(CONVERT("\n\n\n"), "")
        self.assertEqual(CONVERT("\v\v\v"), "")


class EscapedCharacters(unittest.TestCase):
    def test_blockquote(self):
        self.assertEqual(CONVERT("\>This should not be affected."),
                         "<p>>This should not be affected.</p>")
        self.assertEqual(CONVERT("\>>This should not be affected."),
                         "<p>>>This should not be affected.</p>")
        self.assertEqual(CONVERT("\>>>This should not be affected."),
                         "<p>>>>This should not be affected.</p>")

    def test_bold(self):
        self.assertEqual(CONVERT("\*\*This should not be affected.\*\*"),
                         "<p>**This should not be affected.**</p>")
        self.assertEqual(CONVERT("\_\_This should not be affected.\_\_"),
                         "<p>__This should not be affected.__</p>")

    def test_bold_italic(self):
        self.assertEqual(CONVERT("\_\_\_This should not be affected.\_\_\_"),
                         "<p>___This should not be affected.___</p>")
        self.assertEqual(CONVERT("\*\*\_This should not be affected.\_\*\*"),
                         "<p>**_This should not be affected._**</p>")
        self.assertEqual(CONVERT("\_\_\*This should not be affected.\*\_\_"),
                         "<p>__*This should not be affected.*__</p>")
        self.assertEqual(CONVERT("\*\_\_This should not be affected.\_\_\*"),
                         "<p>*__This should not be affected.__*</p>")
        self.assertEqual(CONVERT("\_\*\*This should not be affected.\*\*\_"),
                         "<p>_**This should not be affected.**_</p>")

    def test_code(self):
        self.assertEqual(CONVERT("\`This should not be affected.\`"),
                         "<p>`This should not be affected.`</p>")
        self.assertEqual(CONVERT("\`\`This should not be affected.\`\`"),
                         "<p>``This should not be affected.``</p>")

    def test_escaped_paragraph(self):
        self.assertEqual(CONVERT("\T\h\i\s\ \s\h\o\\u\l\d\ \\n\o\\t\ \\b\e\ \\a\\f\\f\e\c\\t\e\d\."),
                         "<p>This should not be affected.</p>")

    def test_heading(self):
        self.assertEqual(CONVERT("\# This should not be affected."),
                         "<p># This should not be affected.</p>")
        self.assertEqual(CONVERT("\## This should not be affected."),
                         "<p>## This should not be affected.</p>")
        self.assertEqual(CONVERT("\### This should not be affected."),
                         "<p>### This should not be affected.</p>")
        self.assertEqual(CONVERT("\#### This should not be affected."),
                         "<p>#### This should not be affected.</p>")
        self.assertEqual(CONVERT("\##### This should not be affected."),
                         "<p>##### This should not be affected.</p>")
        self.assertEqual(CONVERT("\###### This should not be affected."),
                         "<p>###### This should not be affected.</p>")

    def test_horizontal_separator(self):
        self.assertEqual(CONVERT("\___"), "<p>___</p>")
        self.assertEqual(CONVERT("\---"), "<p>---</p>")
        self.assertEqual(CONVERT("\***"), "<p>***</p>")

    def test_image(self):
        self.assertEqual(CONVERT("!\[This should not be affected.](Not an image.)"),
                         "<p>![This should not be affected.](Not an image.)</p>")
        self.assertEqual(CONVERT("!\[This should not be affected.](Not an image. \"Not a Title.\")"),
                         "<p>![This should not be affected.](Not an image. \"Not a Title.\")</p>")

    def test_italic(self):
        self.assertEqual(CONVERT("\*This should not be affected.\*"),
                         "<p>*This should not be affected.*</p>")
        self.assertEqual(CONVERT("\_This should not be affected.\_"),
                         "<p>_This should not be affected._</p>")

    def test_link(self):
        self.assertEqual(CONVERT("\[This should not be affected.](Not a link.)"),
                         "<p>[This should not be affected.](Not a link.)</p>")
        self.assertEqual(CONVERT("\[This should not be affected.](Not a link. \"Not a title.\")"),
                         "<p>[This should not be affected.](Not a link. \"Not a title.\")</p>")

    def test_reference_link(self):
        self.assertEqual(CONVERT("""
\[1]:Link URL.
[1]
        """), "<p>[1]:Link URL. [1]</p>")

        self.assertEqual(CONVERT("""
\[1]:Link URL.
[This is a link.][1]
        """), "<p>[1]:Link URL. [This is a link.][1]</p>")

        self.assertEqual(CONVERT("""
\[1]:Link URL. "This is a title."
[1]
        """), "<p>[1]:Link URL. \"This is a title.\" [1]</p>")

        self.assertEqual(CONVERT("""
\[1]:Link URL. "This is a title."
[This is a link.][1]
        """), "<p>[1]:Link URL. \"This is a title.\" [This is a link.][1]</p>")

        self.assertEqual(CONVERT("""
\[1]:Link URL. 'This is a title.'
[This is a link.][1]
        """), "<p>[1]:Link URL. 'This is a title.' [This is a link.][1]</p>")

        self.assertEqual(CONVERT("""
\[1]:Link URL. (This is a title.)
[This is a link.][1]
        """), "<p>[1]:Link URL. (This is a title.) [This is a link.][1]</p>")

        self.assertEqual(CONVERT("""
\[1]:<Link URL.> "This is a title."
[This is a link.][1]
        """), "<p>[1]:<Link URL.> \"This is a title.\" [This is a link.][1]</p>")

        self.assertEqual(CONVERT("""
\[1]:<Link URL.> 'This is a title.'
[This is a link.][1]
        """), "<p>[1]:<Link URL.> 'This is a title.' [This is a link.][1]</p>")

        self.assertEqual(CONVERT("""
\[1]:<Link URL.> (This is a title.)
[This is a link.][1]
        """), "<p>[1]:<Link URL.> (This is a title.) [This is a link.][1]</p>")

        self.assertEqual(CONVERT("""
\[     1     ]     :     Link URL.
[     This is a link.     ]     [     1     ]
        """), "<p>[     1     ]     :     Link URL. [     This is a link.     ]     [     1     ]</p>")

        self.assertEqual(CONVERT("""
\[     1     ]     :     Link URL.     "     This is a title.     "
[     This is a link.     ]     [     1     ]
        """), "<p>[     1     ]     :     Link URL.     \"     This is a title.     \" [     This is a link.     ]     [     1     ]</p>")

        self.assertEqual(CONVERT("""
\[     1     ]     :     Link URL.     '     This is a title.     '
[     This is a link.     ]     [     1     ]
        """), "<p>[     1     ]     :     Link URL.     '     This is a title.     ' [     This is a link.     ]     [     1     ]</p>")

        self.assertEqual(CONVERT("""
\[     1     ]     :     Link URL.     (     This is a title.     )
[     This is a link.     ]     [     1     ]
        """), "<p>[     1     ]     :     Link URL.     (     This is a title.     ) [     This is a link.     ]     [     1     ]</p>")

        self.assertEqual(CONVERT("""
\[     1     ]     :     <     Link URL.     >     "     This is a title.     "
[     This is a link.     ]     [     1     ]
        """), "<p>[     1     ]     :     <     Link URL.     >     \"     This is a title.     \" [     This is a link.     ]     [     1     ]</p>")

        self.assertEqual(CONVERT("""
\[     1     ]     :     <     Link URL.     >     '     This is a title.     '
[     This is a link.     ]     [     1     ]
        """), "<p>[     1     ]     :     <     Link URL.     >     '     This is a title.     ' [     This is a link.     ]     [     1     ]</p>")

        self.assertEqual(CONVERT("""
\[     1     ]     :     <     Link URL.     >     (     This is a title.     )
[     This is a link.     ]     [     1     ]
        """), "<p>[     1     ]     :     <     Link URL.     >     (     This is a title.     ) [     This is a link.     ]     [     1     ]</p>")

        self.assertEqual(CONVERT("""
[1]:Link URL.
\[1]
        """), "<p>[1]</p>")

        self.assertEqual(CONVERT("""
[1]:Link URL.
\[This is a link.]\[1]
        """), "<p>[This is a link.][1]</p>")

        self.assertEqual(CONVERT("""
[1]:Link URL. "This is a title."
\[1]
        """), "<p>[1]</p>")

        self.assertEqual(CONVERT("""
[1]:Link URL. "This is a title."
\[This is a link.]\[1]
        """), "<p>[This is a link.][1]</p>")

        self.assertEqual(CONVERT("""
[1]:Link URL. 'This is a title.'
\[This is a link.]\[1]
        """), "<p>[This is a link.][1]</p>")

        self.assertEqual(CONVERT("""
[1]:Link URL. (This is a title.)
\[This is a link.]\[1]
        """), "<p>[This is a link.][1]</p>")

        self.assertEqual(CONVERT("""
[1]:<Link URL.> "This is a title."
\[This is a link.]\[1]
        """), "<p>[This is a link.][1]</p>")

        self.assertEqual(CONVERT("""
[1]:<Link URL.> 'This is a title.'
\[This is a link.]\[1]
        """), "<p>[This is a link.][1]</p>")

        self.assertEqual(CONVERT("""
[1]:<Link URL.> (This is a title.)
\[This is a link.]\[1]
        """), "<p>[This is a link.][1]</p>")

        self.assertEqual(CONVERT("""
[     1     ]     :     Link URL.
\[     This is a link.     ]     \[     1     ]
        """), "<p>[     This is a link.     ]     [     1     ]</p>")

        self.assertEqual(CONVERT("""
[     1     ]     :     Link URL.     "     This is a title.     "
\[     This is a link.     ]     \[     1     ]
        """), "<p>[     This is a link.     ]     [     1     ]</p>")

        self.assertEqual(CONVERT("""
[     1     ]     :     Link URL.     '     This is a title.     '
\[     This is a link.     ]     \[     1     ]
        """), "<p>[     This is a link.     ]     [     1     ]</p>")

        self.assertEqual(CONVERT("""
[     1     ]     :     Link URL.     (     This is a title.     )
\[     This is a link.     ]     \[     1     ]
        """), "<p>[     This is a link.     ]     [     1     ]</p>")

        self.assertEqual(CONVERT("""
[     1     ]     :     <     Link URL.     >     "     This is a title.     "
\[     This is a link.     ]     \[     1     ]
        """), "<p>[     This is a link.     ]     [     1     ]</p>")

        self.assertEqual(CONVERT("""
[     1     ]     :     <     Link URL.     >     '     This is a title.     '
\[     This is a link.     ]     \[     1     ]
        """), "<p>[     This is a link.     ]     [     1     ]</p>")

        self.assertEqual(CONVERT("""
[     1     ]     :     <     Link URL.     >     (     This is a title.     )
\[     This is a link.     ]     \[     1     ]
        """), "<p>[     This is a link.     ]     [     1     ]</p>")

        self.assertEqual(CONVERT("""
\[1]:Link URL.
\[1]
        """), "<p>[1]:Link URL. [1]</p>")

        self.assertEqual(CONVERT("""
\[1]:Link URL.
\[This is a link.][1]
        """), "<p>[1]:Link URL. [This is a link.][1]</p>")

        self.assertEqual(CONVERT("""
\[1]:Link URL. "This is a title."
\[1]
        """), "<p>[1]:Link URL. \"This is a title.\" [1]</p>")

        self.assertEqual(CONVERT("""
\[1]:Link URL. "This is a title."
\[This is a link.][1]
        """), "<p>[1]:Link URL. \"This is a title.\" [This is a link.][1]</p>")

        self.assertEqual(CONVERT("""
\[1]:Link URL. 'This is a title.'
\[This is a link.][1]
        """), "<p>[1]:Link URL. 'This is a title.' [This is a link.][1]</p>")

        self.assertEqual(CONVERT("""
\[1]:Link URL. (This is a title.)
\[This is a link.][1]
        """), "<p>[1]:Link URL. (This is a title.) [This is a link.][1]</p>")

        self.assertEqual(CONVERT("""
\[1]:<Link URL.> "This is a title."
\[This is a link.][1]
        """), "<p>[1]:<Link URL.> \"This is a title.\" [This is a link.][1]</p>")

        self.assertEqual(CONVERT("""
\[1]:<Link URL.> 'This is a title.'
\[This is a link.][1]
        """), "<p>[1]:<Link URL.> 'This is a title.' [This is a link.][1]</p>")

        self.assertEqual(CONVERT("""
\[1]:<Link URL.> (This is a title.)
\[This is a link.][1]
        """), "<p>[1]:<Link URL.> (This is a title.) [This is a link.][1]</p>")

        self.assertEqual(CONVERT("""
\[     1     ]     :     Link URL.
\[     This is a link.     ]     [     1     ]
        """), "<p>[     1     ]     :     Link URL. [     This is a link.     ]     [     1     ]</p>")

        self.assertEqual(CONVERT("""
\[     1     ]     :     Link URL.     "     This is a title.     "
\[     This is a link.     ]     [     1     ]
        """), "<p>[     1     ]     :     Link URL.     \"     This is a title.     \" [     This is a link.     ]     [     1     ]</p>")

        self.assertEqual(CONVERT("""
\[     1     ]     :     Link URL.     '     This is a title.     '
\[     This is a link.     ]     [     1     ]
        """), "<p>[     1     ]     :     Link URL.     '     This is a title.     ' [     This is a link.     ]     [     1     ]</p>")

        self.assertEqual(CONVERT("""
\[     1     ]     :     Link URL.     (     This is a title.     )
\[     This is a link.     ]     [     1     ]
        """), "<p>[     1     ]     :     Link URL.     (     This is a title.     ) [     This is a link.     ]     [     1     ]</p>")

        self.assertEqual(CONVERT("""
\[     1     ]     :     <     Link URL.     >     "     This is a title.     "
\[     This is a link.     ]     [     1     ]
        """), "<p>[     1     ]     :     <     Link URL.     >     \"     This is a title.     \" [     This is a link.     ]     [     1     ]</p>")

        self.assertEqual(CONVERT("""
\[     1     ]     :     <     Link URL.     >     '     This is a title.     '
\[     This is a link.     ]     [     1     ]
        """), "<p>[     1     ]     :     <     Link URL.     >     '     This is a title.     ' [     This is a link.     ]     [     1     ]</p>")

        self.assertEqual(CONVERT("""
\[     1     ]     :     <     Link URL.     >     (     This is a title.     )
\[     This is a link.     ]     [     1     ]
        """), "<p>[     1     ]     :     <     Link URL.     >     (     This is a title.     ) [     This is a link.     ]     [     1     ]</p>")

    def test_ordered_list(self):
        self.assertEqual(CONVERT("\\1. This should not be affected."),
                         "<p>1. This should not be affected.</p>")
        self.assertEqual(CONVERT("\\20. This should not be affected."),
                         "<p>20. This should not be affected.</p>")
        self.assertEqual(CONVERT("\\300. This should not be affected."),
                         "<p>300. This should not be affected.</p>")

    def test_quick_email(self):
        self.assertEqual(CONVERT("\<email@domain.example>"),
                         "<p><email@domain.example></p>")

    def test_quick_link(self):
        self.assertEqual(CONVERT("\<http://example.http.link>"),
                         "<p><http://example.http.link></p>")

    def test_unordered_list(self):
        self.assertEqual(CONVERT("\- This should not be affected."),
                         "<p>- This should not be affected.</p>")
        self.assertEqual(CONVERT("\* This should not be affected."),
                         "<p>* This should not be affected.</p>")
        self.assertEqual(CONVERT("\+ This should not be affected."),
                         "<p>+ This should not be affected.</p>")


class HeadingTest(unittest.TestCase):
    def test_empty_heading(self):
        self.assertEqual(CONVERT("#"), "<p>#</p>")
        self.assertEqual(CONVERT("##"), "<p>##</p>")
        self.assertEqual(CONVERT("###"), "<p>###</p>")
        self.assertEqual(CONVERT("####"), "<p>####</p>")
        self.assertEqual(CONVERT("#####"), "<p>#####</p>")
        self.assertEqual(CONVERT("######"), "<p>######</p>")
        self.assertEqual(CONVERT("#######"), "<p>#######</p>")

    def test_heading(self):
        self.assertEqual(CONVERT("# This is a level 1 heading."),
                         "<h1>This is a level 1 heading.</h1>")
        self.assertEqual(CONVERT("## This is a level 2 heading."),
                         "<h2>This is a level 2 heading.</h2>")
        self.assertEqual(CONVERT("### This is a level 3 heading."),
                         "<h3>This is a level 3 heading.</h3>")
        self.assertEqual(CONVERT("#### This is a level 4 heading."),
                         "<h4>This is a level 4 heading.</h4>")
        self.assertEqual(CONVERT("##### This is a level 5 heading."),
                         "<h5>This is a level 5 heading.</h5>")
        self.assertEqual(CONVERT("###### This is a level 6 heading."),
                         "<h6>This is a level 6 heading.</h6>")

    def test_extra_leading_space(self):
        self.assertEqual(CONVERT(" # This is a level 1 heading with an extra leading space."),
                         "<h1>This is a level 1 heading with an extra leading space.</h1>")
        self.assertEqual(CONVERT("  ## This is a level 2 heading with 2 extra leading spaces."),
                         "<h2>This is a level 2 heading with 2 extra leading spaces.</h2>")
        self.assertEqual(CONVERT("   ### This is a level 3 heading with 3 extra leading spaces."),
                         "<h3>This is a level 3 heading with 3 extra leading spaces.</h3>")
        self.assertEqual(CONVERT("   #### This is a level 4 heading with 3 extra leading spaces."),
                         "<h4>This is a level 4 heading with 3 extra leading spaces.</h4>")
        self.assertEqual(CONVERT("   ##### This is a level 5 heading with 3 extra leading spaces."),
                         "<h5>This is a level 5 heading with 3 extra leading spaces.</h5>")
        self.assertEqual(CONVERT("   ###### This is a level 6 heading with 3 extra leading spaces."),
                         "<h6>This is a level 6 heading with 3 extra leading spaces.</h6>")

    def test_extra_trailing_space(self):
        self.assertEqual(CONVERT("# This is a level 1 heading with an extra trailing space. "),
                         "<h1>This is a level 1 heading with an extra trailing space.</h1>")
        self.assertEqual(CONVERT("## This is a level 2 heading with 2 extra trailing spaces.  "),
                         "<h2>This is a level 2 heading with 2 extra trailing spaces.</h2><br>")
        self.assertEqual(CONVERT("### This is a level 3 heading with 3 extra trailing spaces.   "),
                         "<h3>This is a level 3 heading with 3 extra trailing spaces.</h3><br>")
        self.assertEqual(CONVERT("#### This is a level 4 heading with 4 extra trailing spaces.    "),
                         "<h4>This is a level 4 heading with 4 extra trailing spaces.</h4><br>")
        self.assertEqual(CONVERT("##### This is a level 5 heading with 5 extra trailing spaces.     "),
                         "<h5>This is a level 5 heading with 5 extra trailing spaces.</h5><br>")
        self.assertEqual(CONVERT("###### This is a level 6 heading with 6 extra trailing spaces.      "),
                         "<h6>This is a level 6 heading with 6 extra trailing spaces.</h6><br>")

    def test_extra_space(self):
        self.assertEqual(CONVERT("# This is a level 1 heading with an extra space."),
                         "<h1>This is a level 1 heading with an extra space.</h1>")
        self.assertEqual(CONVERT("##  This is a level 2 heading with 2 extra spaces."),
                         "<h2>This is a level 2 heading with 2 extra spaces.</h2>")
        self.assertEqual(CONVERT("###   This is a level 3 heading with 3 extra spaces."),
                         "<h3>This is a level 3 heading with 3 extra spaces.</h3>")
        self.assertEqual(CONVERT("####    This is a level 4 heading with 4 extra spaces."),
                         "<h4>This is a level 4 heading with 4 extra spaces.</h4>")
        self.assertEqual(CONVERT("#####     This is a level 5 heading with 5 extra spaces."),
                         "<h5>This is a level 5 heading with 5 extra spaces.</h5>")
        self.assertEqual(CONVERT("######      This is a level 6 heading with 6 extra spaces."),
                         "<h6>This is a level 6 heading with 6 extra spaces.</h6>")

    def test_extra_pound(self):
        self.assertEqual(CONVERT("# This is a level 1 heading with extra \"#\"s on the right side. # ## ### #### ##### ######"),
                         "<h1>This is a level 1 heading with extra \"#\"s on the right side. # ## ### #### ##### ######</h1>")
        self.assertEqual(CONVERT("## This # is ## a ### level #### 2 ##### heading ###### with extra \"#\"s inside."),
                         "<h2>This # is ## a ### level #### 2 ##### heading ###### with extra \"#\"s inside.</h2>")

    def test_extra_space_and_pound(self):
        self.assertEqual(CONVERT("# # This is a level 1 heading with an extra space and \"#\"."),
                         "<h1># This is a level 1 heading with an extra space and \"#\".</h1>")
        self.assertEqual(CONVERT("##  ## This is a level 2 heading with 2 extra spaces and \"#\"s."),
                         "<h2>## This is a level 2 heading with 2 extra spaces and \"#\"s.</h2>")
        self.assertEqual(CONVERT("###   ### This is a level 3 heading with 3 extra spaces and \"#\"s."),
                         "<h3>### This is a level 3 heading with 3 extra spaces and \"#\"s.</h3>")
        self.assertEqual(CONVERT("####    #### This is a level 4 heading with 4 extra spaces and \"#\"s."),
                         "<h4>#### This is a level 4 heading with 4 extra spaces and \"#\"s.</h4>")
        self.assertEqual(CONVERT("#####     ##### This is a level 5 heading with 5 extra spaces and \"#\"s."),
                         "<h5>##### This is a level 5 heading with 5 extra spaces and \"#\"s.</h5>")
        self.assertEqual(CONVERT("######      ###### This is a level 6 heading with 6 extra spaces and \"#\"s."),
                         "<h6>###### This is a level 6 heading with 6 extra spaces and \"#\"s.</h6>")

    def test_should_not_be_affected(self):
        self.assertEqual(CONVERT("This should not be affected. # ## ### #### ##### ######"),
                         "<p>This should not be affected. # ## ### #### ##### ######</p>")
        self.assertEqual(CONVERT("This # should ## not ### be #### affected. ##### ######"),
                         "<p>This # should ## not ### be #### affected. ##### ######</p>")

    def test_alternate_syntax(self):
        self.assertEqual(CONVERT("""
This is a level 1 heading.
==
"""), "<h1>This is a level 1 heading.</h1>")

        self.assertEqual(CONVERT("""
This is a level 1 heading.
=====
"""), "<h1>This is a level 1 heading.</h1>")

        self.assertEqual(CONVERT("""
     This is a level 1 heading with 5 extra leading spaces.
     ==
"""), "<h1>This is a level 1 heading with 5 extra leading spaces.</h1>")

        self.assertEqual(CONVERT("""
This is a level 2 heading.
--
"""), "<h2>This is a level 2 heading.</h2>")

        self.assertEqual(CONVERT("""
This is a level 2 heading.
-----
"""), "<h2>This is a level 2 heading.</h2>")

        self.assertEqual(CONVERT("""
     This is a level 2 heading with 5 extra leading spaces.
     --
"""), "<h2>This is a level 2 heading with 5 extra leading spaces.</h2>")


class HorizontalSeparatorTest(unittest.TestCase):
    def test_underscore(self):
        self.assertEqual(CONVERT("___"), "<hr>")
        self.assertEqual(CONVERT("_____"), "<hr>")
        self.assertEqual(CONVERT("_______"), "<hr>")

    def test_dash(self):
        self.assertEqual(CONVERT("---"), "<hr>")
        self.assertEqual(CONVERT("-----"), "<hr>")
        self.assertEqual(CONVERT("-------"), "<hr>")

    def test_asterisk(self):
        self.assertEqual(CONVERT("***"), "<hr>")
        self.assertEqual(CONVERT("*****"), "<hr>")
        self.assertEqual(CONVERT("*******"), "<hr>")

    def test_should_not_be_affected(self):
        self.assertEqual(CONVERT("_"), "<p>_</p>")
        self.assertEqual(CONVERT("__"), "<p>__</p>")
        self.assertEqual(CONVERT("___ This should not be affected."),
                         "<p>___ This should not be affected.</p>")
        self.assertEqual(CONVERT("This should not be affected. ___"),
                         "<p>This should not be affected. ___</p>")

        self.assertEqual(CONVERT("-"), "<p>-</p>")
        self.assertEqual(CONVERT("--"), "<p>--</p>")
        self.assertEqual(CONVERT("This should not be affected. ---"),
                         "<p>This should not be affected. ---</p>")

        self.assertEqual(CONVERT("*"), "<p>*</p>")
        self.assertEqual(CONVERT("**"), "<p>**</p>")
        self.assertEqual(CONVERT("This should not be affected. ***"),
                         "<p>This should not be affected. ***</p>")


class ImageTest(unittest.TestCase):
    def test_empty_image(self):
        self.assertEqual(CONVERT("![]()"), "<p>![]()</p>")
        self.assertEqual(CONVERT("![]( \"\")"), "<p>![]( \"\")</p>")
        self.assertEqual(CONVERT("![This should not be affected.]()"),
                         "<p>![This should not be affected.]()</p>")
        self.assertEqual(CONVERT("![](This should not be affected.)"),
                         "<p>![](This should not be affected.)</p>")
        self.assertEqual(CONVERT("![](\"This should not be affected.\")"),
                         "<p>![](\"This should not be affected.\")</p>")

    def test_image(self):
        self.assertEqual(CONVERT("![This is an image.](Image path or URL.)"),
                         "<img src=\"Image path or URL.\" alt=\"This is an image.\">")
        self.assertEqual(CONVERT("![     This is an image.     ](     Image path or URL.     )"),
                         "<img src=\"Image path or URL.\" alt=\"This is an image.\">")
        self.assertEqual(CONVERT("This is an image ![image](Image path or URL.) inside a paragraph."),
                         "<p>This is an image <img src=\"Image path or URL.\" alt=\"image\"> inside a paragraph.</p>")
        self.assertEqual(CONVERT("This is an image ![     image     ](     Image path or URL.     ) inside a paragraph."),
                         "<p>This is an image <img src=\"Image path or URL.\" alt=\"image\"> inside a paragraph.</p>")

    def test_image_with_title(self):
        self.assertEqual(CONVERT("![This is an image.](Image path or URL. \"This is a title.\")"),
                         "<img src=\"Image path or URL.\" alt=\"This is an image.\" title=\"This is a title.\">")
        self.assertEqual(CONVERT("![     This is an image.     ](     Image path or URL.     \"This is a title.\"     )"),
                         "<img src=\"Image path or URL.\" alt=\"This is an image.\" title=\"This is a title.\">")
        self.assertEqual(CONVERT("This is an image ![image](Image path or URL. \"This is a title.\") inside a paragraph."),
                         "<p>This is an image <img src=\"Image path or URL.\" alt=\"image\" title=\"This is a title.\"> inside a paragraph.</p>")
        self.assertEqual(CONVERT("This is an image ![     image     ](     Image path or URL.     \"This is a title.\"     ) inside a paragraph."),
                         "<p>This is an image <img src=\"Image path or URL.\" alt=\"image\" title=\"This is a title.\"> inside a paragraph.</p>")


class LineBreakTest(unittest.TestCase):
    def test_blockquote(self):
        self.assertEqual(CONVERT(">Here's a line break inside a blockquote.  "),
                         "<blockquote><p>Here's a line break inside a blockquote.</p><br></blockquote>")
        self.assertEqual(CONVERT(">Here's a level 1 blockquote.\n>Here's a level 1 blockquote followed by a line break.  \n>Here's another level 1 blockquote."),
                         "<blockquote><p>Here's a level 1 blockquote.</p><p>Here's a level 1 blockquote followed by a line break.</p><br><p>Here's another level 1 blockquote.</p></blockquote>")
        self.assertEqual(CONVERT(">Here's a level 1 blockquote.\n>>Here's a level 2 blockquote.\n>>>Here's a level 3 blockquote followed by a line break.  "),
                         "<blockquote><p>Here's a level 1 blockquote.</p><blockquote><p>Here's a level 2 blockquote.</p><blockquote><p>Here's a level 3 blockquote followed by a line break.</p><br></blockquote></blockquote></blockquote>")

    def test_bold(self):
        self.assertEqual(CONVERT("**Here's some bold text followed by a line break.**  "),
                         "<p><strong>Here's some bold text followed by a line break.</strong></p><br>")
        self.assertEqual(CONVERT("__Here's some bold text followed by a line break.__  "),
                         "<p><strong>Here's some bold text followed by a line break.</strong></p><br>")

    def test_bold_italic(self):
        self.assertEqual(CONVERT("***This is some bold and italic text followed by a line break.***  "),
                         "<p><em><strong>This is some bold and italic text followed by a line break.</strong></em></p><br>")
        self.assertEqual(CONVERT("___This is some bold and italic text followed by a line break.___  "),
                         "<p><em><strong>This is some bold and italic text followed by a line break.</strong></em></p><br>")
        self.assertEqual(CONVERT("**_This is some bold and italic text followed by a line break._**  "),
                         "<p><strong><em>This is some bold and italic text followed by a line break.</em></strong></p><br>")
        self.assertEqual(CONVERT("__*This is some bold and italic text followed by a line break.*__  "),
                         "<p><strong><em>This is some bold and italic text followed by a line break.</em></strong></p><br>")
        self.assertEqual(CONVERT("*__This is some bold and italic text followed by a line break.__*  "),
                         "<p><em><strong>This is some bold and italic text followed by a line break.</strong></em></p><br>")
        self.assertEqual(CONVERT("_**This is some bold and italic text followed by a line break.**_  "),
                         "<p><em><strong>This is some bold and italic text followed by a line break.</strong></em></p><br>")

    def test_code(self):
        self.assertEqual(CONVERT("`This is some text denoted as code, followed by a line break.`  "),
                         "<code>This is some text denoted as code, followed by a line break.</code><br>")
        self.assertEqual(CONVERT("``This is some code containing `backticks`, followed by a line break.``  "),
                         "<code>This is some code containing `backticks`, followed by a line break.</code><br>")

    def test_heading(self):
        self.assertEqual(CONVERT("# This is a level 1 heading followed by a line break. "),
                         "<h1>This is a level 1 heading followed by a line break.</h1>")
        self.assertEqual(CONVERT("## This is a level 2 heading followed by a line break.  "),
                         "<h2>This is a level 2 heading followed by a line break.</h2><br>")
        self.assertEqual(CONVERT("### This is a level 3 heading followed by a line break.   "),
                         "<h3>This is a level 3 heading followed by a line break.</h3><br>")
        self.assertEqual(CONVERT("#### This is a level 4 heading followed by a line break.    "),
                         "<h4>This is a level 4 heading followed by a line break.</h4><br>")
        self.assertEqual(CONVERT("##### This is a level 5 heading followed by a line break.     "),
                         "<h5>This is a level 5 heading followed by a line break.</h5><br>")
        self.assertEqual(CONVERT("###### This is a level 6 heading followed by a line break.      "),
                         "<h6>This is a level 6 heading followed by a line break.</h6><br>")

    def test_image(self):
        self.assertEqual(CONVERT("![This is an image followed by a line break.](image)  "),
                         "<img src=\"image\" alt=\"This is an image followed by a line break.\"><br>")
        self.assertEqual(CONVERT("![This is an image followed by a line break.](image \"This is a title.\")  "),
                         "<img src=\"image\" alt=\"This is an image followed by a line break.\" title=\"This is a title.\"><br>")

    def test_italic(self):
        self.assertEqual(CONVERT("*This is some italic text followed by a line break.*  "),
                         "<p><em>This is some italic text followed by a line break.</em></p><br>")
        self.assertEqual(CONVERT("_This is some italic text followed by a line break._  "),
                         "<p><em>This is some italic text followed by a line break.</em></p><br>")

    def test_link(self):
        self.assertEqual(CONVERT("[This is a link followed by a line break.](link)  "),
                         "<a href=\"link\">This is a link followed by a line break.</a><br>")
        self.assertEqual(CONVERT("[This is a link followed by a line break.](link \"This is a title.\")  "),
                         "<a href=\"link\" title=\"This is a title.\">This is a link followed by a line break.</a><br>")

    def test_ordered_list(self):
        self.assertEqual(CONVERT("1. This is an ordered list item followed by a line break.  "),
                         "<ol><li>This is an ordered list item followed by a line break.</li><br></ol>")
        self.assertEqual(CONVERT("20. This is an ordered list item followed by a line break.  "),
                         "<ol><li>This is an ordered list item followed by a line break.</li><br></ol>")
        self.assertEqual(CONVERT("300. This is an ordered list item followed by a line break.  "),
                         "<ol><li>This is an ordered list item followed by a line break.</li><br></ol>")

    def test_paragraph(self):
        self.assertEqual(CONVERT("Here's a paragraph followed by a line break.  "),
                         "<p>Here's a paragraph followed by a line break.</p><br>")
        self.assertEqual(CONVERT("Here's \na \nmultiline \nparagraph \nfollowed \nby \na \nline \nbreak.     "),
                         "<p>Here's a multiline paragraph followed by a line break.</p><br>")

    def test_unordered_list(self):
        self.assertEqual(CONVERT("- This is an unordered list item followed by a line break.  "),
                         "<ul><li>This is an unordered list item followed by a line break.</li><br></ul>")
        self.assertEqual(CONVERT("* This is an unordered list item followed by a line break.  "),
                         "<ul><li>This is an unordered list item followed by a line break.</li><br></ul>")
        self.assertEqual(CONVERT("+ This is an unordered list item followed by a line break.  "),
                         "<ul><li>This is an unordered list item followed by a line break.</li><br></ul>")

    def test_should_not_be_affected(self):
        self.assertEqual(CONVERT("  "), "")
        self.assertEqual(CONVERT("  This should be a paragraph with no line breaks."),
                         "<p>This should be a paragraph with no line breaks.</p>")
        self.assertEqual(CONVERT("This should be a paragraph with no line breaks. "),
                         "<p>This should be a paragraph with no line breaks.</p>")


class LinkTest(unittest.TestCase):
    def test_empty_link(self):
        self.assertEqual(CONVERT("[]()"), "<p>[]()</p>")
        self.assertEqual(CONVERT("[]( \"\")"), "<p>[]( \"\")</p>")
        self.assertEqual(CONVERT("[This should not be affected.]()"),
                         "<p>[This should not be affected.]()</p>")
        self.assertEqual(CONVERT("[](This should not be affected.)"),
                         "<p>[](This should not be affected.)</p>")
        self.assertEqual(CONVERT("[](\"This should not be affected.\")"),
                         "<p>[](\"This should not be affected.\")</p>")

    def test_link(self):
        self.assertEqual(CONVERT("[This is a link.](Link URL.)"),
                         "<a href=\"Link URL.\">This is a link.</a>")
        self.assertEqual(CONVERT("[     This is a link.     ](     Link URL.     )"),
                         "<a href=\"Link URL.\">This is a link.</a>")
        self.assertEqual(CONVERT("This is a [link](Link URL.) inside a paragraph."),
                         "<p>This is a <a href=\"Link URL.\">link</a> inside a paragraph.</p>")
        self.assertEqual(CONVERT("This is a [     link     ](     Link URL.     ) inside a paragraph."),
                         "<p>This is a <a href=\"Link URL.\">link</a> inside a paragraph.</p>")

    def test_link_with_title(self):
        self.assertEqual(CONVERT("[This is a link.](Link URL. \"This is a title.\")"),
                         "<a href=\"Link URL.\" title=\"This is a title.\">This is a link.</a>")
        self.assertEqual(CONVERT("[     This is a link.     ](     Link URL.    \"This is a title.\"     )"),
                         "<a href=\"Link URL.\" title=\"This is a title.\">This is a link.</a>")
        self.assertEqual(CONVERT("This is a [link](Link URL. \"This is a title.\") inside a paragraph."),
                         "<p>This is a <a href=\"Link URL.\" title=\"This is a title.\">link</a> inside a paragraph.</p>")
        self.assertEqual(CONVERT("This is a [     link     ](     Link URL.     \"This is a title.\"     ) inside a paragraph."),
                         "<p>This is a <a href=\"Link URL.\" title=\"This is a title.\">link</a> inside a paragraph.</p>")

    def test_quick_link(self):
        self.assertEqual(CONVERT("<This should not be affected.>"),
                         "<p><This should not be affected.></p>")
        self.assertEqual(CONVERT("<> This should not be affected."),
                         "<p><> This should not be affected.</p>")
        self.assertEqual(CONVERT("This should not be affected. <>"),
                         "<p>This should not be affected. <></p>")
        self.assertEqual(CONVERT("<http://example.http.link>"),
                         "<a href=\"http://example.http.link\">http://example.http.link</a>")
        self.assertEqual(CONVERT("<https://example.https.link>"),
                         "<a href=\"https://example.https.link\">https://example.https.link</a>")
        self.assertEqual(CONVERT("<https://example.link/with/slashes>"),
                         "<a href=\"https://example.link/with/slashes\">https://example.link/with/slashes</a>")
        self.assertEqual(CONVERT("<https://example.link/with#pounds>"),
                         "<a href=\"https://example.link/with#pounds\">https://example.link/with#pounds</a>")
        self.assertEqual(CONVERT("<https://example.link/with-dashes>"),
                         "<a href=\"https://example.link/with-dashes\">https://example.link/with-dashes</a>")

    def test_quick_email(self):
        self.assertEqual(CONVERT("<This should not be affected.>"),
                         "<p><This should not be affected.></p>")
        self.assertEqual(CONVERT("<> This should not be affected."),
                         "<p><> This should not be affected.</p>")
        self.assertEqual(CONVERT("This should not be affected. <>"),
                         "<p>This should not be affected. <></p>")
        self.assertEqual(CONVERT("<email@domain.example>"),
                         "<a href=\"mailto:email@domain.example\">email@domain.example</a>")
        self.assertEqual(CONVERT("<email@domain-containing-dashes.example>"),
                         "<a href=\"mailto:email@domain-containing-dashes.example\">email@domain-containing-dashes.example</a>")
        self.assertEqual(CONVERT("<email-containing-dashes@domain.example>"),
                         "<a href=\"mailto:email-containing-dashes@domain.example\">email-containing-dashes@domain.example</a>")
        self.assertEqual(CONVERT("<email.containing.dots@domain.example>"),
                         "<a href=\"mailto:email.containing.dots@domain.example\">email.containing.dots@domain.example</a>")
        self.assertEqual(CONVERT("<email+containing+plus+signs@domain.example>"),
                         "<a href=\"mailto:email+containing+plus+signs@domain.example\">email+containing+plus+signs@domain.example</a>")

    def test_reference_link(self):
        self.assertEqual(CONVERT("""
[1]:Link URL.
[1]
        """), "<a href=\"Link URL.\">1</a>")

        self.assertEqual(CONVERT("""
[1]:Link URL.
[This is a link.][1]
        """), "<a href=\"Link URL.\">This is a link.</a>")

        self.assertEqual(CONVERT("""
[1]:Link URL. "This is a title."
[1]
        """), "<a href=\"Link URL.\" title=\"This is a title.\">1</a>")

        self.assertEqual(CONVERT("""
[1]:Link URL. "This is a title."
[This is a link.][1]
        """), "<a href=\"Link URL.\" title=\"This is a title.\">This is a link.</a>")

        self.assertEqual(CONVERT("""
[1]:Link URL. 'This is a title.'
[This is a link.][1]
        """), "<a href=\"Link URL.\" title=\"This is a title.\">This is a link.</a>")

        self.assertEqual(CONVERT("""
[1]:Link URL. (This is a title.)
[This is a link.][1]
        """), "<a href=\"Link URL.\" title=\"This is a title.\">This is a link.</a>")

        self.assertEqual(CONVERT("""
[1]:<Link URL.> "This is a title."
[This is a link.][1]
        """), "<a href=\"Link URL.\" title=\"This is a title.\">This is a link.</a>")

        self.assertEqual(CONVERT("""
[1]:<Link URL.> 'This is a title.'
[This is a link.][1]
        """), "<a href=\"Link URL.\" title=\"This is a title.\">This is a link.</a>")

        self.assertEqual(CONVERT("""
[1]:<Link URL.> (This is a title.)
[This is a link.][1]
        """), "<a href=\"Link URL.\" title=\"This is a title.\">This is a link.</a>")

        self.assertEqual(CONVERT("""
[     1     ]     :     Link URL.
[     This is a link.     ]     [     1     ]
        """), "<a href=\"Link URL.\">This is a link.</a>")

        self.assertEqual(CONVERT("""
[     1     ]     :     Link URL.     "     This is a title.     "
[     This is a link.     ]     [     1     ]
        """), "<a href=\"Link URL.\" title=\"This is a title.\">This is a link.</a>")

        self.assertEqual(CONVERT("""
[     1     ]     :     Link URL.     '     This is a title.     '
[     This is a link.     ]     [     1     ]
        """), "<a href=\"Link URL.\" title=\"This is a title.\">This is a link.</a>")

        self.assertEqual(CONVERT("""
[     1     ]     :     Link URL.     (     This is a title.     )
[     This is a link.     ]     [     1     ]
        """), "<a href=\"Link URL.\" title=\"This is a title.\">This is a link.</a>")

        self.assertEqual(CONVERT("""
[     1     ]     :     <     Link URL.     >     "     This is a title.     "
[     This is a link.     ]     [     1     ]
        """), "<a href=\"Link URL.\" title=\"This is a title.\">This is a link.</a>")

        self.assertEqual(CONVERT("""
[     1     ]     :     <     Link URL.     >     '     This is a title.     '
[     This is a link.     ]     [     1     ]
        """), "<a href=\"Link URL.\" title=\"This is a title.\">This is a link.</a>")

        self.assertEqual(CONVERT("""
[     1     ]     :     <     Link URL.     >     (     This is a title.     )
[     This is a link.     ]     [     1     ]
        """), "<a href=\"Link URL.\" title=\"This is a title.\">This is a link.</a>")


class OrderedListTest(unittest.TestCase):
    def test_empty_ordered_list(self):
        self.assertEqual(CONVERT("1."), "<p>1.</p>")
        self.assertEqual(CONVERT(" 20."), "<p>20.</p>")
        self.assertEqual(CONVERT("  300."), "<p>300.</p>")

        self.assertEqual(CONVERT("1)"), "<p>1)</p>")
        self.assertEqual(CONVERT(" 20)"), "<p>20)</p>")
        self.assertEqual(CONVERT("  300)"), "<p>300)</p>")

    def test_ordered_list(self):
        self.assertEqual(CONVERT("1. This is an ordered list item."),
                         "<ol><li>This is an ordered list item.</li></ol>")
        self.assertEqual(CONVERT("20. This is an ordered list item."),
                         "<ol><li>This is an ordered list item.</li></ol>")
        self.assertEqual(CONVERT("300. This is an ordered list item."),
                         "<ol><li>This is an ordered list item.</li></ol>")

        self.assertEqual(CONVERT("1) This is an ordered list item."),
                         "<ol><li>This is an ordered list item.</li></ol>")
        self.assertEqual(CONVERT("20) This is an ordered list item."),
                         "<ol><li>This is an ordered list item.</li></ol>")
        self.assertEqual(CONVERT("300) This is an ordered list item."),
                         "<ol><li>This is an ordered list item.</li></ol>")

    def test_extra_leading_space(self):
        self.assertEqual(CONVERT("   1. This an ordered list item with 3 extra leading spaces."),
                         "<ol><li>This an ordered list item with 3 extra leading spaces.</li></ol>")
        self.assertEqual(CONVERT("   20. This an ordered list item with 3 extra leading spaces."),
                         "<ol><li>This an ordered list item with 3 extra leading spaces.</li></ol>")
        self.assertEqual(CONVERT("   300. This an ordered list item with 3 extra leading spaces."),
                         "<ol><li>This an ordered list item with 3 extra leading spaces.</li></ol>")

    def test_extra_trailing_space(self):
        self.assertEqual(CONVERT("1. This an ordered list item with 5 extra trailing spaces.     "),
                         "<ol><li>This an ordered list item with 5 extra trailing spaces.</li><br></ol>")
        self.assertEqual(CONVERT("20. This an ordered list item with 5 extra trailing spaces.     "),
                         "<ol><li>This an ordered list item with 5 extra trailing spaces.</li><br></ol>")
        self.assertEqual(CONVERT("300. This an ordered list item with 5 extra trailing spaces.     "),
                         "<ol><li>This an ordered list item with 5 extra trailing spaces.</li><br></ol>")

    def test_extra_space(self):
        self.assertEqual(CONVERT("1.     This a ordered list item with 5 extra spaces.     "),
                         "<ol><li>This a ordered list item with 5 extra spaces.</li><br></ol>")
        self.assertEqual(CONVERT("20.     This a ordered list item with 5 extra spaces.     "),
                         "<ol><li>This a ordered list item with 5 extra spaces.</li><br></ol>")
        self.assertEqual(CONVERT("300.     This a ordered list item with 5 extra spaces.     "),
                         "<ol><li>This a ordered list item with 5 extra spaces.</li><br></ol>")

    def test_multiline(self):
        self.assertEqual(CONVERT("""1. This is a level 1 ordered list item.
                                    2. This is a level 2 ordered list item.
                                    3. This is a level 2 ordered list item."""), "<ol><li>This is a level 1 ordered list item.</li><ol><li>This is a level 2 ordered list item.</li><li>This is a level 2 ordered list item.</li></ol></ol>")

        self.assertEqual(CONVERT("""
8. This is a level 1 ordered list item.
2. This is a level 1 ordered list item.
4. This is a level 1 ordered list item.
        """), "<ol><li>This is a level 1 ordered list item.</li><li>This is a level 1 ordered list item.</li><li>This is a level 1 ordered list item.</li></ol>")

        self.assertEqual(CONVERT("""
1. This is a level 1 ordered list item.
 2. This is a level 2 ordered list item.
  3. This is a level 3 ordered list item.
        """), "<ol><li>This is a level 1 ordered list item.</li><ol><li>This is a level 2 ordered list item.</li><ol><li>This is a level 3 ordered list item.</li></ol></ol></ol>")

        self.assertEqual(CONVERT("""
   1. This is a level 1 ordered list item.
    2. This is a level 2 ordered list item.
     3. This is a level 3 ordered list item.
        """), "<ol><li>This is a level 1 ordered list item.</li><ol><li>This is a level 2 ordered list item.</li><ol><li>This is a level 3 ordered list item.</li></ol></ol></ol>")

        self.assertEqual(CONVERT("""
16. This is a level 1 ordered list item.
    8. This is a level 2 ordered list item.
        4. This is a level 3 ordered list item.
        """), "<ol><li>This is a level 1 ordered list item.</li><ol><li>This is a level 2 ordered list item.</li><ol><li>This is a level 3 ordered list item.</li></ol></ol></ol>")

        self.assertEqual(CONVERT("""
1. This is a level 1 ordered list item.
2. This is a level 1 ordered list item.
                   1. This is a level 2 ordered list item.
3. This is a level 1 ordered list item.
            """), "<ol><li>This is a level 1 ordered list item.</li><li>This is a level 1 ordered list item.</li><ol><li>This is a level 2 ordered list item.</li></ol><li>This is a level 1 ordered list item.</li></ol>")

        self.assertEqual(CONVERT("""
1. This is a level 1 ordered list item.
2. This is a level 1 ordered list item.
3. This is a level 1 ordered list item.
 1. This is a level 2 ordered list item.
 2. This is a level 2 ordered list item.
  3. This is a level 3 ordered list item.
        """), "<ol><li>This is a level 1 ordered list item.</li><li>This is a level 1 ordered list item.</li><li>This is a level 1 ordered list item.</li><ol><li>This is a level 2 ordered list item.</li><li>This is a level 2 ordered list item.</li><ol><li>This is a level 3 ordered list item.</li></ol></ol></ol>")

        self.assertEqual(CONVERT("""
1) This is a level 1 ordered list item.
2) This is a level 1 ordered list item.
3) This is a level 1 ordered list item.
 1) This is a level 2 ordered list item.
 2) This is a level 2 ordered list item.
  3) This is a level 3 ordered list item.
        """), "<ol><li>This is a level 1 ordered list item.</li><li>This is a level 1 ordered list item.</li><li>This is a level 1 ordered list item.</li><ol><li>This is a level 2 ordered list item.</li><li>This is a level 2 ordered list item.</li><ol><li>This is a level 3 ordered list item.</li></ol></ol></ol>")

        self.assertEqual(CONVERT("""
1. This is a level 1 ordered list item.
1. This is a level 1 ordered list item.
1. This is a level 1 ordered list item.
 2. This is a level 2 ordered list item.
 2. This is a level 2 ordered list item.
  3. This is a level 3 ordered list item.
 2. This is a level 2 ordered list item.
 2. This is a level 2 ordered list item.
1. This is a level 1 ordered list item.
1. This is a level 1 ordered list item.
1. This is a level 1 ordered list item.
        """), "<ol><li>This is a level 1 ordered list item.</li><li>This is a level 1 ordered list item.</li><li>This is a level 1 ordered list item.</li><ol><li>This is a level 2 ordered list item.</li><li>This is a level 2 ordered list item.</li><ol><li>This is a level 3 ordered list item.</li></ol><li>This is a level 2 ordered list item.</li><li>This is a level 2 ordered list item.</li></ol><li>This is a level 1 ordered list item.</li><li>This is a level 1 ordered list item.</li><li>This is a level 1 ordered list item.</li></ol>")

        self.assertEqual(CONVERT("""
1. This is a level 1 ordered list item.
2. This is a level 1 ordered list item.
3. This is a level 1 ordered list item.
 1. This is a level 2 ordered list item.
 2. This is a level 2 ordered list item.
  1. This is a level 3 ordered list item.
   1. This is a level 4 ordered list item.
4. This is a level 1 ordered list item.
        """), "<ol><li>This is a level 1 ordered list item.</li><li>This is a level 1 ordered list item.</li><li>This is a level 1 ordered list item.</li><ol><li>This is a level 2 ordered list item.</li><li>This is a level 2 ordered list item.</li><ol><li>This is a level 3 ordered list item.</li><ol><li>This is a level 4 ordered list item.</li></ol></ol></ol><li>This is a level 1 ordered list item.</li></ol>")

        self.assertEqual(CONVERT("""
  1. This is a level 1 list item.
 1. This is a level 1 list item.
1. This is a level 1 list item.
        """), "<ol><li>This is a level 1 list item.</li></ol><ol><li>This is a level 1 list item.</li></ol><ol><li>This is a level 1 list item.</li></ol>")

        self.assertEqual(CONVERT("""
  1. This is a level 1 list item.
 1. This is a level 1 list item.
1. This is a level 1 list item.
1. This is a level 1 list item.
 2. This is a level 2 list item.
  3. This is a level 3 list item.
        """), "<ol><li>This is a level 1 list item.</li></ol><ol><li>This is a level 1 list item.</li></ol><ol><li>This is a level 1 list item.</li><li>This is a level 1 list item.</li><ol><li>This is a level 2 list item.</li><ol><li>This is a level 3 list item.</li></ol></ol></ol>")

    def test_should_not_be_affected(self):
        self.assertEqual(CONVERT("1This should not be affected."),
                         "<p>1This should not be affected.</p>")
        self.assertEqual(CONVERT("1 This should not be affected."),
                         "<p>1 This should not be affected.</p>")
        self.assertEqual(CONVERT("1.This should not be affected."),
                         "<p>1.This should not be affected.</p>")
        self.assertEqual(CONVERT("This should not be affected. 1."),
                         "<p>This should not be affected. 1.</p>")
        self.assertEqual(CONVERT("This 1. should 2. not 3. be 4. affected."),
                         "<p>This 1. should 2. not 3. be 4. affected.</p>")


class ParagraphTest(unittest.TestCase):
    def test_paragraph(self):
        self.assertEqual(CONVERT("This is a paragraph."),
                         "<p>This is a paragraph.</p>")
        self.assertEqual(CONVERT("This is a paragraph.\n\nThis is another paragraph."),
                         "<p>This is a paragraph.</p><p>This is another paragraph.</p>")
        self.assertEqual(CONVERT("This is a paragraph followed by a line break.  \n\nThis is another paragraph."),
                         "<p>This is a paragraph followed by a line break.</p><br><p>This is another paragraph.</p>")

    def test_extra_leading_space(self):
        self.assertEqual(CONVERT("   This is a paragraph with 3 extra leading spaces."),
                         "<p>This is a paragraph with 3 extra leading spaces.</p>")

    def test_extra_trailing_space(self):
        self.assertEqual(CONVERT("This is a paragraph with 5 extra trailing spaces.     "),
                         "<p>This is a paragraph with 5 extra trailing spaces.</p><br>")

    def test_extra_space(self):
        self.assertEqual(CONVERT("   This is a paragraph with 3 extra spaces.   "),
                         "<p>This is a paragraph with 3 extra spaces.</p><br>")

    def test_multiline(self):
        self.assertEqual(CONVERT("This \nis \na \nmultiline \nparagraph."),
                         "<p>This is a multiline paragraph.</p>")

        self.assertEqual(CONVERT("""
This
is
a
multiline
paragraph.
        """), "<p>This is a multiline paragraph.</p>")

        self.assertEqual(CONVERT("""
   This
   is
   a
   multiline
   paragraph.
            """), "<p>This is a multiline paragraph.</p>")

        self.assertEqual(CONVERT("This is a multiline paragraph.  \nIt has a line break."),
                         "<p>This is a multiline paragraph.<br>It has a line break.</p>")


class UnorderedListTest(unittest.TestCase):
    def test_empty_unordered_list(self):
        self.assertEqual(CONVERT("-"), "<p>-</p>")
        self.assertEqual(CONVERT(" -"), "<p>-</p>")
        self.assertEqual(CONVERT("  -"), "<p>-</p>")

    def test_unordered_list(self):
        self.assertEqual(CONVERT("- This is an unordered list item."),
                         "<ul><li>This is an unordered list item.</li></ul>")
        self.assertEqual(CONVERT("* This is an unordered list item."),
                         "<ul><li>This is an unordered list item.</li></ul>")
        self.assertEqual(CONVERT("+ This is an unordered list item."),
                         "<ul><li>This is an unordered list item.</li></ul>")

    def test_extra_leading_space(self):
        self.assertEqual(CONVERT(" - This an unordered list item with an extra leading space."),
                         "<ul><li>This an unordered list item with an extra leading space.</li></ul>")
        self.assertEqual(CONVERT("  - This an unordered list item with 2 extra leading spaces."),
                         "<ul><li>This an unordered list item with 2 extra leading spaces.</li></ul>")
        self.assertEqual(CONVERT("   - This an unordered list item with 3 extra leading spaces."),
                         "<ul><li>This an unordered list item with 3 extra leading spaces.</li></ul>")

    def test_extra_trailing_space(self):
        self.assertEqual(CONVERT("- This an unordered list item with 5 extra trailing spaces.     "),
                         "<ul><li>This an unordered list item with 5 extra trailing spaces.</li><br></ul>")
        self.assertEqual(CONVERT("-- This an unordered list item with 5 extra trailing spaces.     "),
                         "<ul><li>This an unordered list item with 5 extra trailing spaces.</li><br></ul>")
        self.assertEqual(CONVERT("--- This an unordered list item with 5 extra trailing spaces.     "),
                         "<ul><li>This an unordered list item with 5 extra trailing spaces.</li><br></ul>")

    def test_extra_space(self):
        self.assertEqual(CONVERT("-     This a unordered list item with 5 extra spaces.     "),
                         "<ul><li>This a unordered list item with 5 extra spaces.</li><br></ul>")
        self.assertEqual(CONVERT("--     This a unordered list item with 5 extra spaces.     "),
                         "<ul><li>This a unordered list item with 5 extra spaces.</li><br></ul>")
        self.assertEqual(CONVERT("---     This a unordered list item with 5 extra spaces.     "),
                         "<ul><li>This a unordered list item with 5 extra spaces.</li><br></ul>")

    def test_multiline(self):
        self.assertEqual(CONVERT("""- This is a level 1 unordered list item.
                                    - This is a level 2 unordered list item.
                                    - This is a level 2 unordered list item."""), "<ul><li>This is a level 1 unordered list item.</li><ul><li>This is a level 2 unordered list item.</li><li>This is a level 2 unordered list item.</li></ul></ul>")

        self.assertEqual(CONVERT("""
- This is a level 1 unordered list item.
- This is a level 1 unordered list item.
- This is a level 1 unordered list item.
        """), "<ul><li>This is a level 1 unordered list item.</li><li>This is a level 1 unordered list item.</li><li>This is a level 1 unordered list item.</li></ul>")

        self.assertEqual(CONVERT("""
----- This is a level 1 unordered list item item.
----- This is a level 1 unordered list item item.
----- This is a level 1 unordered list item item.
        """), "<ul><li>This is a level 1 unordered list item item.</li><li>This is a level 1 unordered list item item.</li><li>This is a level 1 unordered list item item.</li></ul>")

        self.assertEqual(CONVERT("""
- This is a level 1 unordered list item.
 - This is a level 2 unordered list item.
  - This is a level 3 unordered list item.
        """), "<ul><li>This is a level 1 unordered list item.</li><ul><li>This is a level 2 unordered list item.</li><ul><li>This is a level 3 unordered list item.</li></ul></ul></ul>")

        self.assertEqual(CONVERT("""
- This is a level 1 unordered list item.
 - This is a level 2 unordered list item.
  - This is a level 3 unordered list item.
        """), "<ul><li>This is a level 1 unordered list item.</li><ul><li>This is a level 2 unordered list item.</li><ul><li>This is a level 3 unordered list item.</li></ul></ul></ul>")

        self.assertEqual(CONVERT("""
- This is a level 1 unordered list item.
    - This is a level 2 unordered list item.
        - This is a level 3 unordered list item.
        """), "<ul><li>This is a level 1 unordered list item.</li><ul><li>This is a level 2 unordered list item.</li><ul><li>This is a level 3 unordered list item.</li></ul></ul></ul>")

        self.assertEqual(CONVERT("""
- This is a level 1 unordered list item.
- This is a level 1 unordered list item.
                   - This is a level 2 unordered list item.
- This is a level 1 unordered list item.
            """), "<ul><li>This is a level 1 unordered list item.</li><li>This is a level 1 unordered list item.</li><ul><li>This is a level 2 unordered list item.</li></ul><li>This is a level 1 unordered list item.</li></ul>")

        self.assertEqual(CONVERT("""
- This is a level 1 unordered list item.
- This is a level 1 unordered list item.
- This is a level 1 unordered list item.
 - This is a level 2 unordered list item.
 - This is a level 2 unordered list item.
  - This is a level 3 unordered list item.
        """), "<ul><li>This is a level 1 unordered list item.</li><li>This is a level 1 unordered list item.</li><li>This is a level 1 unordered list item.</li><ul><li>This is a level 2 unordered list item.</li><li>This is a level 2 unordered list item.</li><ul><li>This is a level 3 unordered list item.</li></ul></ul></ul>")

        self.assertEqual(CONVERT("""
- This is a level 1 unordered list item.
* This is a level 1 unordered list item.
+ This is a level 1 unordered list item.
 - This is a level 2 unordered list item.
 * This is a level 2 unordered list item.
  + This is a level 3 unordered list item.
        """), "<ul><li>This is a level 1 unordered list item.</li><li>This is a level 1 unordered list item.</li><li>This is a level 1 unordered list item.</li><ul><li>This is a level 2 unordered list item.</li><li>This is a level 2 unordered list item.</li><ul><li>This is a level 3 unordered list item.</li></ul></ul></ul>")

        self.assertEqual(CONVERT("""
- This is a level 1 unordered list item.
- This is a level 1 unordered list item.
- This is a level 1 unordered list item.
 - This is a level 2 unordered list item.
 - This is a level 2 unordered list item.
  - This is a level 3 unordered list item.
 - This is a level 2 unordered list item.
 - This is a level 2 unordered list item.
- This is a level 1 unordered list item.
- This is a level 1 unordered list item.
- This is a level 1 unordered list item.
        """), "<ul><li>This is a level 1 unordered list item.</li><li>This is a level 1 unordered list item.</li><li>This is a level 1 unordered list item.</li><ul><li>This is a level 2 unordered list item.</li><li>This is a level 2 unordered list item.</li><ul><li>This is a level 3 unordered list item.</li></ul><li>This is a level 2 unordered list item.</li><li>This is a level 2 unordered list item.</li></ul><li>This is a level 1 unordered list item.</li><li>This is a level 1 unordered list item.</li><li>This is a level 1 unordered list item.</li></ul>")

        self.assertEqual(CONVERT("""
- This is a level 1 unordered list item.
- This is a level 1 unordered list item.
- This is a level 1 unordered list item.
 * This is a level 2 unordered list item.
 * This is a level 2 unordered list item.
  + This is a level 3 unordered list item.
 * This is a level 2 unordered list item.
 * This is a level 2 unordered list item.
- This is a level 1 unordered list item.
- This is a level 1 unordered list item.
- This is a level 1 unordered list item.
        """), "<ul><li>This is a level 1 unordered list item.</li><li>This is a level 1 unordered list item.</li><li>This is a level 1 unordered list item.</li><ul><li>This is a level 2 unordered list item.</li><li>This is a level 2 unordered list item.</li><ul><li>This is a level 3 unordered list item.</li></ul><li>This is a level 2 unordered list item.</li><li>This is a level 2 unordered list item.</li></ul><li>This is a level 1 unordered list item.</li><li>This is a level 1 unordered list item.</li><li>This is a level 1 unordered list item.</li></ul>")

        self.assertEqual(CONVERT("""
- This is a level 1 unordered list item.
- This is a level 1 unordered list item.
- This is a level 1 unordered list item.
 - This is a level 2 unordered list item.
 - This is a level 2 unordered list item.
  - This is a level 3 unordered list item.
   - This is a level 4 unordered list item.
- This is a level 1 unordered list item.
        """), "<ul><li>This is a level 1 unordered list item.</li><li>This is a level 1 unordered list item.</li><li>This is a level 1 unordered list item.</li><ul><li>This is a level 2 unordered list item.</li><li>This is a level 2 unordered list item.</li><ul><li>This is a level 3 unordered list item.</li><ul><li>This is a level 4 unordered list item.</li></ul></ul></ul><li>This is a level 1 unordered list item.</li></ul>")

        self.assertEqual(CONVERT("""
  - This is a level 1 list item.
 - This is a level 1 list item.
- This is a level 1 list item.
        """), "<ul><li>This is a level 1 list item.</li></ul><ul><li>This is a level 1 list item.</li></ul><ul><li>This is a level 1 list item.</li></ul>")

        self.assertEqual(CONVERT("""
  - This is a level 1 list item.
 - This is a level 1 list item.
- This is a level 1 list item.
- This is a level 1 list item.
 - This is a level 2 list item.
  - This is a level 3 list item.
        """), "<ul><li>This is a level 1 list item.</li></ul><ul><li>This is a level 1 list item.</li></ul><ul><li>This is a level 1 list item.</li><li>This is a level 1 list item.</li><ul><li>This is a level 2 list item.</li><ul><li>This is a level 3 list item.</li></ul></ul></ul>")

    def test_should_not_be_affected(self):
        self.assertEqual(CONVERT("-This should not be affected."),
                         "<p>-This should not be affected.</p>")
        self.assertEqual(CONVERT("This should not be affected. -"),
                         "<p>This should not be affected. -</p>")
        self.assertEqual(CONVERT("This - should - not - be - affected."),
                         "<p>This - should - not - be - affected.</p>")


if __name__ == '__main__':
    unittest.main()
