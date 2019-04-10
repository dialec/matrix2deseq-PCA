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

#"python "

print "Generating PCA..."
input_file= sys.argv[1]
samples_desc=sys.argv[2] # "CPM,CPM,CPM,GMP,GMP,GMP,HSC,HSC,HSC,LMPP,LMPP,LMPP,MEP,MEP,MEP,MPP,MPP,MPP"
samples_desc=samples_desc.split(",")
samples_desc_df=pd.DataFrame({'sample':samples_desc})

print "Generating colorcode string for matlab"
color_scheme=['b','k','r','g','y','c','m'] #,'w=white but not included
len_color_scheme=len(color_scheme)

samples_df=pd.DataFrame({'sample':samples_desc})
samples_df=samples_df.drop_duplicates().reset_index(drop=True)

sample_code=[]
for i in range(len(samples_df)): sample_code.append(color_scheme[i%len_color_scheme])
samples_df['sample_code']=sample_code

samples_desc=pd.merge(samples_desc_df,samples_df,on='sample')
colorcode=samples_desc['sample_code'].str.cat()

    
    
    



print "Generating main MATLAB script..."
aln_file="sPCA_DCH.m"

for i in [0]:
    try:
        outF=open(aln_file, "w")
        outF.write("""x = importdata('"""+input_file+"""')\n;""")
        outF.write("""genes = x.textdata(:,1);\n""")
        outF.write("""genes(1) = [];\n\n""")
        
        outF.write("samples = x.textdata(1,:);\n")
        outF.write("samples(1) = [];\n\n")
        
        outF.write("exp = x.data;\n\n")
        
        outF.write("""colorcode(1:length(samples)) = '"""+colorcode+"""';\n""")
        outF.write("symbols(1:length(samples)) = 'o';\n\n")            
        
        outF.write("save('expr.mat');\n\n")            
        
        outF.write("f_pcaGeneExp('expr.mat', 100);\n")            
        
        outF.write("%f_pcaPlotsGeneExpDetail('expr.mat', 'pcaDetails_expr.mat', 100);\n\n")            
      
        outF.write("""%Instructions: nohup  matlab -nosplash -nodisplay -nodesktop -r 'try; sPCA_DCH; catch; end; quit' > output_sPCA_DCH.log &""")
                             
        outF.close()
        
        print "Executing Matlab script - "+aln_file
        subprocess.call("""matlab -nosplash -nodisplay -nodesktop -r 'try; sPCA_DCH; catch; end; quit'""", shell=True)
        print "Script is being executed in the background. Execute the last part of the code on Windows"
    
    except:
        print "ERROR GENERATING THE FILE..."
        
    