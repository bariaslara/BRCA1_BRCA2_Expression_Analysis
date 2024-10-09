
# import packages
import pandas as pd
import os

def readFiles(path,rows=False, delimiter='\t'):
    """Reads in a file. 
    parameters: 
        path: path to file
        rows: Default to false, if False will read in file normal, if set to True will skip the first three rows
        delimiter: default to '\t' can be used to change delimiter"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File {path} does not exist.")
    try:
        skip = 3 if rows else 0
        data = pd.read_csv(path, delimiter=delimiter, skiprows=skip)
    except pd.errors.EmptyDataError:
        print(f"File {path} is empty or not in correct format.")
        return None
    return data
 
def renameColumns(data):
    data.columns = data.iloc[0]
    data = data.drop(0)
    return data

# Read in all appropriate files; update with file paths to files
mutations_data = readFiles('..path/data_mutations.txt')
clinical_data = readFiles('..path/data_clinical_patient.txt', rows=True)
sample_data = readFiles('..path/data_clinical_sample.txt', rows=True)
expression_data = readFiles('..path/data_mrna_seq_v2_rsem.txt')


# Select appropriate columns in mutations data then rename sample_id column
mutations_data = mutations_data[["Hugo_Symbol", "Tumor_Sample_Barcode", "Mutation_Status","Variant_Classification"]]
mutations_data = mutations_data.rename(columns={'Tumor_Sample_Barcode': 'SAMPLE_ID'})


# Filter mutations data by separating brca1 and brca2
brca1_data = mutations_data[mutations_data['Hugo_Symbol'] == 'BRCA1']
brca2_data = mutations_data[mutations_data['Hugo_Symbol'] == 'BRCA2']


# Fix column names in sample and clinical data
clinical_data = renameColumns(clinical_data)
sample_data = renameColumns(sample_data)

# Merge sample and clinical data by Patient_ID then select appropriate columns
clinical_sample_data = pd.merge(clinical_data, sample_data, on='PATIENT_ID', how='outer')
clinical_sample_data = clinical_sample_data[["PATIENT_ID", "SAMPLE_ID", "AGE","RACE","PREOPERATIVE_PSA","CLINICAL_GLEASON_SUM"]]


# Merge mutations and clinical data by SAMPLE_ID
mutations_sample_brca1_data = pd.merge(brca1_data, clinical_sample_data, on='SAMPLE_ID', how='inner')
mutations_sample_brca2_data = pd.merge(brca2_data, clinical_sample_data, on='SAMPLE_ID', how='inner')

# Wrangle expression data by transposing and creating a SAMPLE_ID and Expression column
expression_data_long = pd.melt(
    expression_data,
    id_vars=['Hugo_Symbol', 'Entrez_Gene_Id'],
    var_name='SAMPLE_ID',
    value_name='Expression' 
)

# Select appropriate columns for expression data then filter by BRCA1 and BRCA2
expression_data_long = expression_data_long[['Hugo_Symbol', 'SAMPLE_ID', 'Expression']]
expression_data_brca1 = expression_data_long[expression_data_long['Hugo_Symbol'] == 'BRCA1']
expression_data_brca2 = expression_data_long[expression_data_long['Hugo_Symbol'] == 'BRCA2']

# Merge mutattions/clinical/expression data by SAMPLE_ID
final_brca1_data = pd.merge(mutations_sample_brca1_data, expression_data_brca1, on='SAMPLE_ID', how='inner')
final_brca2_data = pd.merge(mutations_sample_brca2_data, expression_data_brca2, on='SAMPLE_ID', how='inner')

# Write final data to new csv for analyzing; update path to folder to hold final data
final_brca1_data.to_csv('..path/final_brca1_data.csv', index=False)
final_brca2_data.to_csv('..path/final_brca2_data.csv', index=False)


## Citation
# Please cite the following if you use this dataset for your research:
# Cancer Genome Atlas Research Network (2015). The Molecular Taxonomy of Primary Prostate Cancer. Cell, 163(4), 1011–1025. https://doi.org/10.1016/j.cell.2015.10.025

## Data Source
#All data associated with this study can be found at cBioPortal.
#Link: https://www.cbioportal.org/study/summary?id=prad_tcga_pub
