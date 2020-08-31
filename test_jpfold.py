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
