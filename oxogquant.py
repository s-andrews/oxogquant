#!/usr/bin/env python3

## This is a program to quantitate 8-oxo G in RNA-Seq datasets based on
## the presence of G to T transversions in the sense strand of the RNA
## It takes in BAM files and produces directional quantitations of all
## observed Gs in the data along with the frequency of G to T transversions

import argparse

options = None

def main():
    get_options()

    # Structure of the quantitations will be
    # quantitation = {"chr:pos:strand": {bamfile:[totalcount,gt_count]}}
    quantitations = {}

    for bamfile in options.bamfiles:
        process_bamfile(bamfile,quantitations)

    write_output(quantitations)


def process_bamfile(file,quantitaitons):
    pass


def get_options():

    parser = argparse.ArgumentParser("Quantitation of 8-oxo-G G to T transversions")

    parser.add_argument("--direction",choices=["same","opposing"], help="Direction of the library - same or opposing strand", required=True)
    parser.add_argument("--outfile", type=str, default="oxogquant_output.txt", help="Output file to write results to")

    parser.add_argument("bamfiles", nargs="+", type=str, help="BAM files to analyse")

    global options
    options = parser.parse_args()
