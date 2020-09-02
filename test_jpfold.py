#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import jpfold


class TestJpfold(unittest.TestCase):
    def test_count_east_asian_string_width(self):
        self.assertEqual( 0, jpfold.count_east_asian_string_width("") )
        self.assertEqual( 0, jpfold.count_east_asian_string_width("\r\n") )
        self.assertEqual( 3, jpfold.count_east_asian_string_width("123") )
        self.assertEqual( 6, jpfold.count_east_asian_string_width("あいう") )
        self.assertEqual( 4, jpfold.count_east_asian_string_width("漢字") )
        self.assertEqual( 6, jpfold.count_east_asian_string_width("①②③") )
        self.assertEqual( 4, jpfold.count_east_asian_string_width("ﾆｺﾆｺ") )
        self.assertEqual( 2, jpfold.count_east_asian_string_width("☺") )

    def test_calc_position_by_width_en(self):
        self.assertEqual( 0, jpfold.calc_position_by_width("", 0) )
        self.assertEqual( 0, jpfold.calc_position_by_width("", 1) )
        self.assertEqual( 0, jpfold.calc_position_by_width("1", 0) )
        self.assertEqual( 1, jpfold.calc_position_by_width("1", 1) )
        self.assertEqual( 1, jpfold.calc_position_by_width("1", 2) )
        self.assertEqual( 0, jpfold.calc_position_by_width("12", 0) )
        self.assertEqual( 1, jpfold.calc_position_by_width("12", 1) )
        self.assertEqual( 2, jpfold.calc_position_by_width("12", 2) )

    def test_calc_position_by_width_jp(self):
        self.assertEqual( 0, jpfold.calc_position_by_width("あ", 0) )
        self.assertEqual( 1, jpfold.calc_position_by_width("あ", 1) )
        self.assertEqual( 1, jpfold.calc_position_by_width("あ", 2) )
        self.assertEqual( 1, jpfold.calc_position_by_width("あ", 3) )
        self.assertEqual( 0, jpfold.calc_position_by_width("あい", 0) )
        self.assertEqual( 1, jpfold.calc_position_by_width("あい", 1) )
        self.assertEqual( 1, jpfold.calc_position_by_width("あい", 2) )
        self.assertEqual( 2, jpfold.calc_position_by_width("あい", 3) )
        self.assertEqual( 2, jpfold.calc_position_by_width("あい", 4) )
        self.assertEqual( 2, jpfold.calc_position_by_width("あい", 5) )
        self.assertEqual( 2, jpfold.calc_position_by_width("あい", 6) )
        self.assertEqual( 5, jpfold.calc_position_by_width("こんにちは", 10) )
        self.assertEqual( 3, jpfold.calc_position_by_width("こんにちは", 6) )

    def test_one_line_break(self):
        origline, nextline = jpfold.one_line_break("こんにちは", 10)
        self.assertEqual( origline, "こんにちは" )
        self.assertEqual( nextline, "" )
        origline, nextline = jpfold.one_line_break("こんにちは", 6)
        self.assertEqual( origline, "こんに" )
        self.assertEqual( nextline, "ちは" )
        origline, nextline = jpfold.one_line_break("こんにちは", 5)
        self.assertEqual( origline, "こんに" )
        self.assertEqual( nextline, "ちは" )
        origline, nextline = jpfold.one_line_break("こんにちは", 4)
        self.assertEqual( origline, "こん" )
        self.assertEqual( nextline, "にちは" )
        origline, nextline = jpfold.one_line_break("こんにちは", 2)
        self.assertEqual( origline, "こ" )
        self.assertEqual( nextline, "んにちは" )

    def test_tab_to_space(self):
        self.assertEqual( jpfold.tab_to_space("abcdef",4),     "abcdef" )
        self.assertEqual( jpfold.tab_to_space("abcdef",8),     "abcdef" )
        self.assertEqual( jpfold.tab_to_space("\tef",4),       "    ef" )
        self.assertEqual( jpfold.tab_to_space("ab\tef",4),     "ab  ef" )
        self.assertEqual( jpfold.tab_to_space("\t\tef",4),     "        ef" )
        self.assertEqual( jpfold.tab_to_space("ab\tcd\tef",4), "ab  cd  ef" )
        self.assertEqual( jpfold.tab_to_space("abc\td\tef",4), "abc d   ef" )
        self.assertEqual( jpfold.tab_to_space("abcd\tef",4),   "abcd    ef" )
