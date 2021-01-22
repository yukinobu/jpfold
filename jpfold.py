#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
from typing import TextIO
import unicodedata


LINE_BREAK: str = "\r\n"
LINEHEAD_KINSOKU = "!%),.:;?]}¢°’”‰′″℃、。々〉》」』】〕ぁぃぅぇぉっゃゅょゎ゛゜ゝゞァィゥェォッャュョヮヵヶ・ーヽヾ！％），．：；？］｝｡｣､･ｧｨｩｪｫｬｭｮｯｰﾞﾟ￠"
LINETAIL_KINSOKU = "$([\{£¥‘“〈《「『【〔＄（［｛｢￡￥"


def main(args: argparse.Namespace) -> int:
    infile:  TextIO = sys.stdin  if args.input=="-"  else open(args.input, "r",encoding="utf-8")
    outfile: TextIO = sys.stdout if args.output=="-" else open(args.output,"w",encoding="utf-8")
    retval = jpfold(infile, outfile, args)
    outfile.close()
    infile.close()
    return retval


def jpfold(io_in: TextIO, io_out: TextIO, args: argparse.Namespace) -> int:
    """jpfold のメイン関数

    Parameters:
    ----------
    io_in: TextIO
        入力用のI/O
    io_out: TextIO
        出力用のI/O
    args: argparse.Namespace
        コマンドライン引数

    Returns:
    ----------
    int
        成功なら 0 を返す
    """
    for line in io_in:
        origline, nextline = one_line_break(line, args.width)
        while nextline != "":
            io_out.write(origline+LINE_BREAK)
            origline, nextline = one_line_break(nextline, args.width)
        io_out.write(origline)
    return 0


def one_line_break(origline: str, target_width: int):
    """テキストを所定の幅で改行する

    Parameters:
    ----------
    origline: str
        改行すべき元の行
    target_width: int
        一行の幅、すなわち改行すべき位置

    Returns:
    ----------
    origline: str
        改行された元の行
    nextline: str
        改行によって作成された次の行
    """
    assert 1 <= target_width, "target_width は 1 以上である必要があります"
    origline_len: int = len(origline)
    break_pos: int = calc_position_by_width(origline, target_width)
    while break_pos < origline_len and is_linehead_konsoku(origline[break_pos]):
        break_pos += 1
    while 0 < break_pos and is_linetail_konsoku(origline[break_pos-1]):
        break_pos -= 1
    if break_pos == 0:
        while is_linehead_konsoku(origline[break_pos]) or is_linetail_konsoku(origline[break_pos]):
            break_pos += 1
        break_pos += 1
    return origline[0:break_pos], origline[break_pos:]


def calc_position_by_width(text: str, target_width: int) -> int:
    """文字列が特定の幅になる位置を返す

    Parameters:
    ----------
    text: str
        入力文字列
    target_width: int
        ターゲットとなる幅

    Returns:
    ----------
    position: int
        strがwidth幅となる位置
    """
    # very naive implement: O(textlen^2)
    assert 0 <= target_width, "target_width は 0 以上である必要があります"
    position: int = 0
    textlen: int = len(text)
    while position < textlen:
        current_width: int = count_east_asian_string_width(text[0:position])
        if(target_width <= current_width):
            break
        position += 1
    return position


def count_east_asian_string_width(val: str) -> int:
    """文字列の幅を数えて返す

    Parameters:
    ----------
    val: str
        入力文字列

    Returns:
    ----------
    width: int
        入力文字列の幅
    """
    width:  int = 0
    vallen: int = len(val)
    cursor: int = 0
    while cursor < vallen:
        c: str = val[cursor:cursor+1]
        w: str = unicodedata.east_asian_width(c)
        if c == "\r" or c == "\n":
            pass
        else:
            width += east_asian_width_symbol_to_number(w)
        cursor += 1
    return width


def east_asian_width_symbol_to_number(symbol: str) -> int:
    """unicodedata.east_asian_width が返す記号を数字幅に変換

    Parameters:
    ----------
    symbol: str
        unicodedata.east_asian_width が返す記号

    Returns:
    ----------
    number: int
        幅。半角なら1、全角なら2を基本
    """
    # https://water2litter.net/rum/post/python_unicodedata_east_asian_width/
    if symbol == "F":
        return 2
    elif symbol == "H":
        return 1
    elif symbol == "W":
        return 2
    elif symbol == "Na":
        return 1
    elif symbol == "A":
        return 2
    elif symbol == "N":
        return 2
    else:
        assert False, "不明なeast_asian_widthシンボル: "+symbol


def tab_to_space(line: str, tabsize: int) -> str:
    assert 1 <= tabsize, "tabsize は 1 以上である必要があります"
    retstr:    str = ""
    linelen:   int = len(line)
    cursor:    int = 0
    retcursor: int = 0
    while cursor < linelen:
        c: str = line[cursor:cursor+1]
        if c == "\t":
            mod: int = retcursor % tabsize
            if mod == 0:
                retstr += (" " * tabsize)
                retcursor += tabsize
            else:
                retstr += (" " * (tabsize-mod))
                retcursor += (tabsize-mod)
        else:
            retstr += c
            retcursor += 1
        cursor += 1
    return retstr


def is_linehead_konsoku(char: str) -> bool:
    assert len(char) == 1, "charは1文字でなくてはなりません"
    return char in LINEHEAD_KINSOKU


def is_linetail_konsoku(char: str) -> bool:
    assert len(char) == 1, "charは1文字でなくてはなりません"
    return char in LINETAIL_KINSOKU


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="日本語整形ツール")
    parser.add_argument("-w", "--width",  type=int, default=66,  help="自動改行の幅を指定します（デフォルトは66）")
    parser.add_argument("-i", "--input",  type=str, default="-", help="入力ファイル名を指定します（デフォルトは標準入力）")
    parser.add_argument("-o", "--output", type=str, default="-", help="出力ファイル名を指定します（デフォルトは標準出力）")
    parser.add_argument("--no-linehead-kinsoku", action="store_false", help="行頭禁則処理を抑止します")
    parser.add_argument("--no-linetail-kinsoku", action="store_false", help="行末禁則処理を抑止します")
    parser.add_argument("--no-separate-kinsoku", action="store_false", help="分割禁則処理を抑止します")
    parser.add_argument("--no-indent",           action="store_false", help="改行時のインデントを抑止します")
    parser.add_argument("--no-listtail-indent",  action="store_false", help="箇条書き途中で改行時のぶら下げインデントを抑止します")
    args = parser.parse_args()
    sys.exit( main(args) )
