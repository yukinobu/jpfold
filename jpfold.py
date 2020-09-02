#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
from typing import TextIO
import unicodedata


LINE_BREAK: str = "\r\n"


def main(args: argparse.Namespace) -> int:
    infile:  TextIO = sys.stdin  if args.input=="-"  else open(args.input, "r",encoding="utf-8")
    outfile: TextIO = sys.stdout if args.output=="-" else open(args.output,"w",encoding="utf-8")
    retval = jpfold(infile, outfile, args)
    outfile.close()
    infile.close()
    return retval


def jpfold(io_in: TextIO, io_out: TextIO, args: argparse.Namespace) -> int:
    for line in io_in:
        origline, nextline = one_line_break(line, args.width)
        while nextline != "":
            io_out.write(origline+LINE_BREAK)
            origline, nextline = one_line_break(nextline, args.width)
        io_out.write(origline)
    return 0


def one_line_break(origline: str, width: int):
    nextline: str = ""
    if(count_east_asian_string_width(origline) <= width):
        return origline, ""
    else:
        pos: int = calc_position_by_width(origline, width)
        return origline[0:pos-1], origline[pos:]


def calc_position_by_width(text: str, width: int) -> int:
    # very naive implement
    position: int = 0
    while count_east_asian_string_width(text[0:position]) <= width:
        position += 1
    return position


def count_east_asian_string_width(val: str) -> int:
    width:  int = 0
    vallen: int = len(val)
    cursor: int = 0
    while cursor < vallen:
        # https://water2litter.net/rum/post/python_unicodedata_east_asian_width/
        c: int = val[cursor:cursor+1]
        w: str = unicodedata.east_asian_width(c)
        if c == "\r" or c == "\n":
            pass
        elif w == "F":
            width += 2;
        elif w == "H":
            width += 1;
        elif w == "W":
            width += 2;
        elif w == "Na":
            width += 1;
        elif w == "A":
            width += 2;
        elif w == "N":
            width += 2;
        else:
            assert 0
        cursor += 1
    return width


def tab_to_space(line: str, tabsize: int) -> str:
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "日本語整形ツール")
    parser.add_argument("-w", "--width",  type=int, default=66)
    parser.add_argument("-i", "--input",  type=str, default="-")
    parser.add_argument("-o", "--output", type=str, default="-")
    args = parser.parse_args()
    sys.exit( main(args) )
