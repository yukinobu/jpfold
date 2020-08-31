#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
from typing import TextIO

def main(args: argparse.Namespace) -> int:
    infile: TextIO = sys.stdin if args.input=='-' else open(args.input)
    for line in infile:
        print(line.rstrip())
    infile.close()
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = '日本語整形ツール')
    parser.add_argument('-w', '--width', type=int, default=66)
    parser.add_argument('-i', '--input', type=str, default='-')
    parser.add_argument('-o', '--output', type=str, default='-')
    args = parser.parse_args()
    sys.exit( main(args) )
