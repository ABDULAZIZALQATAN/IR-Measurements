import bash as sh

trec_file = '~/anserini/trec_eval/trec_eval'

def executeBash(resFile,gainFile):
    measures = '-m map -m bpref -m P.10 -m ndcg'
    cmd = '%s %s %s %s' % (trec_file , measures ,gainFile,resFile)
    result = sh.runBashCmd(cmd)
    return result

def getTrecData (resFile , gainFile):
    # Given a path af trec File Return [map - BPref - P10 - NDCG]
    f = executeBash(resFile,gainFile)
    result = []
    lines = f.split('\n')
    # map , bpref , P.10 , ndcg'
    for line in lines:
        value = line.split('\t')[2]
        result.append(value)
    return result