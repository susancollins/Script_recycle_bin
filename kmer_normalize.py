#!/usr/bin/env python

import argparse

def get_args():
#Takes an input FASTQ file and normalizes kmer coverage to chosen coverage limit, outputs new normalized FASTQ file
    parser = argparse.ArgumentParser(description="add desciption")
    parser.add_argument("-f", "--file", help="filename", required=True)
    parser.add_argument("-c", "--coveragelimit", help="kmer coverage limit", type=int)
    parser.add_argument("-o", "--outputfile", help="output file")
    return parser.parse_args()

args = get_args()

input_file = args.file
coverage_limit = args.coveragelimit
output = args.outputfile

def normalize(input_file, coverage_limit, output):
#normalized kmer coverage of input and outputs new fastq file
    with open(input_file) as fh:
        k_mer_size = 15
        line_counter = 1
        record_list = []
        kmer_occurence = {}
        for line in fh:
            line = line.strip()
            if line_counter%4 == 0:
                #stores one record in memory
                record_list.append(line)
                line_counter += 1
                number_kmers = 101 - k_mer_size + 1
                start = 0
                end = k_mer_size
                read = record_list[1]
                while (start) < number_kmers:
                    #kmerizes read
                    kmer = read[start:end]
                    if kmer in kmer_occurence:
                        kmer_occurence[kmer] += 1
                    else:
                        kmer_occurence.setdefault(read[start:end], 1)
                    start += 1
                    end += 1
                kmer_coverage = []
                start = 0
                end = k_mer_size
                while (start) < number_kmers:
                    #kmerizes read again and adds kmer coverage to a list
                    kmer = read[start:end]
                    kmer_coverage.append(kmer_occurence[kmer])
                    start += 1
                    end += 1
                sorted_coverage = sorted(kmer_coverage)
                length = len(sorted_coverage)
                if len(sorted_coverage)%2 == 0:
                    #finds median kmer coverage
                    median = (sorted_coverage[length//2] + sorted_coverage[length//2-1])/2
                else:
                    median = sorted_coverage[length//2]
                if median <= coverage_limit:
                    #if median is below threshold, record is written to output file
                    with open(output, "a") as oh:
                        oh.write(record_list[0] + "\n" + record_list[1] + "\n" + record_list[2] + "\n" + record_list[3] + "\n")
                record_list = []
                kmer_coverage = []
            else:
                record_list.append(line)
                line_counter += 1

normalize(input_file, coverage_limit, output)
