#!/usr/bin/env python3

import unittest
import jpfold


class TestJpfold(unittest.TestCase):
    def test_count_east_asian_string_width(self):
        self.assertEqual(0, jpfold.count_east_asian_string_width(""))
        self.assertEqual(0, jpfold.count_east_asian_string_width("\r\n"))
        self.assertEqual(3, jpfold.count_east_asian_string_width("123"))
        self.assertEqual(6, jpfold.count_east_asian_string_width("あいう"))
        self.assertEqual(4, jpfold.count_east_asian_string_width("漢字"))
        self.assertEqual(6, jpfold.count_east_asian_string_width("①②③"))
        self.assertEqual(4, jpfold.count_east_asian_string_width("ﾆｺﾆｺ"))
        self.assertEqual(2, jpfold.count_east_asian_string_width("☺"))

    def test_calc_position_by_width_en(self):
        self.assertRaises(AssertionError, lambda: jpfold.calc_position_by_width("", -1))
        self.assertEqual(0, jpfold.calc_position_by_width("", 0))
        self.assertEqual(0, jpfold.calc_position_by_width("", 1))
        self.assertEqual(0, jpfold.calc_position_by_width("1", 0))
        self.assertEqual(1, jpfold.calc_position_by_width("1", 1))
        self.assertEqual(1, jpfold.calc_position_by_width("1", 2))
        self.assertEqual(0, jpfold.calc_position_by_width("12", 0))
        self.assertEqual(1, jpfold.calc_position_by_width("12", 1))
        self.assertEqual(2, jpfold.calc_position_by_width("12", 2))
        self.assertEqual(0, jpfold.calc_position_by_width("\r\n", 0))
        self.assertEqual(2, jpfold.calc_position_by_width("\r\n", 1))

    def test_calc_position_by_width_jp(self):
        self.assertEqual(0, jpfold.calc_position_by_width("あ", 0))
        self.assertEqual(0, jpfold.calc_position_by_width("あ", 1))
        self.assertEqual(1, jpfold.calc_position_by_width("あ", 2))
        self.assertEqual(1, jpfold.calc_position_by_width("あ", 3))
        self.assertEqual(0, jpfold.calc_position_by_width("あい", 0))
        self.assertEqual(0, jpfold.calc_position_by_width("あい", 1))
        self.assertEqual(1, jpfold.calc_position_by_width("あい", 2))
        self.assertEqual(1, jpfold.calc_position_by_width("あい", 3))
        self.assertEqual(2, jpfold.calc_position_by_width("あい", 4))
        self.assertEqual(2, jpfold.calc_position_by_width("あい", 5))
        self.assertEqual(2, jpfold.calc_position_by_width("あい", 6))
        self.assertEqual(5, jpfold.calc_position_by_width("こんにちは", 10))
        self.assertEqual(3, jpfold.calc_position_by_width("こんにちは", 6))

    def test_one_line_break(self):
        self.assertRaises(AssertionError, lambda: jpfold.one_line_break("こんにちは", 0))
        origline, nextline = jpfold.one_line_break("こんにちは", 10)
        self.assertEqual(origline, "こんにちは")
        self.assertEqual(nextline, "")
        origline, nextline = jpfold.one_line_break("こんにちは", 6)
        self.assertEqual(origline, "こんに")
        self.assertEqual(nextline, "ちは")
        origline, nextline = jpfold.one_line_break("こんにちは", 5)
        self.assertEqual(origline, "こん")
        self.assertEqual(nextline, "にちは")
        origline, nextline = jpfold.one_line_break("こんにちは", 4)
        self.assertEqual(origline, "こん")
        self.assertEqual(nextline, "にちは")
        origline, nextline = jpfold.one_line_break("こんにちは", 2)
        self.assertEqual(origline, "こ")
        self.assertEqual(nextline, "んにちは")

    def test_one_line_break_with_kinsoku(self):
        origline, nextline = jpfold.one_line_break("今日、晴れる？", 4)
        self.assertEqual(origline, "今日、")
        self.assertEqual(nextline, "晴れる？")
        origline, nextline = jpfold.one_line_break("晴れる？", 6)
        self.assertEqual(origline, "晴れる？")
        self.assertEqual(nextline, "")
        origline, nextline = jpfold.one_line_break("チェック", 2)
        self.assertEqual(origline, "チェッ")
        self.assertEqual(nextline, "ク")
        origline, nextline = jpfold.one_line_break("それ「みかん」", 6)
        self.assertEqual(origline, "それ")
        self.assertEqual(nextline, "「みかん」")
        origline, nextline = jpfold.one_line_break("「みかん」", 2)
        self.assertEqual(origline, "「み")
        self.assertEqual(nextline, "かん」")
        origline, nextline = jpfold.one_line_break("「「「", 2)
        self.assertEqual(origline, "「「「")
        self.assertEqual(nextline, "")
        origline, nextline = jpfold.one_line_break("」」」", 2)
        self.assertEqual(origline, "」」」")
        self.assertEqual(nextline, "")
        origline, nextline = jpfold.one_line_break("This is a pen.", 4)
        self.assertEqual(origline, "This ")
        self.assertEqual(nextline, "is a pen.")

    def test_one_line_break_with_quoted_line(self):
        origline, nextline = jpfold.one_line_break("> 今日、晴れる？", 4)
        self.assertEqual(origline, "> 今日、晴れる？")
        self.assertEqual(nextline, "")
        origline, nextline = jpfold.one_line_break("＞> 今日、晴れる？", 4)
        self.assertEqual(origline, "＞> 今日、晴れる？")
        self.assertEqual(nextline, "")
        origline, nextline = jpfold.one_line_break("  > 今日、晴れる？", 4)
        self.assertEqual(origline, "  > ")
        self.assertEqual(nextline, "  今日、晴れる？")

    def test_one_line_break_with_english_wordwrap(self):
        origline, nextline = jpfold.one_line_break("The quick brown fox jumps over the lazy dog.", 10)
        self.assertEqual(origline, "The quick ")
        self.assertEqual(nextline, "brown fox jumps over the lazy dog.")
        origline, nextline = jpfold.one_line_break("The quick brown fox jumps over the lazy dog.", 8)
        self.assertEqual(origline, "The ")
        self.assertEqual(nextline, "quick brown fox jumps over the lazy dog.")
        origline, nextline = jpfold.one_line_break("The quick brown fox jumps over the lazy dog.", 6)
        self.assertEqual(origline, "The ")
        self.assertEqual(nextline, "quick brown fox jumps over the lazy dog.")
        origline, nextline = jpfold.one_line_break("Co.,Ltd.", 2)
        self.assertEqual(origline, "Co.,")
        self.assertEqual(nextline, "Ltd.")

    def test_one_line_break_with_number_wordwrap(self):
        origline, nextline = jpfold.one_line_break("12345です", 3)
        self.assertEqual(origline, "12345")
        self.assertEqual(nextline, "です")
        origline, nextline = jpfold.one_line_break("\\12345です", 3)
        self.assertEqual(origline, "\\12345")
        self.assertEqual(nextline, "です")
        origline, nextline = jpfold.one_line_break("\\12,345です", 3)
        self.assertEqual(origline, "\\12,345")
        self.assertEqual(nextline, "です")
        origline, nextline = jpfold.one_line_break("\\12,345-です", 3)
        self.assertEqual(origline, "\\12,345-")
        self.assertEqual(nextline, "です")

    def test_is_position_within_english_word(self):
        self.assertFalse(jpfold.is_position_within_english_word("", 0))
        self.assertRaises(AssertionError, lambda: jpfold.is_position_within_english_word("", 1))
        self.assertFalse(jpfold.is_position_within_english_word("The quick brown", 0))
        self.assertTrue(jpfold.is_position_within_english_word("The quick brown", 1))
        self.assertTrue(jpfold.is_position_within_english_word("The quick brown", 2))
        self.assertFalse(jpfold.is_position_within_english_word("The quick brown", 3))
        self.assertFalse(jpfold.is_position_within_english_word("The quick brown", 4))
        self.assertTrue(jpfold.is_position_within_english_word("The quick brown", 5))
        self.assertTrue(jpfold.is_position_within_english_word("I'm Jhon.", 1))
        self.assertTrue(jpfold.is_position_within_english_word("I'm Jhon.", 2))
        self.assertFalse(jpfold.is_position_within_english_word("I'm Jhon.", 3))
        self.assertFalse(jpfold.is_position_within_english_word("I'm Jhon.", 4))
        self.assertTrue(jpfold.is_position_within_english_word("I'm Jhon.", 5))
        self.assertTrue(jpfold.is_position_within_english_word("co-founder", 1))
        self.assertTrue(jpfold.is_position_within_english_word("co-founder", 2))
        self.assertFalse(jpfold.is_position_within_english_word("co-founder", 3))
        self.assertTrue(jpfold.is_position_within_english_word("co-founder", 4))
        self.assertFalse(jpfold.is_position_within_english_word("あいう", 0))
        self.assertFalse(jpfold.is_position_within_english_word("あいう", 1))
        self.assertFalse(jpfold.is_position_within_english_word("あいう", 2))
        self.assertFalse(jpfold.is_position_within_english_word("あいう", 3))
        self.assertFalse(jpfold.is_position_within_english_word("桜並木", 0))
        self.assertFalse(jpfold.is_position_within_english_word("桜並木", 1))
        self.assertFalse(jpfold.is_position_within_english_word("桜並木", 2))
        self.assertFalse(jpfold.is_position_within_english_word("桜並木", 3))
        self.assertFalse(jpfold.is_position_within_english_word(" 'fo' ", 1))
        self.assertTrue(jpfold.is_position_within_english_word(" 'fo' ", 2))
        self.assertTrue(jpfold.is_position_within_english_word(" 'fo' ", 3))
        self.assertTrue(jpfold.is_position_within_english_word(" 'fo' ", 4))
        self.assertFalse(jpfold.is_position_within_english_word(" 'fo' ", 5))

    def test_one_line_break_with_indent(self):
        origline, nextline = jpfold.one_line_break("  今日、晴れる？", 4)
        self.assertEqual(origline, "  今")
        self.assertEqual(nextline, "  日、晴れる？")
        origline, nextline = jpfold.one_line_break("・今日、晴れる？", 4)
        self.assertEqual(origline, "・今")
        self.assertEqual(nextline, "  日、晴れる？")
        origline, nextline = jpfold.one_line_break("  ・今日、晴れる？", 10)
        self.assertEqual(origline, "  ・今日、")
        self.assertEqual(nextline, "    晴れる？")

    def test_one_line_break_for_url(self):
        origline, nextline = jpfold.one_line_break("https://www.example.jp/", 10)
        self.assertEqual(origline, "https://www.example.jp/")
        self.assertEqual(nextline, "")
        origline, nextline = jpfold.one_line_break("こんにちはhttps://www.example.jp/", 10)
        self.assertEqual(origline, "こんにちは")
        self.assertEqual(nextline, "https://www.example.jp/")
        origline, nextline = jpfold.one_line_break("mailto:test@example.com", 7)
        self.assertEqual(origline, "mailto:test@example.com")
        self.assertEqual(nextline, "")
        origline, nextline = jpfold.one_line_break("こんにちはmailto:test@example.com", 10)
        self.assertEqual(origline, "こんにちは")
        self.assertEqual(nextline, "mailto:test@example.com")

    def test_one_line_break_for_mailaddress(self):
        origline, nextline = jpfold.one_line_break("test@example.com", 7)
        self.assertEqual(origline, "test@example.com")
        self.assertEqual(nextline, "")
        origline, nextline = jpfold.one_line_break("こんにちはmailto:test@example.com", 10)
        self.assertEqual(origline, "こんにちは")
        self.assertEqual(nextline, "mailto:test@example.com")

    def test_one_line_break_complex_case(self):
        # 英文ワードラップの結果、行末禁則が出現するケース
        origline, nextline = jpfold.one_line_break("これは「JavaScript」です", 12)
        self.assertEqual(origline, "これは")
        self.assertEqual(nextline, "「JavaScript」です")
        # 行末に複数種類の行頭禁則文字
        origline, nextline = jpfold.one_line_break("'foo' 、 'foo.'", 5)
        self.assertEqual(origline, "'foo' 、 ")
        self.assertEqual(nextline, "'foo.'")
        origline, nextline = jpfold.one_line_break("\"fo\" ", 3)
        self.assertEqual(origline, "\"fo\" ")
        self.assertEqual(nextline, "")

    def test_tab_to_space(self):
        self.assertRaises(AssertionError, lambda: jpfold.tab_to_space("abcdef", 0))
        self.assertEqual(jpfold.tab_to_space("abcdef", 4),     "abcdef")
        self.assertEqual(jpfold.tab_to_space("abcdef", 8),     "abcdef")
        self.assertEqual(jpfold.tab_to_space("\tef", 4),       "    ef")
        self.assertEqual(jpfold.tab_to_space("ab\tef", 4),     "ab  ef")
        self.assertEqual(jpfold.tab_to_space("\t\tef", 4),     "        ef")
        self.assertEqual(jpfold.tab_to_space("ab\tcd\tef", 4), "ab  cd  ef")
        self.assertEqual(jpfold.tab_to_space("abc\td\tef", 4), "abc d   ef")
        self.assertEqual(jpfold.tab_to_space("abcd\tef", 4),   "abcd    ef")
        self.assertEqual(jpfold.tab_to_space("a\tc\tef", 1),   "a c ef")

    def test_kinsoku_char(self):
        self.assertFalse(jpfold.is_linehead_konsoku("あ"))
        self.assertTrue(jpfold.is_linehead_konsoku("。"))
        self.assertTrue(jpfold.is_linehead_konsoku("」"))
        self.assertTrue(jpfold.is_linehead_konsoku(")"))
        self.assertTrue(jpfold.is_linehead_konsoku("。"))
        self.assertTrue(jpfold.is_linehead_konsoku("？"))
        self.assertTrue(jpfold.is_linehead_konsoku("!"))
        self.assertTrue(jpfold.is_linehead_konsoku("っ"))
        self.assertFalse(jpfold.is_linetail_konsoku("あ"))
        self.assertTrue(jpfold.is_linetail_konsoku("「"))
        self.assertTrue(jpfold.is_linetail_konsoku("("))
        self.assertRaises(AssertionError, lambda: jpfold.is_linehead_konsoku(""))
        self.assertRaises(AssertionError, lambda: jpfold.is_linetail_konsoku(""))
        self.assertRaises(AssertionError, lambda: jpfold.is_linehead_konsoku("ああ"))
        self.assertRaises(AssertionError, lambda: jpfold.is_linetail_konsoku("ああ"))

    def test_get_indent_for_line(self):
        self.assertEqual(jpfold.get_indent_for_line(""),         "")
        self.assertEqual(jpfold.get_indent_for_line(" "),        " ")
        self.assertEqual(jpfold.get_indent_for_line("  "),       "  ")
        self.assertEqual(jpfold.get_indent_for_line("\t"),       "\t")
        self.assertEqual(jpfold.get_indent_for_line(" \t"),      " \t")
        self.assertEqual(jpfold.get_indent_for_line(" \t "),     " \t ")
        self.assertEqual(jpfold.get_indent_for_line("・"),       "  ")
        self.assertEqual(jpfold.get_indent_for_line("・ "),      "   ")
        self.assertEqual(jpfold.get_indent_for_line(" -abc"),    "  ")
        self.assertEqual(jpfold.get_indent_for_line(" - abc"),   "   ")
        self.assertEqual(jpfold.get_indent_for_line(" * abc"),   "   ")
        self.assertEqual(jpfold.get_indent_for_line(" ・"),      "   ")
        self.assertEqual(jpfold.get_indent_for_line("  ・あい"), "    ")
        self.assertEqual(jpfold.get_indent_for_line("  ・ あ"),  "     ")
        self.assertEqual(jpfold.get_indent_for_line("  ※ あ"),  "     ")
        self.assertEqual(jpfold.get_indent_for_line("1."),       "  ")
        self.assertEqual(jpfold.get_indent_for_line("2. "),      "   ")
        self.assertEqual(jpfold.get_indent_for_line(" 3. "),     "    ")
        self.assertEqual(jpfold.get_indent_for_line("  A. "),    "     ")
        self.assertEqual(jpfold.get_indent_for_line("  (A) "),   "      ")
        self.assertEqual(jpfold.get_indent_for_line("  [A] "),   "      ")
        self.assertEqual(jpfold.get_indent_for_line("  <A> "),   "      ")
        self.assertEqual(jpfold.get_indent_for_line("  A) "),    "     ")
        self.assertEqual(jpfold.get_indent_for_line("  )A "),    "  ")
        self.assertEqual(jpfold.get_indent_for_line("abc"),      "")
        self.assertEqual(jpfold.get_indent_for_line("A "),       "")
        self.assertEqual(jpfold.get_indent_for_line("123"),      "")
        self.assertEqual(jpfold.get_indent_for_line("()"),       "")
        self.assertEqual(jpfold.get_indent_for_line("() "),      "")
        self.assertEqual(jpfold.get_indent_for_line(")("),       "")
        self.assertEqual(jpfold.get_indent_for_line("."),        "")
        self.assertEqual(jpfold.get_indent_for_line(". "),       "")
        self.assertEqual(jpfold.get_indent_for_line("-----"),       "")

    def test_is_quoted_line(self):
        self.assertFalse(jpfold.is_quoted_line(""))
        self.assertFalse(jpfold.is_quoted_line("a"))
        self.assertFalse(jpfold.is_quoted_line("a>"))
        self.assertFalse(jpfold.is_quoted_line("あ>"))
        self.assertTrue(jpfold.is_quoted_line(">"))
        self.assertTrue(jpfold.is_quoted_line("> "))
        self.assertTrue(jpfold.is_quoted_line(">> "))
        self.assertTrue(jpfold.is_quoted_line("> > "))
        self.assertTrue(jpfold.is_quoted_line("＞"))
        self.assertTrue(jpfold.is_quoted_line(">＞"))
        self.assertTrue(jpfold.is_quoted_line(">＞ >"))
        self.assertTrue(jpfold.is_quoted_line("> ＞ > "))
