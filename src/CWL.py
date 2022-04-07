import bash as sh
import pandas as pd
import io

cwl_file = '~/cwl/cwl-eval'

def executeBash(resFile,gainFile):
    cmd = '%s %s %s -m ~/cwl/MyMetrics_file' % (cwl_file ,gainFile,resFile)
    result = sh.runPythonBashCmd(cmd)
    return result

def getMetricsValues (resFile,gainFile):
    # CWL
    # [Map,NDCG, P10,R4, R6, R8]
    result = executeBash(resFile,gainFile)
    fileData = io.StringIO(result)
    df = pd.read_csv(fileData,delimiter='\t',names=['Topic','Metric','EU','ETU','EC','ETC','ED'])
    df = df.groupby('Metric')['EU'].agg(['mean']).round(decimals=3)
    result = []
    for i in range(6):
        result.append(str(df.iat[i,0]))
    # [Map,NDCG, P10,R4, R6, R8]
    return result

def displayCWl(resFile,gainFile):
    result = executeBash(resFile,gainFile)
    print(result)