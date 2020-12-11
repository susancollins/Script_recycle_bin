#!/usr/bin/env python

import argparse
import re

def get_args():
#Create arguments to run script in command line
    parser = argparse.ArgumentParser(description="checks bitwise flag of SAM file to determine strandedness")
    parser.add_argument("-f", "--file", help="filename")
    return parser.parse_args()

args = get_args()
input_file = args.file


def mapped_reads(input_file):
    R1_reverse = 0
    R2_reverse = 0
    mapped = 0
    not_mapped = 0
    with open(input_file) as fh:
        for line in fh:
            if line[0] != "@":
                flag = line.strip().split()[1]
                flag = int(flag)
                if (flag & 4) != 4:
                    mapped += 1
                    if (flag & 16) == 16 and (flag & 64) == 64:
                        R1_reverse += 1
                    elif (flag & 16) == 16 and (flag & 64) != 64:
                        R2_reverse += 1
                elif (flag & 4) == 4:
                    not_mapped += 1
    return R1_reverse, R2_reverse, mapped, not_mapped

reverse, not_reverse, mapped, not_mapped = mapped_reads(input_file)
print("R1 reverse:", str(reverse))
print("R2 reverse:", str(not_reverse))
print("Mapped:", str(mapped))
print("Not mapped:", str(not_mapped))
