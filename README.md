This is a script to calculate the secondary structure of a protein in solution. The script is based on the carbon chemical shifts obtained from sequence specific backbone resonance assignment using solution NMR and the calculated random coil chemical shifts of the same protein sequence using the POTENCI algorithm. 

## How to run
  python3 calc_secstructure.py -i1 FtsHRawShift.csv -i2 POTENCI_result.csv -out secondary_structure.csv -seqno 138

  The packages needed are csv, argparse, pandas, numpy and matplotlib.pyplot

## Arguments
  -h      Prints help message.
  -i1     File with the chemical shifts from NMR assignment in csv format.
  -i2     File with the chemical shifts from the POTENCI algortihm in csv format.
  -out    Name of the csv output file.
  -seqno  The position of the first residue in the wild-type protein sequence (set to 0 if not needed).

  
