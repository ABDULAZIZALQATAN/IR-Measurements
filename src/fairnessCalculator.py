import numpy as np
# import pandas as pd
import classes.general as gen
# import clsRetrievabilityCalculator as rc



def calculate_fairness(dict_corpus,dict_ret,exposure_operation,fairness_field,fairness_operation):

    exposure_result = {}
    exposure_count = {}
    fairness_result = {}
    faieness_val_index = 'rel_sum rel_count'.split().index(fairness_field) + 1
    for docid , val in dict_corpus.items():
        # Get author
        group = val[0]
        # Assign Exposure
        r = dict_ret[docid]
        exposure_result = gen.setVaue(exposure_result,group,r)
        if (exposure_operation == 'mean'):
            exposure_count = gen.setVaue(exposure_count,group,1)
        # Assign Fairness
        if (fairness_operation != 'equal'):
            r = val[faieness_val_index] if (fairness_operation == 'sum') else 1
            fairness_result = gen.setVaue(fairness_result,group,r)

    values = list(exposure_result.values())
    if (exposure_operation == 'mean'):
        values = np.divide(values , list(exposure_count.values()))
    exposure = compute_percent(values)

    # fld = list(agg.keys())[1]

    values = [1] * len(values) if (fairness_operation == 'equal') else list(fairness_result.values())
    fairness = compute_percent(values)
    result = compute_fairness_score(fairness,exposure)
    return result

def compute_percent(v):
    total_v = np.sum(v)
    percent_v = np.divide(v , total_v)
    return percent_v

def compute_fairness_score(a, b):
    c = np.subtract(a,b)  # substract
    c = np.power(c,2) # square
    c = np.sum(c) # sum
    score = np.power(c, 0.5) #square root
    return score


def get_fairness_scores(dict_corpus,dict_ret):
    '''
    Calculate Exposure_g
    	For each group calculate the sum of the r(d) values
        Then workout the proportion of r(d) for each group g.  = Exposure_g
    '''

    '''
    Calculate Rel_count_g
    	For each group, calculate the count of the #rels for each 
    	group g, = Rel_count_g    = sum of rel counts for group / total rel count over the collection
    '''
    exposure_operation = ''
    # agg = {rField:'sum' , 'rel_count':'sum'}
    # print('Begin F(Relevance)')
    # fairness_field = 'rel_count'
    # fairness_operation = 'sum'
    # rel_count_exposure = calculate_fairness(dict_corpus,dict_ret,exposure_operation,fairness_field,fairness_operation)

    '''
        Calculate Rel_g
        	For each group, calculate the sum of the #rels for each 
        	group g, = Rel_g    = sum of rels for group / total rels over the collection
        '''
    # 1 Fairness(Relevance)
    # print('Begin F(Relevance)')
    fairness_field = 'rel_sum'
    fairness_operation = 'sum'
    rel_sum_exposure = calculate_fairness(dict_corpus,dict_ret,exposure_operation,fairness_field,fairness_operation)

    '''
    Calculate Size_g 
        For each group, calculate the total group member - 
        i.e. the number of documents in the group = Size_g
    '''
    # print('Begin F(Group)')
    # Fairness(Group)
    fairness_field = 'rel_count'
    fairness_operation = 'count'
    size_exposure = calculate_fairness(dict_corpus,dict_ret,exposure_operation,fairness_field,fairness_operation)

    '''
    Calculate Group_g
    - [GROUPs] ALL GROUPS ARE EQUAL
        For each group, Group_g = 1/(Number of groups). 
    '''
    # Fairness(Equality)
    # print('Begin F(Equality)')
    fairness_field = 'rel_count'
    fairness_operation = 'equal'
    grp_exposure = calculate_fairness(dict_corpus,dict_ret,exposure_operation,fairness_field,fairness_operation)

    # print('Begin F(Exposure Mean Over Relevance)')
    exposure_operation = 'mean'
    fairness_field = 'rel_sum'
    fairness_operation = 'sum'
    rel_avg_exposure = calculate_fairness(dict_corpus,dict_ret,exposure_operation,fairness_field,fairness_operation)


    # rel_sum_exposure,size_exposure,grp_exposure,rel_avg_exposure
    result = [ str(x) for x in [rel_sum_exposure,size_exposure,grp_exposure,rel_avg_exposure]]
    return result

def get_ret_dict (resFile,b,dict_corpus):
    dict_ret = {}.fromkeys(dict_corpus.keys(),0)
    resF = open(resFile, 'r', encoding='utf-8')
    for line in resF:
        # print(line)
        parts = line.split()
        # qryid = parts[0]
        docid = parts[2]
        rank = int(parts[3])
        r = rank ** -b
        dict_ret[docid] += r
    resF.close()
    return dict_ret


def get_corpus_dict(corpus_file,group):
    f = open(corpus_file,encoding='utf-8')
    # Skip header
    line = f.readline()
    parts = line.replace('\n','').split(',')
    groupIndex = parts.index(group)
    val_slice = [groupIndex,len(parts)-3 , len(parts) - 2]
    result = {}
    # docid,author,pubDate,kicker,byLine,rel_sum,rel_count,length
    for line in f:
        parts = line.split(',')
        key = parts[0]
        val = [parts[index] for index in val_slice]
        result[key] = val
    f.close()
    return result

def calculate (res_file ,  group , corpus,b):
    corpus = gen.getCorpus(corpus)
    corpus_file = gen.get_corpus_filename(corpus)
    dict_corpus = get_corpus_dict(corpus_file,group)
    dict_ret = get_ret_dict(res_file,b,dict_corpus)
    line = get_fairness_scores(dict_corpus,dict_ret)
    # Output : rel_sum_exposure,size_exposure,grp_exposure,rel_avg_exposure
    return line


def main():
    res_file = r'C:\Users\kkb19103\Desktop\test\WA-BM25-100-200K-baseline.res'
    t1 = gen.getCurrentTime()
    calculate(res_file,'author','w',0.5)
    t2 = gen.getCurrentTime()
    print(t2 - t1)
if __name__ == '__main__':
    main()