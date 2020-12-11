#!/usr/bin/env python

import argparse
import re
import matplotlib
import matplotlib.pyplot as plt


def get_args():
#Takes fasta file output from Velvet and kmer size, returns assembly stats
    parser = argparse.ArgumentParser(description="Add description")
    parser.add_argument("-f", "--file", help="filename")
    parser.add_argument("-o", "--output", help="output file")
    parser.add_argument("-k", "--kmersize", help="kmer size", type=int)
    return parser.parse_args()

args = get_args()

input_file = args.file
output_file = args.output
kmer_size = args.kmersize

def find_lengths_coverage(input_file, kmer_size):
    headers = []
    length_list = []
    physical_lengths = []
    coverage_list = []
    with open(input_file) as fh:
    #pulls just header lines out of fasta file
        for line in fh:
            line = line.strip()
            if line[0] == ">":
                headers.append(line)
    for element in headers:
    #find lengths and coverage in header lines and appends them to their own lists
    #adjusts lengths to be in base pairs for a given kmer length
        length = re.search("length_([0-9]+)", element).group(1)
        real_length = int(length) + kmer_size - 1
        physical_lengths.append(real_length)
        kmer_coverage = re.search("cov_([0-9]+\.[0-9]+)", element).group(1)
        kmer_coverage = float(kmer_coverage)
        coverage = (kmer_coverage * real_length)/(real_length - kmer_size + 1)
        coverage_list.append(coverage)
    #find stats for lengths and coverage
    number_of_contigs = len(physical_lengths)
    sorted_lengths = sorted(physical_lengths)
    max_contig_length = sorted_lengths[-1]
    total_length = 0
    for element in physical_lengths:
        total_length += int(element)
    mean_length = total_length/number_of_contigs
    sum_cov_length = 0
    #find mean coverage
    for i in range(0,len(coverage_list)):
            cov_length = coverage_list[i] * physical_lengths[i]
            sum_cov_length += cov_length
    mean_coverage = sum_cov_length/total_length
    #calculate n50 using median
    n50_list = []
    for item in sorted_lengths:
        n50_list.extend(item for i in range(item))
    sorted_n50 = sorted(n50_list)
    if len(sorted_n50)%2 == 0:
        median = (sorted_n50[len(sorted_n50)//2] + sorted_n50[len(sorted_n50)//2-1])//2
    else:
        median = sorted_n50[len(sorted_n50)//2]
    n_50 = median
    #create buckets for contig lengths
    contig_buckets = {}
    for i in range(0, max_contig_length + 1, 100):
        contig_buckets.setdefault(i, [])
    for length in physical_lengths:
        rounded_length = (length//100)*100
        contig_buckets[rounded_length].append(length)
    return number_of_contigs, max_contig_length, total_length, mean_length, mean_coverage, n_50, contig_buckets

number_of_contigs, max_contig_length, total_length, mean_length, mean_coverage, n_50, contig_buckets = find_lengths_coverage(input_file, kmer_size)

#writes out stats to output file
oh = open(output_file, "w")
oh.write("number of contigs: " + str(number_of_contigs) + '\n')
oh.write("max contig length: " + str(max_contig_length) + '\n')
oh.write("total length: " + str(total_length) + '\n')
oh.write("mean length: " + str(mean_length) + '\n')
oh.write("mean coverage: " + str(mean_coverage) + '\n')
oh.write("n50: " + str(n_50) + '\n\n')
oh.write('# Contig length' + '  ' + 'Number of contigs in this category' + '\n')
for key, value in contig_buckets.items():
    oh.write(str(key) + "\t" + str(len(value)) + '\n')
oh.close()

#creates list of number of contigs in each bucket for graphing below
number_in_bucket = []
for value in contig_buckets.values():
    number_in_bucket.append(len(value))

#plots distribution of contigs
plt.bar(list(contig_buckets.keys()), number_in_bucket, width = 85)
plt.xlim(left=0, right=30000)
plt.xlabel('Contig Length Binned by 100s')
plt.ylabel('Number of contigs in this category')
plt.title('Distribution of Contig Length')
plt.savefig(str(input_file) + '_new' + '.png')
