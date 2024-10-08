import csv
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Create parser object and add/parse the arguments for two input files (cara and potenci csv files) and one output file (calculated secondary structure as csv) as well as the residue number.
def parse_files():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i1', '--input1', help = 'Input csv file from CARA.' )
    parser.add_argument('-i2', '--input2', help = 'Input csv file from POTENCI.')
    parser.add_argument('-out', '--output', help = 'Name of the output file, has to be .csv')
    parser.add_argument('-seqno', '--sequence_no', type = int, help = 'Change the final residue number.')
    args = parser.parse_args()
    return args
    
# Read the cara file and load into a pandas dataframe. Delete the rows that does not contain a CA or a CB shift.
def read_cara(Cfile):
    df1 = pd.read_csv(Cfile, delimiter = ';')
    df1 = df1[df1.CA.notnull()]
    df1 = df1[df1.CB.notnull()]
    return df1

# Read the POTENCI file and load into a pandas dataframe. Change the header of #NUM to Residue (as this is the name in the cara file).
def read_potenci(Pfile):
    df2 = pd.read_csv(Pfile, delimiter = ';')
    df2.rename(columns={'#NUM':'Residue'}, inplace=True)
    return df2

# Calculate CA-CB from the cara file and generate a new dataframe with only the residue number and the CA, CB chemical shift difference.
def diff_cara(deltashift_cara):
    df1['CA-CB_cara'] = df1['CA'] - df1['CB']
    df3 = df1[['Residue','CA-CB_cara']]
    return df3
    
# Calculate CA-CB from the potenci file and generate a new dataframe with only the residue number and the CA, CB chemical shift difference.
def diff_potenci(deltashift_potenci):
    df2['CA-CB_potenci'] = df2['CA'] - df2['CB']
    df4 = df2[['Residue','CA-CB_potenci']]
    return df4

# Merge the two dataframes on Residue number into a new dataframe.
def combine(c,p):
    df_merged = df3.merge(df4, on='Residue', how='outer')
    return(df_merged)

# Calculate "Secondary", which is the CA-CB difference of the cara and the potenci values and create a new dataframe with only residue number and secondary values as columns.
def secondary(delta_secondary):
    df_merged['Secondary'] = df_merged['CA-CB_cara'] - df_merged['CA-CB_potenci']
    df_secondary = df_merged[['Residue','Secondary']]
    return(df_secondary)
 
# Calculate Smooth from the secondary values: (2*C-1*C*C+1)/4 OR (2*C*C+1)/3.
def smooth(df_secondary):
    df_smooth = df_secondary[['Residue','Secondary']]
    df_smooth['Smooth'] = np.nan
    
    for i in range(len(df_smooth)): #Loop through the column 'Secondary'.
        current = df_smooth.loc[i, 'Secondary']  #Define the current value.
        if i > 0:
            previous = df_smooth.loc[i-1, 'Secondary']   #Check if the previous row contains a value or if it is NaN.
        else:
            previous = np.nan
        if i < len(df_smooth) -1:    #Check if the next row contains a value or if it is NaN.
            next = df_smooth.loc[i+1, 'Secondary']
        else:
            next = np.nan
        if not pd.isna(previous) and not pd.isna(next): #If both the previous and the next row contains values (not are NaN) then perform the "smooth" calculation.
            df_smooth.loc[i, 'Smooth'] = (previous + 2*current + next)/4
        elif not pd.isna(previous): #If only the previous row contains a value (and the next one is NaN), then perform the "smooth" calc only with the previous value.
            df_smooth.loc[i, 'Smooth'] = (previous + 2*current)/3
        elif not pd.isna(next): #If only the next row contains a value (and the next one is NaN), then perform the "smooth" calc only with the next value.
            df_smooth.loc[i, 'Smooth'] = (next + 2*current)/3
    
    df_final = df_smooth[['Residue', 'Smooth']] #Create a new dataframe containing the residue number and the calculated smooth values.
    df_final.loc[:,('Smooth')] = df_final['Smooth'].round(3)    #Round values to 3 decimals.
    df_final.loc[:,('Smooth')] = df_final['Smooth'].clip(lower=-5, upper=5)   #Set a range of allowed smooth values between -5 and 5.
    df_final = df_final.fillna(0)   #Replace all NaN with 0.
    return(df_final)

# This function takes the seqno argument from the command line and adds that number to every row in the Residue column. In case the cara and the potenci files are not numbered according to the wt sequence.
def seq(df_final, seq_no):
    df_final.loc[:,('Residue')] = df_final['Residue'] + seq_no
    return(df_final)

# Create the output file with the name chosen in the command line.
def create_outfile(out):
    df_final.to_csv(args.output, index=False)

# Output a plot over secondary structure with residue number on the x-axis and smooth values on the y-axis.
def create_plot(df_final):
    plt.figure(figsize = (10,5))
    plt.bar(df_final['Residue'], df_final['Smooth'], color='black', edgecolor='black')
    plt.title('Plot of secondary structure', fontsize=13)
    plt.xlabel('Residue', fontsize=11)
    plt.show()

if __name__ == '__main__':
    args = parse_files()
    df1 = read_cara(args.input1)
    df2 = read_potenci(args.input2)
    df3 = diff_cara(df1)
    df4 = diff_potenci(df2)
    df_merged = combine(df3,df4)
    df_secondary = secondary(df_merged)
    df_final = smooth(df_secondary)
    df_final = seq(df_final, args.sequence_no)
    create_outfile(df_final)
    create_plot(df_final)
    
    
    
    
    
    
   
