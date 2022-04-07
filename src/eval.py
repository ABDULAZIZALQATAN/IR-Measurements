import trec  as trec
import CWL as cwl
import clsRetrievabilityCalculator as rc
import fairnessCalculator as fc
import general as gen

def eval_performance_trec (res_file,corpus):
    '''
    Evaluate Results Based on Given Res File :
    Returns List Of Results
    Performance Results TREC [map , bpref , P.10 , ndcg]
    '''
    gainFile = gen.getGainFile(corpus)
    # Set Trec Path
    trec.trec_file = gen.trec_file
    result =  trec.getTrecData(res_file,gainFile) # map , bpref , P.10 , ndcg'
    return result

def eval_performance_cwl (res_file,corpus):
    '''
    Evaluate Results Based on Given Res File :
    Returns List Of Results
    Performance Results CWL [Map,NDCG, P10,RBP0.4, RBP0.6, RBP0.8]
    '''
    gainFile = gen.getGainFile(corpus)
    # Set Cwl Path
    cwl.cwl_file = gen.cwl_file
    result = cwl.getMetricsValues(res_file,gainFile) # [Map,NDCG, P10,R4, R6, R8]
    return result



def eval_performance (res_file,corpus):
    '''
    Evaluate Results Based on Given Res File :
    Returns List Of Results
    Performance Results TREC [map , bpref , P.10 , ndcg] - CWL [Map,NDCG, P10,RBP0.4, RBP0.6, RBP0.8]
    '''
    trecResults =  eval_performance_trec(res_file,corpus)
    cwlResults = eval_performance_cwl(res_file,corpus)
    result = trecResults + cwlResults
    return result

def format_line (corpus,model,parameter,b,bias_fairness_results):
    line = ','.join([corpus,model,str(parameter) , str(b)] +  bias_fairness_results)
    return line

def eval_bias (res_file , corpus , b):
    return rc.calculate(res_file,b,corpus,'')

def eval_fairness(res_file , corpus , b):
    return fc.calculate(res_file,'author',corpus,b)

def eval_bias_fairness (res_file , corpus , b ):
    bias_results = eval_bias(res_file , corpus , b)
    fairness_results = eval_fairness(res_file , corpus , b)
    result = bias_results + fairness_results
    return result
