#!/usr/bin/env python

import argparse
import re

def get_args():
#Parses bitwise flag of BAM file to find and count mapped vs. unmapped reads
    parser = argparse.ArgumentParser(description="Defines arguments to run script with")
    parser.add_argument("-f", "--file", help="filename")
    return parser.parse_args()

args = get_args()
input_file = args.file


def mapped_reads(input_file):
    mapped = 0
    not_mapped = 0
    with open(input_file) as fh:
        for line in fh:
            if line[0] != "@":
                flag = re.search("\t([0-99]+)\t", line).group(1)
                flag = int(flag)
                if ((flag & 4) != 4) and ((flag & 256) != 256):
                    mapped += 1
                if ((flag & 4) == 4) and ((flag & 256) != 256):
                    not_mapped += 1
    return mapped, not_mapped

mapped, not_mapped = mapped_reads(input_file)
print("Mapped:", str(mapped))
print("Not mapped:", str(not_mapped))
