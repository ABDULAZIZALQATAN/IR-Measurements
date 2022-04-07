import performanceCalculator as per_calc

def run_single_Experiment():
    # exp ,docs,terms,beta, corpus,bias,model,parameter
    # [index , qry , hits , out , modelLine , exp_line ,coRange] = initialize('')

    corpus = 'a' # a AQUAINT - c CORE17 - w WAPO
    exp = 'b' # a Axiom - r RM3 - b Baseline
    bias = False
    model = 'b' # b BM25 - p PL2 - l LMD
    docs = 0 # default - 10
    terms = 0 # default - 10
    beta = 0
    parameter = 0.75
    index = ''
    res_file = ''
    qry_file = ''
    line =  per_calc.run_experiment(corpus,exp,model,docs,terms,beta,parameter , index , res_file , qry_file)
    print(line)


if __name__ == '__main__':
    run_single_Experiment()