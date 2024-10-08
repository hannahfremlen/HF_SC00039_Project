This is a script to calculate the secondary structure of a protein in solution. The script is based on the carbon chemical shifts obtained from sequence specific backbone resonance assignment using solution NMR and the calculated random coil chemical shifts of the same protein sequence using the POTENCI algorithm. 

## How to run
  python3 calc_secstructure.py -i1 FtsHRawShift.csv -i2 POTENCI_result.csv -out secondary_structure.csv -seqno 138

  The packages needed are csv, argparse, pandas, numpy and matplotlib.pyplot

## Arguments
-h&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Prints help message.

-i1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;File with the chemical shifts from NMR assignment in CSV format.

-i2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;File with the chemical shifts from the POTENCI algorithm in CSV format.

-out&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Name of the CSV output file.

-seqno&nbsp;&nbsp;The position of the first residue in the wild-type protein sequence (set to 0 if not needed).

  ## Outputs
    CSV file containing the residues and the calculated secondary structure (smooth).

    A plot with residues on the x-axis and smooth values on the y-axis where values close to -5 indicate beta-sheet structure and values closer to 5 indicate alpha-helical structure. 
