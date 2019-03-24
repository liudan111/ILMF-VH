'''
[1] Yong Liu, Min Wu, Chunyan Miao, Peilin Zhao, Xiao-Li Li, "Neighborhood Regularized Logistic Matrix Factorization for Drug-target Interaction Prediction", under review.
'''
import os
import sys
import time
import getopt
from nrlmf import NRLMF

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "m:d:f:c:s:o:n:p", ["method=", "dataset=", "data-dir=", "cvs=", "specify-arg=", "method-options=", "predict-num=", "output-dir=", ])
    except getopt.GetoptError:
        sys.exit()

    data_dir = os.path.join(os.path.pardir, 'data')
    output_dir = os.path.join(os.path.pardir, 'output')
    cvs, sp_arg, model_settings, predict_num = 1, 1, [], 0

    seeds = [7771]
    #seeds = [7771, 8367, 22, 1812, 4659]
    #seeds = np.random.choice(10000, 10, replace=False)
    for opt, arg in opts:
        if opt == "--method":
            method = arg
        if opt == "--dataset":
            dataset = arg
        if opt == "--data-dir":
            data_dir = arg
        if opt == "--output-dir":
            output_dir = arg
        if opt == "--cvs":
            cvs = int(arg)
        if opt == "--specify-arg":
            sp_arg = int(arg)
        if opt == "--method-options":
            model_settings = [s.split('=') for s in str(arg).split()]
        if opt == "--predict-num":
            predict_num = int(arg)
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    # default parameters for each methods
    if method == 'nrlmf':
        args = {'c': 5, 'K1': 5, 'K2': 5, 'r': 60, 'lambda_d': 2.0, 'lambda_t':2.0, 'alpha': 0.0313, 'beta':4.0, 'theta':1.0, 'max_iter': 100}
    if method == 'netlaprls':
        args = {'gamma_d': 10.0, 'gamma_t': 10.0, 'beta_d': 1e-05, 'beta_t': 1e-05}
    if method == 'blmnii':
        args = {'alpha': 0.8, 'gamma': 1.0, 'sigma': 1.0, 'avg': False}
    if method == 'wnngip':
        args = {'T': 0.7, 'sigma': 1.0, 'alpha': 0.9}
    if method == 'kbmf':
        args = {'R': 100}
    if method == 'cmf':
        args = {'K': 50, 'lambda_l': 0.25, 'lambda_d': 0.125, 'lambda_t': 0.125, 'max_iter': 30}

    for key, val in model_settings:
        args[key] = val

    intMat, drugMat, targetMat = load_data_from_file(dataset, os.path.join(data_dir, 'datasets'))
    drug_names, target_names = get_drugs_targets_names(dataset, os.path.join(data_dir, 'datasets'))

    if predict_num == 0:
        if cvs == 1:  # CV setting CVS1
            X, cv = intMat, 1
        if cvs == 2:  # CV setting CVS2
            X, cv = intMat, 0
        if cvs == 3:  # CV setting CVS3
            X, D, T, cv = intMat.T, targetMat, drugMat, 0
        cv_data = cross_validation(X, seeds, cv)
        #scipy.io.savemat('D.mat', mdict={'D': D})
        #scipy.io.savemat('T.mat', mdict={'T': T})
    #np.where(intMat>0, intMat, -1)

    if sp_arg == 1 or predict_num > 0:
        tic = time.clock()
        if method == 'nrlmf':
            model = NRLMF(cfix=args['c'], K1=args['K1'], K2=args['K2'], num_factors=args['r'], lambda_d=args['lambda_d'], lambda_t=args['lambda_t'], alpha=args['alpha'], beta=args['beta'], theta=args['theta'], max_iter=args['max_iter'])
        if method == 'netlaprls':
            model = NetLapRLS(gamma_d=args['gamma_d'], gamma_t=args['gamma_t'], beta_d=args['beta_t'], beta_t=args['beta_t'])
        if method == 'blmnii':
            model = BLMNII(alpha=args['alpha'], gamma=args['gamma'], sigma=args['sigma'], avg=args['avg'])
        if method == 'wnngip':
            model = WNNGIP(T=args['T'], sigma=args['sigma'], alpha=args['alpha'])
        if method == 'kbmf':
            model = KBMF(num_factors=args['R'])
        if method == 'cmf':
            model = CMF(K=args['K'], lambda_l=args['lambda_l'], lambda_d=args['lambda_d'], lambda_t=args['lambda_t'], max_iter=args['max_iter'])
        cmd = str(model)
        if predict_num == 0:
            print "Dataset:"+dataset+" CVS:"+str(cvs)+"\n"+cmd
            fpr_vec, tpr_vec, aupr_vec, auc_vec = train(model, cv_data, X)
            aupr_avg, aupr_conf = mean_confidence_interval(aupr_vec)
            auc_avg, auc_conf = mean_confidence_interval(auc_vec)
            print "auc:%.6f, aupr: %.6f,auc_conf:%.6f, aupr_conf:%.6f,Time:%.6f" % (auc_avg, aupr_avg,auc_conf, aupr_conf,time.clock()-tic)
            write_metric_vector_to_file(auc_vec, os.path.join(output_dir, method+"_auc_cvs"+str(cvs)+"_"+dataset+".txt"))
            write_metric_vector_to_file(aupr_vec, os.path.join(output_dir, method+"_aupr_cvs"+str(cvs)+"_"+dataset+".txt"))
            write_metric_vector_to_file(fpr_vec, os.path.join(output_dir, method+"_fpr_"+dataset+".txt"))
            write_metric_vector_to_file(tpr_vec, os.path.join(output_dir, method+"_tpr_"+dataset+".txt"))
        elif predict_num > 0:
            seq=np.loadtxt(open('820_snf/seq/vhonf821_2699.csv',"rb"),delimiter=",",skiprows=0)
            print "Dataset:"+dataset+"\n"+cmd
            seed = 7771 if method == 'cmf' else 22
            #print(np.shape(drugMat))
            # print(np.shape(targetMat))
            #print(np.shape(intMat))
            model.fix_model(intMat, intMat, drugMat, targetMat, seed)
            # print(np.shape(drugMat))
            # print(np.shape(targetMat))
            # print(np.shape(intMat))
            x, y = np.where(intMat == 0)
            #x, y = np.where(intMat == 1)
            scores = model.predict_scores(zip(x, y), 5,seq)
            ii = np.argsort(scores)[::-1]
            print(ii)
            predict_pairs = [(drug_names[x[i]], target_names[y[i]], scores[i]) for i in ii[:predict_num]]
            print predict_pairs
            with open('821seqresultnewcanshu.csv', 'w') as f:
                for item in predict_pairs:
                   f.write(str(item).encode('utf-8'))
                   f.write("\n")
            #new_dti_file = os.path.join(output_dir, "_".join([method, dataset, "new_dti.txt"]))
            #novel_prediction_analysis(predict_pairs, new_dti_file, os.path.join(data_dir, 'biodb'))

if __name__ == "__main__":
    main(sys.argv[1:])
