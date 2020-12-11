#!/usr/bin/env python

import matplotlib
import matplotlib.pyplot as plt
import argparse

def get_args():
#Takes FASTQ file and k-mer size, k-merizes data and returns k-mer spectra and plot
    parser = argparse.ArgumentParser(description="Populates a dictionary of kmers and their counts")
    parser.add_argument("-f", "--file", help="filename")
    parser.add_argument("-k", "--kmersize", help="kmer size", type=int)
    return parser.parse_args()

args = get_args()

my_file = args.file
k_mer_size = args.kmersize

def populate_dict(my_file, k_mer_size):
#This populates a dictionary with kmers as keys and their counts as values   
    k_mer_dict = {}
    number_kmers = 101 - k_mer_size + 1
    line_counter = 0
    with open(my_file) as fh:
        for line in fh:
            line = line.strip()
            line_counter += 1
            if (line_counter-2)%4 == 0:
                start = 0
                end = k_mer_size
                while (start+1) <= number_kmers:
                    kmer = line[start:end]
                    if kmer in k_mer_dict:
                        k_mer_dict[kmer] += 1
                    else:
                        k_mer_dict.setdefault(line[start:end], 1)
                    start += 1
                    end += 1
    return k_mer_dict

k_mer_dict = populate_dict(my_file, k_mer_size)

def second_dict(k_mer_dict):
#This populates a dictionary with the number of kmers as keys and their frequency as values
    summary_dict = {}
    for key, value in k_mer_dict.items():
        if value in summary_dict:
            summary_dict[value] += 1
        else:
            summary_dict.setdefault(k_mer_dict[key], 1)
    return summary_dict

summary_dict = second_dict(k_mer_dict)


def tab_sep(dict):
#This gives a tab seperated ouput of the keys and values from a dictionary
    print('kmer frequency' + '  ' + 'number of kmers in this category')
    for key, value in sorted(dict.items()):
        print(key, value, sep=' ')

tab_format = tab_sep(summary_dict)

#Plots a bar graph of kmer frequency vs. number of kmers with that frequency 
plt.bar(list(summary_dict.keys()), list(summary_dict.values()), align='center')
plt.yscale("log")
plt.xlim(left=0, right=10000)
plt.xlabel('k-mer frequency')
plt.ylabel('Number of k-mers in this category')
plt.title('K-mer Summary for K-mer Size ' + str(k_mer_size))
plt.show()
