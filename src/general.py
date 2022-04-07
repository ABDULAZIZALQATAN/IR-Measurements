import sys
from datetime import datetime
import shutil as shu
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Constants
# Default Values
trec_file = '~/anserini/trec_eval/trec_eval'
cwl_file = '~/cwl/cwl-eval'

# End Of Constants


def getDefaultCoefficient(model):
    switcher = {
        'B':0.75,
        'P':1,
        'L':1000
    }
    result = switcher.get(model[0].upper(),'')
    return str(result)

def printCurrentTime(title):
    result = getCurrentTime()
    print(title , ": date and time =", timeToString(result))
    return result

def getCurrentTime():
    return datetime.now()

def getCurrentTimeString():
    return timeToString(datetime.now())

def getExp(exp):
    switcher = {
        'B': 'BA',
         'A':'AX',
        'R':'RM3'
    }
    result = switcher.get(exp[0].upper(),'')
    return result

def getModel(model):
    switcher = {
        'B': 'BM25',
        'P':'PL2',
        'L':'LMD'
    }
    result = switcher.get(model[0].upper(),'')
    return result

def getTwoNumbers(num):
    return str(num).zfill(2)

def timeToString (time):
    result = time.strftime("%d/%m/%Y %H:%M:%S")
    return result

def getCorpus(c):
    switcher = {
        'A': 'AQUAINT',
        'C': 'CORE17',
        'W': 'WAPO'
    }
    return switcher.get(c[0].upper())

def getModelCoefficient(model):
    switcher = {
        'BM25': 'b',
        'PL2': 'c',
        'LMD': 'mu'
    }
    return switcher.get(model)

def get_coefficient_range(model):
    model = getModel(model)
    switcher = {
        'BM25': [x / 10 for x in range(1,11)],
        'PL2' : [0.1 ,  0.5 ,1 , 5 , 10 , 15 , 20 , 50],
        'LMD': list(range(100,1100,100)) + [5000]
    }
    return switcher.get(model,'None')

def getQryExpansion(c):
    switcher = {
        'A': 'AX',
        'B': 'Baseline',
        'R': 'RM3'
    }
    return switcher.get(c.upper())

def getResHeader():
    return ['qryID','dum','docid','rank','score','tag']

def getPerformanceHeader():
    return 'TrecMAP TrecBref TrecP10 TrecNDCG CWLMAP CWLNDCG CWLP10 CWLRBP0.4 CWLRBP0.6 CWLRBP0.8'.split()

def getGainFile(c):
    corpus = getCorpus(c[0])
    result = r'~/resource/%s/%s.qrel' % (corpus,corpus)
    return result

def getLinuxPath (path):
    # Windows Path : C:\Users\kkb19103\Desktop\new\data
    # Linux Path : /mnt/c/Users/kkb19103/Desktop/new/data
    replacements = {
        'D:':'/mnt/d',
        'C:':'/mnt/c',
        '\\':'/'
        # ' ':'\ '
        # '\\':'\\'
    }
    result = path
    for key , val in replacements.items():
        result = result.replace(key,val)
    return result

def getIndex (corpus):
    switcher = {
        'A' : 'lucene-index.robust05.pos+docvectors+rawdocs',
        'C' : 'lucene-index.core17.pos+docvectors+rawdocs',
        'W': 'lucene-index.core18.pos+docvectors+rawdocs'
    }
    result = switcher.get(corpus[0].upper(),'None')
    return result

def getOutputResName(corpus,exp,model,coefficient,bias,beta,docs,terms):
    # Sample : AQ-BM25-AX-b0.1-200K-beta0.5-10-05.res
    corpus = corpus[:2]
    qry = '200K' if bias else '50'
    modelCoefficient = getModelCoefficient(model)
    result = '%s-%s-%s-%s%s-%s-beta%0s-docs%02d-terms%02d.res' % \
             ( corpus , model.upper() , exp.upper() , modelCoefficient, str(coefficient),qry, str(beta), docs, terms)
    return result

def getModelLine (model, parameter):
    # -spl -spl.c $c - -bm25 -bm25.b $b -bm25.k1 1.2
    model = getModel(model)
    switcher = {
        'BM25':'-bm25 -bm25.b %s -bm25.k1 1.2',
        'PL2':'-spl -spl.c %s',
        'LMD':'-qld -qld.mu %s',
    }
    result = switcher.get(model,'None')
    return result % parameter

def setVaue (dict,key,val):
    val = float(val)
    if (key in dict):
        dict[key] += val
    else:
        dict[key] = val
    return dict

# General Functions - General 2
def get_plot_properties(exp):
    switcher = {
        'B': 'o,b,:',
        'A':'X,g,-',
        'R' : 's,orange,--',
    }
    temp = switcher.get(exp[0].upper(),'N-N')
    [marker, color,line] = temp.split(',')
    return [marker, color,line]

def getGroup (axis):
    if (axis.startswith('G') or axis == 'rSum'):
        result = 'ret'
    elif (axis.endswith('exposure')):
        result = 'fair'
    else:
        result = 'per'
    return result

def getNumTicks(ticks):
    ticks = ticks.split()
    return np.arange(float(ticks[0]), float(ticks[1]), float(ticks[2]))

def plotLine(x,y,exp):
    [marker, color,line] = get_plot_properties(exp)
    plt.plot(x, y, marker = marker, color=color , ls=line);

def printColumns(df):
    cols = df.columns.values
    for i in cols :
        print(i)
    return cols

def getAxisLabel(axis):
    switcher = {
        'G0': "G - Cumulative - \u03B2 = 0 - C = 100",
        'G0.5': "G - Gravity - \u03B2 = 0.5 - C = 100",
        'TrecMAP': "Trec MAP",
        'TrecP10': "P10",
        'TrecNDCG':"Trec NDCG",
        'CWLMAP': "CWL MAP",
        'CWLP10': "CWL P10",
        'CWLNDCG': 'CWL NDCG',
        'TrecBref': "Binary Preference",
        'rSum0': "Total Retrievability Mass",
        'rSum0.5': "Total Retrievability Mass",
        'CWLRBP0.4' : 'Rank Biased Precision 0.4',
        'CWLRBP0.6': 'Rank Biased Precision 0.6',
        'CWLRBP0.8': 'Rank Biased Precision 0.8',
        'fbTerms': 'FbTerms',
        'fbDocs': 'FbDocs'
    }
    return switcher.get(axis)

def showFigure(title ,legend, xLabel , yLabel):
    [fSize, fWeight] = [17,500]
    plt.title(title,size=fSize,weight=fWeight)
    plt.xlabel(xLabel,size=fSize,weight=fWeight)
    plt.ylabel(yLabel,size=fSize,weight=fWeight)
    if (legend != ''):
        plt.legend(title=legend,ncol=2)

def filterDf (df, dictCriteria):
    '''
    First Criteria should be Equal criteria
    Operators might be inserted at the end of the key in input dictionary
    -< for <
    -> for >
    -! for !=
    -isin for isin
    '''
    if (len(dictCriteria) > 0):
        criteria = ''
        for item in dictCriteria:
            if (item.__contains__('-')):
                parts = item.split('-')
                key = parts[0]
                operator = parts[1]
                value = dictCriteria[item]
                if (operator == '<'):
                    criteria &= df[key] < value
                elif (operator == '>'):
                    criteria &= df[key] > value
                elif (operator == '!'):
                    criteria &= df[key] != value
                elif (operator == 'isin'):
                    criteria &= df[key].isin(value)
            else:
                # First Criteria should be Equal
                value = dictCriteria[item]
                if (len(criteria) == 0):
                    criteria = df[item] == value
                else:
                    criteria &= df[item] == value
        df = df[criteria]
    return df

def add_document_length (df, corpus, subset_group_count , total_group_count):
    group = 'length'
    key = 'docid'

    df_corpus = read_corpus_file(corpus)
    df_all = pd.concat([df,df_corpus],axis=1, join='inner' , keys=key)
    df_all.columns = df_all.columns.droplevel(0)
    hdr = list(df.columns.values) + [group]
    df = df_all[hdr]
    df = df.loc[:,~df.columns.duplicated()]
    df_all = None
    df_corpus = None
    # Add grouping sequence Number Field
    df = add_group_field(df,group,subset_group_count,total_group_count)


    return df

def add_group_field(df,group, subset_group_count,total_group_count):
    # Extract Top (groupCount) From total 100 Groups
    # group count <= 100
    # total_count = 100
    cohort_field = 'length_group'

    if (subset_group_count > total_group_count):
        print('Error in group counts')
        return
    # Sort By intended Field ( Length )
    df.sort_values([group], ascending=False, inplace=True)

    total_num_docs = len(df)
    bucket_size = total_num_docs // total_group_count
    # 4- build a list (bucket_list) that assigns the first n docs to bucket 1, the next n to bucket 2, etc.
    rng = list(range(1,total_group_count + 1)) * bucket_size
    rem = total_num_docs - (bucket_size * total_group_count)
    rng += list(range(rem,0,-1))
    df[cohort_field] = sorted(rng)
    # Extract Top of given group_count from 100 counts
    criteria = df[cohort_field] <= subset_group_count
    return df[criteria]

def get_average(df):
    return df / df.sum() * 100

# Reading CSV
def read_res_file (file):
    hdr = getResHeader()
    return pd.read_csv(file,names=hdr,sep=' ')

def read_df(file):
    return pd.read_csv(file)

