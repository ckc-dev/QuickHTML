"""
Unit tests for QuickHTML, sorted alphabetically.
"""
import unittest
import importlib.util
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
        self.assertEqual(CONVERT("     >This a blockquote with extra leading space."),
                         "<blockquote><p>This a blockquote with extra leading space.</p></blockquote>")
        self.assertEqual(CONVERT("     >>This a blockquote with extra leading space."),
                         "<blockquote><p>This a blockquote with extra leading space.</p></blockquote>")
        self.assertEqual(CONVERT("     >>>This a blockquote with extra leading space."),
                         "<blockquote><p>This a blockquote with extra leading space.</p></blockquote>")

    def test_extra_trailing_space(self):
        self.assertEqual(CONVERT(">This a blockquote with extra trailing space.     "),
                         "<blockquote><p>This a blockquote with extra trailing space.</p><br></blockquote>")
        self.assertEqual(CONVERT(">>This a blockquote with extra trailing space.     "),
                         "<blockquote><p>This a blockquote with extra trailing space.</p><br></blockquote>")
        self.assertEqual(CONVERT(">>>This a blockquote with extra trailing space.     "),
                         "<blockquote><p>This a blockquote with extra trailing space.</p><br></blockquote>")

    def test_extra_space(self):
        self.assertEqual(CONVERT(">     This a blockquote with extra space.     "),
                         "<blockquote><p>This a blockquote with extra space.</p><br></blockquote>")
        self.assertEqual(CONVERT(">>     This a blockquote with extra space.     "),
                         "<blockquote><p>This a blockquote with extra space.</p><br></blockquote>")
        self.assertEqual(CONVERT(">>>     This a blockquote with extra space.     "),
                         "<blockquote><p>This a blockquote with extra space.</p><br></blockquote>")

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
        >>>>>This is a level 1 blockquote.
        >>>>>>>>This is a level 2 blockquote.
        >>>>>>>>>>>This is a level 3 blockquote.
        """), "<blockquote><p>This is a level 1 blockquote.</p><blockquote><p>This is a level 2 blockquote.</p><blockquote><p>This is a level 3 blockquote.</p></blockquote></blockquote></blockquote>")

        self.assertEqual(CONVERT("""\
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

    def test_should_not_be_affected(self):
        self.assertEqual(CONVERT("This should not be affected. >"),
                         "<p>This should not be affected. ></p>")
        self.assertEqual(CONVERT("This > should > not > be > affected."),
                         "<p>This > should > not > be > affected.</p>")


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

    def test_extra_space(self):
        self.assertEqual(CONVERT("`     This is some text denoted as code.     `"),
                         "<code>This is some text denoted as code.</code>")
        self.assertEqual(CONVERT("This is a `     word     ` denoted as code."),
                         "<p>This is a <code>word</code> denoted as code.</p>")
        self.assertEqual(CONVERT("These are some letters denoted as `     c     `o`     d     `e."),
                         "<p>These are some letters denoted as <code>c</code>o<code>d</code>e.</p>")
        self.assertEqual(CONVERT("``     This is some code containing `backticks`.     ``"),
                         "<code>This is some code containing `backticks`.</code>")

    def test_should_not_be_affected(self):
        self.assertEqual(CONVERT("`This should not be affected."),
                         "<p>`This should not be affected.</p>")
        self.assertEqual(CONVERT("This should not be affected.`"),
                         "<p>This should not be affected.`</p>")


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

    def test_italic_bold(self):
        self.assertEqual(CONVERT("***This is some italic bold text.***"),
                         "<p><em><strong>This is some italic bold text.</strong></em></p>")
        self.assertEqual(CONVERT("___This is some italic bold text.___"),
                         "<p><em><strong>This is some italic bold text.</strong></em></p>")
        self.assertEqual(CONVERT("**_This is some italic bold text._**"),
                         "<p><strong><em>This is some italic bold text.</em></strong></p>")
        self.assertEqual(CONVERT("__*This is some italic bold text.*__"),
                         "<p><strong><em>This is some italic bold text.</em></strong></p>")
        self.assertEqual(CONVERT("*__This is some italic bold text.__*"),
                         "<p><em><strong>This is some italic bold text.</strong></em></p>")
        self.assertEqual(CONVERT("_**This is some italic bold text.**_"),
                         "<p><em><strong>This is some italic bold text.</strong></em></p>")

        self.assertEqual(CONVERT("This is an italic bold ***word***."),
                         "<p>This is an italic bold <em><strong>word</strong></em>.</p>")
        self.assertEqual(CONVERT("This is an italic bold ___word___."),
                         "<p>This is an italic bold <em><strong>word</strong></em>.</p>")
        self.assertEqual(CONVERT("This is an italic bold **_word_**."),
                         "<p>This is an italic bold <strong><em>word</em></strong>.</p>")
        self.assertEqual(CONVERT("This is an italic bold __*word*__."),
                         "<p>This is an italic bold <strong><em>word</em></strong>.</p>")
        self.assertEqual(CONVERT("This is an italic bold *__word__*."),
                         "<p>This is an italic bold <em><strong>word</strong></em>.</p>")
        self.assertEqual(CONVERT("This is an italic bold _**word**_."),
                         "<p>This is an italic bold <em><strong>word</strong></em>.</p>")

        self.assertEqual(CONVERT("These are some i***t***a***l***i***c*** a***n***d ***b***o***l***d letters."),
                         "<p>These are some i<em><strong>t</strong></em>a<em><strong>l</strong></em>i<em><strong>c</strong></em> a<em><strong>n</strong></em>d <em><strong>b</strong></em>o<em><strong>l</strong></em>d letters.</p>")
        self.assertEqual(CONVERT("These are some i___t___a___l___i___c___ a___n___d ___b___o___l___d letters."),
                         "<p>These are some i<em><strong>t</strong></em>a<em><strong>l</strong></em>i<em><strong>c</strong></em> a<em><strong>n</strong></em>d <em><strong>b</strong></em>o<em><strong>l</strong></em>d letters.</p>")
        self.assertEqual(CONVERT("These are some i**_t_**a**_l_**i**_c_** a**_n_**d **_b_**o**_l_**d letters."),
                         "<p>These are some i<strong><em>t</em></strong>a<strong><em>l</em></strong>i<strong><em>c</em></strong> a<strong><em>n</em></strong>d <strong><em>b</em></strong>o<strong><em>l</em></strong>d letters.</p>")
        self.assertEqual(CONVERT("These are some i__*t*__a__*l*__i__*c*__ a__*n*__d __*b*__o__*l*__d letters."),
                         "<p>These are some i<strong><em>t</em></strong>a<strong><em>l</em></strong>i<strong><em>c</em></strong> a<strong><em>n</em></strong>d <strong><em>b</em></strong>o<strong><em>l</em></strong>d letters.</p>")
        self.assertEqual(CONVERT("These are some i*__t__*a*__l__*i*__c__* a*__n__*d *__b__*o*__l__*d letters."),
                         "<p>These are some i<em><strong>t</strong></em>a<em><strong>l</strong></em>i<em><strong>c</strong></em> a<em><strong>n</strong></em>d <em><strong>b</strong></em>o<em><strong>l</strong></em>d letters.</p>")
        self.assertEqual(CONVERT("These are some i_**t**_a_**l**_i_**c**_ a_**n**_d _**b**_o_**l**_d letters."),
                         "<p>These are some i<em><strong>t</strong></em>a<em><strong>l</strong></em>i<em><strong>c</strong></em> a<em><strong>n</strong></em>d <em><strong>b</strong></em>o<em><strong>l</strong></em>d letters.</p>")
        self.assertEqual(CONVERT("These are some i***t***a___l___i**_c_** a__*n*__d *__b__*o_**l**_d letters."),
                         "<p>These are some i<em><strong>t</strong></em>a<em><strong>l</strong></em>i<strong><em>c</em></strong> a<strong><em>n</em></strong>d <em><strong>b</strong></em>o<em><strong>l</strong></em>d letters.</p>")

        self.assertEqual(CONVERT("***Some*** ***italic*** ***and*** ***bold*** ***words.***"),
                         "<p><em><strong>Some</strong></em> <em><strong>italic</strong></em> <em><strong>and</strong></em> <em><strong>bold</strong></em> <em><strong>words.</strong></em></p>")
        self.assertEqual(CONVERT("___Some___ ___italic___ ___and___ ___bold___ ___words.___"),
                         "<p><em><strong>Some</strong></em> <em><strong>italic</strong></em> <em><strong>and</strong></em> <em><strong>bold</strong></em> <em><strong>words.</strong></em></p>")
        self.assertEqual(CONVERT("**_Some_** **_italic_** **_and_** **_bold_** **_words._**"),
                         "<p><strong><em>Some</em></strong> <strong><em>italic</em></strong> <strong><em>and</em></strong> <strong><em>bold</em></strong> <strong><em>words.</em></strong></p>")
        self.assertEqual(CONVERT("__*Some*__ __*italic*__ __*and*__ __*bold*__ __*words.*__"),
                         "<p><strong><em>Some</em></strong> <strong><em>italic</em></strong> <strong><em>and</em></strong> <strong><em>bold</em></strong> <strong><em>words.</em></strong></p>")
        self.assertEqual(CONVERT("*__Some__* *__italic__* *__and__* *__bold__* *__words.__*"),
                         "<p><em><strong>Some</strong></em> <em><strong>italic</strong></em> <em><strong>and</strong></em> <em><strong>bold</strong></em> <em><strong>words.</strong></em></p>")
        self.assertEqual(CONVERT("_**Some**_ _**italic**_ _**and**_ _**bold**_ _**words.**_"),
                         "<p><em><strong>Some</strong></em> <em><strong>italic</strong></em> <em><strong>and</strong></em> <em><strong>bold</strong></em> <em><strong>words.</strong></em></p>")

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

    def test_code(self):
        self.assertEqual(CONVERT("\`This should not be affected.\`"),
                         "<p>`This should not be affected.`</p>")
        self.assertEqual(CONVERT("\`\`This should not be affected.\`\`"),
                         "<p>``This should not be affected.``</p>")

    def test_italic(self):
        self.assertEqual(CONVERT("\*This should not be affected.\*"),
                         "<p>*This should not be affected.*</p>")
        self.assertEqual(CONVERT("\_This should not be affected.\_"),
                         "<p>_This should not be affected._</p>")

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
        self.assertEqual(CONVERT("!\[This should not be affected.](not an image)"),
                         "<p>![This should not be affected.](not an image)</p>")
        self.assertEqual(CONVERT("!\[This should not be affected.](not an image \"Not a Title.\")"),
                         "<p>![This should not be affected.](not an image \"Not a Title.\")</p>")

    def test_line_break(self):
        self.assertEqual(CONVERT("Here's a paragraph followed by two spaces instead of a line break. \ "),
                         "<p>Here's a paragraph followed by two spaces instead of a line break.  </p>")

    def test_link(self):
        self.assertEqual(CONVERT("\[This should not be affected.](link)"),
                         "<p>[This should not be affected.](link)</p>")
        self.assertEqual(CONVERT("\[This should not be affected.](not a link \"Not a title.\")"),
                         "<p>[This should not be affected.](not a link \"Not a title.\")</p>")

    def test_ordered_list(self):
        self.assertEqual(CONVERT("\\1. This should not be affected."),
                         "<p>1. This should not be affected.</p>")
        self.assertEqual(CONVERT("\\20. This should not be affected."),
                         "<p>20. This should not be affected.</p>")
        self.assertEqual(CONVERT("\\300. This should not be affected."),
                         "<p>300. This should not be affected.</p>")

    def test_escaped_paragraph(self):
        self.assertEqual(CONVERT("\T\h\i\s\ \s\h\o\\u\l\d\ \\n\o\\t\ \\b\e\ \\a\\f\\f\e\c\\t\e\d\."),
                         "<p>This should not be affected.</p>")

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
        self.assertEqual(CONVERT("    #### This is a level 4 heading with 4 extra leading spaces."),
                         "<h4>This is a level 4 heading with 4 extra leading spaces.</h4>")
        self.assertEqual(CONVERT("     ##### This is a level 5 heading with 5 extra leading spaces."),
                         "<h5>This is a level 5 heading with 5 extra leading spaces.</h5>")
        self.assertEqual(CONVERT("      ###### This is a level 6 heading with 6 extra leading spaces."),
                         "<h6>This is a level 6 heading with 6 extra leading spaces.</h6>")

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
        self.assertEqual(CONVERT("![This is an image.](image)"),
                         "<img src=\"image\" alt=\"This is an image.\">")
        self.assertEqual(CONVERT("![     This is an image.     ](     image     )"),
                         "<img src=\"image\" alt=\"This is an image.\">")
        self.assertEqual(CONVERT("This is an image ![image](image) inside a paragraph."),
                         "<p>This is an image <img src=\"image\" alt=\"image\"> inside a paragraph.</p>")
        self.assertEqual(CONVERT("This is an image ![     image     ](     image     ) inside a paragraph."),
                         "<p>This is an image <img src=\"image\" alt=\"image\"> inside a paragraph.</p>")

    def test_image_with_title(self):
        self.assertEqual(CONVERT("![This is an image.](image \"Here's a Title.\")"),
                         "<img src=\"image\" alt=\"This is an image.\" title=\"Here's a Title.\">")
        self.assertEqual(CONVERT("![     This is an image.     ](     image     \"Here's a Title.\"     )"),
                         "<img src=\"image\" alt=\"This is an image.\" title=\"Here's a Title.\">")
        self.assertEqual(CONVERT("This is an image ![image](image \"Here's a title.\") inside a paragraph."),
                         "<p>This is an image <img src=\"image\" alt=\"image\" title=\"Here's a title.\"> inside a paragraph.</p>")
        self.assertEqual(CONVERT("This is an image ![     image     ](     image     \"Here's a title.\"     ) inside a paragraph."),
                         "<p>This is an image <img src=\"image\" alt=\"image\" title=\"Here's a title.\"> inside a paragraph.</p>")


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
        self.assertEqual(CONVERT("![This is an image followed by a line break.](image \"Here's a Title.\")  "),
                         "<img src=\"image\" alt=\"This is an image followed by a line break.\" title=\"Here's a Title.\"><br>")

    def test_italic(self):
        self.assertEqual(CONVERT("*This is some italic text followed by a line break.*  "),
                         "<p><em>This is some italic text followed by a line break.</em></p><br>")
        self.assertEqual(CONVERT("_This is some italic text followed by a line break._  "),
                         "<p><em>This is some italic text followed by a line break.</em></p><br>")

    def test_link(self):
        self.assertEqual(CONVERT("[This is a link followed by a line break.](link)  "),
                         "<a href=\"link\">This is a link followed by a line break.</a><br>")
        self.assertEqual(CONVERT("[This is a link followed by a line break.](link \"Here's a title.\")  "),
                         "<a href=\"link\" title=\"Here's a title.\">This is a link followed by a line break.</a><br>")

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
                         "<p>This should be a paragraph with no line breaks. </p>")


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
        self.assertEqual(CONVERT("[This is a link.](link)"),
                         "<a href=\"link\">This is a link.</a>")
        self.assertEqual(CONVERT("[     This is a link.     ](     link     )"),
                         "<a href=\"link\">This is a link.</a>")
        self.assertEqual(CONVERT("This is a [link](link) inside a paragraph."),
                         "<p>This is a <a href=\"link\">link</a> inside a paragraph.</p>")
        self.assertEqual(CONVERT("This is a [     link     ](     link     ) inside a paragraph."),
                         "<p>This is a <a href=\"link\">link</a> inside a paragraph.</p>")

    def test_link_with_title(self):
        self.assertEqual(CONVERT("[This is a link.](link \"Here's a title.\")"),
                         "<a href=\"link\" title=\"Here's a title.\">This is a link.</a>")
        self.assertEqual(CONVERT("[     This is a link.     ](     link     \"Here's a title.\"     )"),
                         "<a href=\"link\" title=\"Here's a title.\">This is a link.</a>")
        self.assertEqual(CONVERT("This is a [link](link \"Here's a title.\") inside a paragraph."),
                         "<p>This is a <a href=\"link\" title=\"Here's a title.\">link</a> inside a paragraph.</p>")
        self.assertEqual(CONVERT("This is a [     link     ](     link     \"Here's a title.\"     ) inside a paragraph."),
                         "<p>This is a <a href=\"link\" title=\"Here's a title.\">link</a> inside a paragraph.</p>")


class OrderedListTest(unittest.TestCase):
    def test_empty_ordered_list(self):
        self.assertEqual(CONVERT("1."), "<p>1.</p>")
        self.assertEqual(CONVERT(" 20."), "<p>20.</p>")
        self.assertEqual(CONVERT("  300."), "<p>300.</p>")

    def test_ordered_list(self):
        self.assertEqual(CONVERT("1. This is an ordered list item."),
                         "<ol><li>This is an ordered list item.</li></ol>")
        self.assertEqual(CONVERT("20. This is an ordered list item."),
                         "<ol><li>This is an ordered list item.</li></ol>")
        self.assertEqual(CONVERT("300. This is an ordered list item."),
                         "<ol><li>This is an ordered list item.</li></ol>")

    def test_extra_leading_space(self):
        self.assertEqual(CONVERT("     1. This an ordered list item with extra leading space."),
                         "<ol><li>This an ordered list item with extra leading space.</li></ol>")
        self.assertEqual(CONVERT("      20. This an ordered list item with extra leading space."),
                         "<ol><li>This an ordered list item with extra leading space.</li></ol>")
        self.assertEqual(CONVERT("       300. This an ordered list item with extra leading space."),
                         "<ol><li>This an ordered list item with extra leading space.</li></ol>")

    def test_extra_trailing_space(self):
        self.assertEqual(CONVERT("1. This an ordered list item with extra trailing space.     "),
                         "<ol><li>This an ordered list item with extra trailing space.</li><br></ol>")
        self.assertEqual(CONVERT("20. This an ordered list item with extra trailing space.     "),
                         "<ol><li>This an ordered list item with extra trailing space.</li><br></ol>")
        self.assertEqual(CONVERT("300. This an ordered list item with extra trailing space.     "),
                         "<ol><li>This an ordered list item with extra trailing space.</li><br></ol>")

    def test_extra_space(self):
        self.assertEqual(CONVERT("1.     This a ordered list item with extra space.     "),
                         "<ol><li>This a ordered list item with extra space.</li><br></ol>")
        self.assertEqual(CONVERT("20.     This a ordered list item with extra space.     "),
                         "<ol><li>This a ordered list item with extra space.</li><br></ol>")
        self.assertEqual(CONVERT("300.     This a ordered list item with extra space.     "),
                         "<ol><li>This a ordered list item with extra space.</li><br></ol>")

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

        1024. This is a level 1 ordered list item.
        1. This is a level 1 ordered list item.
        256. This is a level 1 ordered list item.

        """), "<ol><li>This is a level 1 ordered list item.</li><li>This is a level 1 ordered list item.</li><li>This is a level 1 ordered list item.</li></ol>")

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
        self.assertEqual(CONVERT("     This is a paragraph with extra leading space."),
                         "<p>This is a paragraph with extra leading space.</p>")
        self.assertEqual(CONVERT("This is a paragraph with extra trailing space (a line break).     "),
                         "<p>This is a paragraph with extra trailing space (a line break).</p><br>")
        self.assertEqual(CONVERT("This \nis \na \nmultiline \nparagraph."),
                         "<p>This is a multiline paragraph.</p>")
        self.assertEqual(CONVERT("This is a multiline paragraph.  \nIt has a line break."),
                         "<p>This is a multiline paragraph.<br>It has a line break.</p>")
        self.assertEqual(CONVERT("This is a paragraph.\n\nThis is another paragraph."),
                         "<p>This is a paragraph.</p><p>This is another paragraph.</p>")
        self.assertEqual(CONVERT("This is a paragraph followed by a line break.  \n\nThis is another paragraph."),
                         "<p>This is a paragraph followed by a line break.</p><br><p>This is another paragraph.</p>")


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
        self.assertEqual(CONVERT("     - This an unordered list item with extra leading space."),
                         "<ul><li>This an unordered list item with extra leading space.</li></ul>")
        self.assertEqual(CONVERT("      - This an unordered list item with extra leading space."),
                         "<ul><li>This an unordered list item with extra leading space.</li></ul>")
        self.assertEqual(CONVERT("       - This an unordered list item with extra leading space."),
                         "<ul><li>This an unordered list item with extra leading space.</li></ul>")

    def test_extra_trailing_space(self):
        self.assertEqual(CONVERT("- This an unordered list item with extra trailing space.     "),
                         "<ul><li>This an unordered list item with extra trailing space.</li><br></ul>")
        self.assertEqual(CONVERT("-- This an unordered list item with extra trailing space.     "),
                         "<ul><li>This an unordered list item with extra trailing space.</li><br></ul>")
        self.assertEqual(CONVERT("--- This an unordered list item with extra trailing space.     "),
                         "<ul><li>This an unordered list item with extra trailing space.</li><br></ul>")

    def test_extra_space(self):
        self.assertEqual(CONVERT("-     This a unordered list item with extra space.     "),
                         "<ul><li>This a unordered list item with extra space.</li><br></ul>")
        self.assertEqual(CONVERT("--     This a unordered list item with extra space.     "),
                         "<ul><li>This a unordered list item with extra space.</li><br></ul>")
        self.assertEqual(CONVERT("---     This a unordered list item with extra space.     "),
                         "<ul><li>This a unordered list item with extra space.</li><br></ul>")

    def test_multiline(self):
        self.assertEqual(CONVERT("""- This is a level 1 unordered list item.
                                    - This is a level 1 unordered list item.
                                    - This is a level 1 unordered list item."""), "<ul><li>This is a level 1 unordered list item.</li><ul><li>This is a level 1 unordered list item.</li><li>This is a level 1 unordered list item.</li></ul></ul>")

        self.assertEqual(CONVERT("""
        - This is a level 1 unordered list item.
        - This is a level 1 unordered list item.
        - This is a level 1 unordered list item.
        """), "<ul><li>This is a level 1 unordered list item.</li><li>This is a level 1 unordered list item.</li><li>This is a level 1 unordered list item.</li></ul>")

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

    def test_should_not_be_affected(self):
        self.assertEqual(CONVERT("-This should not be affected."),
                         "<p>-This should not be affected.</p>")
        self.assertEqual(CONVERT("This should not be affected. -"),
                         "<p>This should not be affected. -</p>")
        self.assertEqual(CONVERT("This - should - not - be - affected."),
                         "<p>This - should - not - be - affected.</p>")


if __name__ == '__main__':
    unittest.main()
