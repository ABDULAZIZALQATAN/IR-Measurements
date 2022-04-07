import general as gen
import bash as sh
import eval as eval
import os


dummy_folder = 'dum'

def get_root_folder():
    p = os.getcwd()
    return p.replace('/src','')

def get_template_bash ():
    default_root = gen.default_root
    line = '#!/bin/bash \n' + \
            'cd %s\n' % default_root + \
            'nohup target/appassembler/bin/SearchCollection -index %index ' + \
            '-topicreader Trec -topics %qry -hits %hits %modelLine %exp ' + \
            '-output %resFile & wait'
    return line

def runBashFile (path , file):
    cmd = r"cd %s && sh %s" % \
          (path,file)
    return sh.runBashCmd(cmd)

def  getExpCmd (exp, docs, terms, beta):
#    -rm3 -rm3.fbTerms $fbTerms -rm3.fbDocs $fbDocs -rm3.originalQueryWeight $beta /
#    -axiom -axiom.n $fbDocs -axiom.top $fbTerms -axiom.beta $beta -axiom.deterministic -rerankCutoff 20
    switcher = {
        'a':'-axiom -axiom.n %d -axiom.top %d -axiom.beta %0.2f -axiom.deterministic -rerankCutoff 20',
        'r':'-rm3 -rm3.fbDocs %d -rm3.fbTerms %d -rm3.originalQueryWeight %0.2f'
    }
    exp = exp[0].lower()
    if (exp == 'b'):
        result = ''
    else:
        result = switcher.get(exp,'')
        result = result % (docs,terms,beta)
    return result

def process_input(corpus, exp, model, parameter, docs, terms, beta, index, res_file, qry_file):
    '''
    Process All input to get All output:
    index = default index if Empty
    res_file = default res_file if Empty
    qry = qry File
    hits = number of hits
    modelLine = Retrieval Model Line
    exp_line = Query Expansion Line
    '''

    result = False
    default_root = gen.default_root
    exp = gen.getExp(exp)
    corpus = gen.getCorpus(corpus)
    model = gen.getModel(model)

    if (index == ''):
        index = '%s/indexes/%s' % (default_root,gen.getIndex(corpus))

    if (res_file == ''):
        res_file = '%s/%s/%s' % (default_root , dummy_folder ,
                    gen.getOutputResName(corpus,exp,model,parameter,False,beta,docs,terms))
    if (qry_file == ''):
        qry_file = '%s/resource/%s/50XML.qry' % (default_root,corpus)

    hits = '1000'
    modelLine = gen.getModelLine(model,parameter)
    exp_line = getExpCmd(exp, docs, terms, beta)
    result = [index , res_file , qry_file , hits ,modelLine , exp_line]
    return result

def processExperiment (index , res_file, qry_file , modelLine, exp_line, hits):

    default_root = gen.default_root
    lines = get_template_bash()

    replacements = {
        '%index':index,
        '%qry':qry_file,
        '%hits':hits,
        '%resFile':res_file,
        '%modelLine':modelLine,
        '%exp':exp_line
    }
    for old,new in replacements.items():
        lines = lines.replace(old,new,1)

    # Create Dummy Folder
    path = '%s/%s' % ( default_root , dummy_folder)
    if (not os.path.exists(path)):
        os.mkdir(path)


    filled_template_file = res_file.replace('.res','-template.sh')
    # Write New Template File after Filling parameters

    f = open(filled_template_file,'w')
    f.write(lines)
    f.close()

    runBashFile(default_root , filled_template_file)

def run_experiment(corpus,exp,model,docs,terms,beta,parameter , index , res_file , qry_file):
    '''
    Important :
        Linux Interpreter that recognize bash commands must be used
    ---------------------------------------------------------
    Run and evaluate based on input
    Return Effectiveness Measures:
        'corpus,qryExpansion,beta,model,fbDocs,fbTerms,'Retrievalparameter,TrecMAP,
        TrecBref,TrecP10,TrecNDCG,CWLMAP,CWLNDCG,CWLP10,CWLRBP0.4,CWLRBP0.6,CWLRBP0.8'

    corpus = ( a = AQUAINT , c = CORE17 , w = WAPO )
    exp = (b = Baseline , a = Axiom , r = RM3 )
    model = ( b = BM25 , P = PL2 , l = LMD )
    docs = Number of FbDocs - For Baseline = 0 automatically
    terms = Number of FbTerms - For Baseline = 0 automatically
    beta = Original Query Weight
    parameter = Length Normalization Parameter
    index = Index to use with Path -
            For empty use default index path ~/anserini/indexes/ (Anserini index Name Ex. lucene-index.robust05.pos+docvectors+rawdocs)
    res_file = res_file from Experiment - if Empty use default path ~/anserini/ (our Naming Ex = AQ-BM25-AX-b0.1-200K-beta0.5-10-05.res)

    qry_file = qry_file from Experiment - if Empty use default path ~/anserini/resource
    '''
    result = process_input(corpus,exp,model,parameter , docs , terms , beta , index , res_file, qry_file)
    line = ''
    if (result):
        [index , res_file , qry_file , hits ,modelLine , exp_line ] = result
        processExperiment( index , res_file, qry_file , modelLine, exp_line, hits)
        line = eval.eval_performance(res_file,corpus)
        line = ','.join(line)
    return line