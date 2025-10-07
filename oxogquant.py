#!/usr/bin/env python3

## This is a program to quantitate 8-oxo G in RNA-Seq datasets based on
## the presence of G to T transversions in the sense strand of the RNA
## It takes in BAM files and produces directional quantitations of all
## observed Gs in the data along with the frequency of G to T transversions

import argparse
import pysam
from pathlib import Path


options = None

def main():
    get_options()



    # Structure of the quantitations will be
    # quantitation = {"chr:pos:strand": {bamfile:[totalcount,gt_count]}}
    quantitations = {}

    for bamfile in options.bamfiles:
        process_bamfile(Path(bamfile),quantitations)

    write_output(quantitations)

def write_output(quantitations):

    print("Writing output to",options.outfile, flush=True)
    with open(options.outfile,"wt",encoding="utf8") as out:

        filenames = []

        for file in options.bamfiles:
            filenames.append(Path(file).name)

        # Write the headers
        headers = ["Locus"]
        for file in filenames:
            headers.append(file+" Total")
            headers.append(file+" Transformed")

        print("\t".join(headers), file=out)

        for locus in quantitations:
            line = [locus]

            for file in filenames:
                if file in quantitations[locus]:
                    line.extend(quantitations[locus][file])

                else:
                    line.extend([0,0])

            line = [str(x) for x  in line]

            print("\t".join(line), file=out)


def process_bamfile(file,quantitations):

    print("Processing",file.name, flush=True)

    bamin = pysam.AlignmentFile(file, "rb")

    for i,read in enumerate(bamin.fetch(until_eof=True)):

        if i>0 and i % 100000 == 0:
            print(f"Read {i} reads", flush=True)
            # break ##### JUST TESTING ########
        

        # We need to figure out the direction we're looking in
        # ie looking for G or C
        # 
        reverse = options.direction=="opposing"

        chr = read.reference_name
        strand = "+"

        if read.is_reverse:
            reverse = not reverse
            strand = "-"

        seeking = "G"
        checking = "T"

        if reverse:
            seeking = "C"
            checking = "A"

        query_seq = read.query_sequence

        for query_zero_pos, ref_zero_pos, ref_base in read.get_aligned_pairs(with_seq=True):
            if ref_base != seeking:
                continue

            # There may not be an alignment for this position
            if query_zero_pos is None:
                continue

            # We have a position we want to record
            modified = query_seq[query_zero_pos] == checking

            # Our genome position will be the reported position plus one (it's zero indexed)

            position = ref_zero_pos+1
                
            locus = chr+":"+str(position)+":"+strand

            if not locus in quantitations:
                quantitations[locus] = {}

            if not file.name in quantitations[locus]:
                quantitations[locus][file.name] = [0,0]

            quantitations[locus][file.name][0] += 1 # We saw this base
            
            if modified:
                quantitations[locus][file.name][1] += 1 # The base was modified

            

def get_options():

    parser = argparse.ArgumentParser("Quantitation of 8-oxo-G G to T transversions")

    parser.add_argument("--direction",choices=["same","opposing"], help="Direction of the library - same or opposing strand", required=True)
    parser.add_argument("--outfile", type=str, default="oxogquant_output.txt", help="Output file to write results to")

    parser.add_argument("bamfiles", nargs="+", type=str, help="BAM files to analyse")

    global options
    options = parser.parse_args()



if __name__ == "__main__":
    main()