#!/usr/bin/env python

import argparse

def get_args():
#Takes three fastq files and return nt and read counts
    parser = argparse.ArgumentParser(description="Add description")
    parser.add_argument("-f1", "--file1", help="filename")
    parser.add_argument("-f2", "--file2", help="filename")
    parser.add_argument("-f3", "--file3", help="filename")
    return parser.parse_args()

args = get_args()

input_file1 = args.file1
input_file2 = args.file2
input_file3 = args.file3

def total_nt(file1, file2, file3):
#finds total number of nucleotides and number of reads for the three fastq files
    line_counter1 = 0
    line_counter2 = 0
    line_counter3 = 0
    nt_counter = 0
    read_counter = 0
    with open(file1) as f1:
        for line in f1:
            line = line.strip()
            line_counter1 += 1
            if line_counter1 % 4 == 0:
                read_counter += 1
                nt_counter += len(line)
    with open(file2) as f2:
        for line in f2:
            line = line.strip()
            line_counter2 += 1
            if line_counter2 % 4 == 0:
                read_counter += 1
                nt_counter += len(line)
    with open(file3) as f1:
        for line in f3:
            line = line.strip()
            line_counter3 += 1
            if line_counter3 % 4 == 0:
                read_counter += 1
                nt_counter += len(line)
    return nt_counter, read_counter

nt_counter, read_counter = total_nt(input_file1, input_file2, input_file3)
print("Nucleotides:" + str(nt_counter))
print("Reads:" + str(read_counter))
