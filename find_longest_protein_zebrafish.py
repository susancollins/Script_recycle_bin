#!/usr/bin/env python

import argparse
import re

def get_args():
#Takes Ensembl peptide FASTA and table of gene IDs, return longest protein per gene. If multiple longest proteins, returns first one encountered
    parser = argparse.ArgumentParser(description="Defines arguments to run script with")
    parser.add_argument("-f", "--file", help="filename")
    parser.add_argument("-g", "--gene", help="gene id filename")
    parser.add_argument("-o", "--output", help = "output file")
    return parser.parse_args()

args = get_args()
input_file = args.file
gene_file = args.gene
output_file = args.output


def pull_gene_ids(gene_file):
#Creates dictionary of gene ids from mart_export table
    gene_ids = {}
    with open(gene_file, "r") as gh:
        line_counter = 0
        for line in gh:
            line = line.strip()
            splt_lines = re.split('\t', line)
            if line_counter != 0:
                gene_ids.setdefault(splt_lines[0], ['', ''])
            line_counter +=1
    for key in gene_ids.keys():
        if re.search("([a-zA-Z]+[0-9]+\t)", key) is not None:
            gene_ids.pop(key)
    return gene_ids

gene_ids = pull_gene_ids(gene_file)


def match_genes(input_file):
#Creates dictionary with header lines as keys and sequences as values
    records = {}
    with open(input_file) as fh:
        for line in fh:
            line = line.strip()
            if line[0] == '>':
                header = line
                records.setdefault(header, "")
            else:
                records[header] += str(line)
    return records

records = match_genes(input_file)


def long_protein(records, gene_ids):
#Compares records to gene ids to find longest protein for each gene
    for key in records.keys():
        match_id = re.search("gene:([a-zA-Z]+[0-9]+)", key).group(1)
        if match_id in gene_ids:
            if len(records[key]) > len(gene_ids[match_id][1]):
                new_d = {match_id: [key, records[key]]}
                gene_ids.update(new_d)
    return gene_ids

gene_ids = long_protein(records, gene_ids)


oh = open(output_file, "w")
for value in gene_ids.values():
    oh.write(str(value[0]) + "\n")
    oh.write(str(value[1]) + "\n")
oh.close()
