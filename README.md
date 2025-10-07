# Quantitating 8-oxo-G

This program takes in an RNA-Seq dataset and quantiate the abundance of 8-oxo-G based on the presence of G to T transversions on the sense strand of the RNA.

The input for the program is one or more BAM files of RNA-Seq data and these will be quantitated over ever observed G in the transcriptome.

The only option to set is the directionality of the library.  The program will only work with directional RNA-Seq libraries.  The options are:

* `same` if the direction of R1 in the data is the same as the original RNA molecule
* `opposing` if the reads seen are the reverse complement of the original RNA molecule

## Installation

To install the program follow these simple steps.  We assume that you have a recent version of python installed already

1. Clone this repository ```git clone https://github.com/s-andrews/oxogquant.git```
2. Move into the newly created folder ```cd oxogquant```
3. Create a virtual environment ```python3 -m venv venv```
4. Activate the environment ```source venv/bin/activate```
5. Install the dependencies ```pip install -r requiremnets.txt```
6. Run the program ```./oxogquant.py --help```


## Usage

```
$ ./oxogquant.py --help
usage: Quantitation of 8-oxo-G G to T transversions [-h] --direction {same,opposing} [--outfile OUTFILE] bamfiles [bamfiles ...]

positional arguments:
  bamfiles              BAM files to analyse

options:
  -h, --help            show this help message and exit
  --direction {same,opposing}
                        Direction of the library - same or opposing strand
  --outfile OUTFILE     Output file to write results to
```