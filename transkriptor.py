#!/usr/bin/env python3

import argparse
import sys
import itertools
import json
from pprint import pprint

def read_lut(path):
    data=json.loads(open(path).read())
    return(data['glyphes'],data['substitutions'])


def print_table(glypheset, width=10):
    for i in range(int(len(glypheset)/width)+1):
        output = []
        for j in range(width):
            output.append(glypheset)
        print(''.join(output))            

    #pprint(set['glyphes'])
    

def substitute(text, set):
    for s in set.keys():
        text = text.replace(s, set[s])
    return text


def transcribe(text, glypheset, start=True, strict=False, fallback=False, remove_doubles=False):
    out_text = []
    if start:
        out_text.append(glypheset['SRT'])

    for char in text:
        try:
            out_text.append(glypheset[char])
        except KeyError:
            if strict:
                pass
            else:
                out_text.append(char)

    if start:
        out_text.append(glypheset['STP'])

    output = "".join(out_text)

    if remove_doubles:
        output = ''.join(c[0] for c in itertools.groupby(output))
    return output


def main():
    parser = argparse.ArgumentParser(
        description="Since unicode is fun you now can render whatever you want in some old glyphes")
    parser.add_argument(
        "-i", help="Input mandatory if you don't pipe something into the script.", type=str)
    parser.add_argument("-s", "--glypheset",
                        help="path to glypheset as json", type=str)
    parser.add_argument(
        "-e", help="Don't show start/end glyphes.", action="store_true")
    parser.add_argument(
        "-x", "--strict", help="Strict mode, pass unknown characters.", action="store_true")
    # parser.add_argument(
    #    "-b", "--fallback", help = "Fallback mode, use less historically correct glypes as fallback.", action = "store_true")
    parser.add_argument("-d", "--no_double",
                        help = "Dont show double letters.", action = "store_true")
    parser.add_argument(
        "-t", "--table", help = "Print table of given glypheset", action = "store_true")

    args=parser.parse_args()

    start=not args.e
    strict=args.strict
    # fallback = args.fallback
    no_double=args.no_double

    (set,substitutions) = read_lut(args.glypheset)
    
    if args.table:
        print_table(set) 
        return

    if args.i:
        text=args.i
    else:
        text=sys.stdin.read()

    text=text.lower()

    text=substitute(text, substitutions)
    print(transcribe(text,set,start,strict,False,no_double))
    # print(parse(text, start, strict, fallback, no_double, glypheset))

if __name__ == "__main__":
    main()
