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



#input_data=pd.read_csv("LAB_summary.featurecount_refFlat_PE.count", sep="\t", header = 0 , low_memory=False)                 

                
                 
read_count_file=sys.argv[1] #"MERGED_summary.featurecount_PE.count"

matrix= pd.read_csv(read_count_file, sep="\t", header = 0 , low_memory=False)


total_samples=int(sys.argv[2])
min_count=total_samples*1

print "Defining output file..."
if min_count>0:
     suffix="_min"+str(min_count)
else:
    suffix=""

out_file=read_count_file.split(".read_count")[0]+suffix+".read_count"


      
print "Creating filtered matrix..."
matrix.set_index('Geneid',inplace=True)
flag=[]
    
for h in matrix.index:
    gene=matrix.ix[h]
    flag.append(str(sum(gene)))  


matrix['flag']=map(int,flag)
matrix=matrix[matrix['flag']>=min_count] #--> 1. Filter based on min number of reads

        
print "adding 1..."            
#matrix=matrix+1
print "Remove temp col..."            
del matrix['flag']
matrix.to_csv(out_file,index=True,header=True,sep='\t')    
    

          