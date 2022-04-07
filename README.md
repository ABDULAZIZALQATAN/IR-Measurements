# InformationRetrieval
My Work in Phd Information Retrieval ( Algorithmetic Bias in Search Engines )

### Pre-Requisite
1. Use Linux interpreter to run bash commands

    For Windows Use [WSL Ubuntu Interpreter](https://www.jetbrains.com/help/pycharm/using-wsl-as-a-remote-interpreter.html#configure-wsl)

2. download Anserini [Anserini](https://github.com/castorini/anserini)
Under anserini main path do the following :
   - Create "indexes" folder and put the required indexes of [AQUAINT - CORE17 - WAPO]
    - move resource folder from our Github account to that location for Queries
3. download Trec_Eval [Trec_Eval](https://github.com/usnistgov/trec_eval)
4. download cwl_eval [cwl_Eval](https://github.com/leifos/cwl/tree/master/scripts)
5. Set The locations of [Anserini - Trec_Eval - CWL_Eval] in general.py constants list
### Performance Measurement 
File : performanceCalculator - Test in measurePerformance
#### Description : 
Run Retrieval experiment on 50 queries and get performance measurements based on input

#### input
    corpus , exp , model , docs , terms , beta , parameter , index , res_file , qry_file

1. corpus = ( a = AQUAINT , c = CORE17 , w = WAPO )
2. exp = (b = Baseline , a = Axiom , r = RM3 )
3. model = ( b = BM25 , P = PL2 , l = LMD )
4. docs = Number of FbDocs - For Baseline = 0 automatically
5. terms = Number of FbTerms - For Baseline = 0 automatically
6. beta = Original Query Weight
7. parameter = Length Normalization Parameter
8. index = Index to use with Path -
        For empty use default index path Anserini_root/indexes/ (Anserini index Name Ex. lucene-index.robust05.pos+docvectors+rawdocs)
9. res_file = res_file from Experiment - if Empty use Anserini_root/ (our Naming Ex = AQ-BM25-AX-b0.1-200K-beta0.5-10-05.res)
10. qry_file = qry_file from Experiment - if Empty use Anserini_root/resource
### Output
 [TrecMAP,TrecBref,TrecP10,TrecNDCG,CWLMAP,CWLNDCG,CWLP10,CWLRBP0.4,CWLRBP0.6,CWLRBP0.8]


