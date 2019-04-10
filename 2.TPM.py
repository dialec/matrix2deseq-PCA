# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 14:36:56 2018

@author: diego
"""
import sys
from commands import *
import os
import re
import numpy as np
import pandas as pd
from pandas import Series, DataFrame 
import csv as csv
from itertools import groupby
import fnmatch
import subprocess
import glob2
from scipy.stats import mstats
from math import exp, expm1, log
import subprocess
import string
import datetime
from collections import Counter
import scipy.stats as stats
import random 

print "Loading "+sys.argv[1]+" to apply TPM normalisation..."
count_matrix_file= sys.argv[1]
out_file=count_matrix_file+"_TPM"

count_matrix=pd.read_csv(count_matrix_file, sep="\t", header=0, low_memory=False)
gene_len = pd.read_csv("/home/dbeck/estorage/index/hg19/effective_gene_length_refFlat_hg37.txt", sep="\t", header=0, low_memory=False)
samples_list=count_matrix.columns[1::]

count_matrix=pd.merge(count_matrix,gene_len,on=['Geneid'])
h=0
for subfrac in ['CMP','GMP','HSC','LMPP','MEP','MPP']:
    if subfrac!='MPP': samples_cols=list(samples_list[samples_list.str.contains(subfrac)])
    else: samples_cols=list(samples_list[((samples_list.str.contains(subfrac))&(~samples_list.str.contains("L"+subfrac)))])

    for i in range(len(samples_cols)):
        
        sample=samples_cols[i]
        print sample
        count_sample=count_matrix.copy()[['Geneid',sample,'length']]
        count_sample['RPK']=count_sample[sample]*1000/count_sample['length']
        per_million_scale_factor=count_sample['RPK'].sum()/1000000
        count_sample['TPM']=count_sample['RPK']/per_million_scale_factor
        TPM_normal_sample=pd.DataFrame({'Geneid':count_sample['Geneid'],sample:count_sample['TPM']})
        TPM_normal_sample=TPM_normal_sample[['Geneid',sample]]
        if i==0: TOTAL_TPM_cell=TPM_normal_sample.copy()
        else: TOTAL_TPM_cell=pd.merge(TOTAL_TPM_cell,TPM_normal_sample,on=['Geneid'])
    
    #TOTAL_TPM_cell=TOTAL_TPM_cell.sort_values([sample],ascending=[False]).reset_index(drop=True)
    if h==0: TOTAL_TPM=TOTAL_TPM_cell.copy()
    else:  TOTAL_TPM=pd.merge(TOTAL_TPM,TOTAL_TPM_cell,on=['Geneid'])
    h=h+1

TOTAL_TPM.to_csv(out_file, index=False, header=True, sep='\t')