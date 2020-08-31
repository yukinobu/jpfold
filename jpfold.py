#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
from typing import TextIO


def main(args: argparse.Namespace) -> int:
    infile:  TextIO = sys.stdin  if args.input=='-'  else open(args.input, 'r',encoding='utf-8')
    outfile: TextIO = sys.stdout if args.output=='-' else open(args.output,'w',encoding='utf-8')
    for line in infile:
        outfile.write(line)
    infile.close()
    outfile.close()
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = '日本語整形ツール')
    parser.add_argument('-w', '--width',  type=int, default=66)
    parser.add_argument('-i', '--input',  type=str, default='-')
    parser.add_argument('-o', '--output', type=str, default='-')
    args = parser.parse_args()
    sys.exit( main(args) )
