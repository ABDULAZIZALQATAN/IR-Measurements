import eval as eval
import general as gen


def get_outline_ex2 (corpus,exp,docs,terms,beta,b,eval_line):
    # corpus model coefficient docs terms beta b g(d) ctr_zero(d) rSum(d) g(a) ctr_zero(a) rSum(a) rel_sum_exposure	size_exposure grp_exposure rel_avg_exposure
    line = '%s,BM25,%s,0.4,%s,%s,%s,%s,%s' \
           % (corpus, exp,docs,terms,str(beta),str(b),eval_line)
    return line

def get_file_name_ex2(corpus , exp , docs , terms ):
    # Ex 2
    # CO-BM25-UI-200K-C100-RV-fbdocs20-fbterms10-b0.4-beta0.0
    corpus = corpus[:2]
    beta = 1.0 if exp.upper() == 'RV' else 0.5
    # exp = gen.getExp(exp)
    result = '%s-BM25-UI-200K-C100-%s-fbdocs%s-fbterms%s-b0.4-beta%s.res' % \
             (corpus,exp , docs,terms,str(beta))
    return result

def iterate():
    rng = range(5,35,5)
    beta = 0.5
    # Target Path
    path = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\Thesis Experiments\2- Analyze Query Expansion\csv'
    path += '\Ex2-Ret.csv'
    f = open(path,'a')
    # Source Path
    path = r'D:\Backup 29-04-2021\200K Experiments\2nd Set Query Expansion Checking\res\fbDocs fbTerms Iteration\\'

    for corpus in 'a c w'.split():
        corpus = gen.getCorpus(corpus)
        for exp in 'a r v'.split():
            exp = gen.getExp(exp)
            for docs in rng:
                docs = gen.getTwoNumbers(docs)
                for terms in rng:
                    terms = gen.getTwoNumbers(terms)
                    res_file = path + get_file_name_ex2(corpus,exp,docs,terms)
                    for b in [0,0.5]:
                        eval_line = eval.eval_bias_fairness(res_file,corpus,b)
                        eval_line = ','.join(eval_line)
                        line = get_outline_ex2(corpus,exp,docs,terms,beta,b,eval_line)
                        print(line)
                        f.write(line + '\n')
                        # print(corpus,exp,docs,terms,beta,b)
    f.close()


if __name__ == '__main__':
    iterate()