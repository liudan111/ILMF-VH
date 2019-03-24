# LMFH-VH

Kernelized Logistic Matrix Factorization based on Similarity Network Fusion for Predicting Virus-host Association
===========
Xingpeng Jiang, xpjiang@mail.ccnu.edu.cn 
Dan Liu, liudan@mails.ccnu.edu.cn

School of Computer,Central China Normal University Wuhan, China

For any questions regarding to this library, please feel free to contact the author.

Usage codes
---------------

code/dowload_host_of_virus.py  is used to extract the "isolate host =" or "host" fields from the annotation files downloaded from complete viral genomes of  NCBI

code/dowload_virus.py is used to retrieve the viral genomes from NCBI based on the accession numbers of viruses

code/similarity_os.py and code/main.py are used to calculate Gaussian interaction profile kernel similarity between hosts.

code/PyDTI.py and code/nrlmf.py  are used to predict scores between viruses and hosts

The codes of KBMF,NetLapRLS,BLM-NII ,CMF can refer to codes of Yong et al.https://github.com/stephenliu0423/PyDTI [3].

Note:the code is implemented by Python 2.7.9

 Description of datasets
---------------
datasets/dataset I including 71 hosts and 352 viruses which only one specific host genome appeared in the prokaryotic genome database at NCBI[2].

datasets/dataset II including 2699 hosts and 820 viruses which is downloaded from RefSeq on 7/25/2015[1].

datasets/onf including onf measures of viruses and hosts which are obtained by Jie Ren's tools [2].

Note: Jie Ren's tools is used to get dissimilarity between viruses,you should transform to similarity.

Reference and Citation
------------
If you use this codes , please cite the following paper:

Kernelized Logistic Matrix Factorization based on Similarity Network Fusion for Predicting Virus-host Association

Our Reference  
------------
[1]Edwards RA, McNair K, Faust K, Raes J, Dutilh BE, Smith M: Computational approaches to predict bacteriophage–host relationships. FEMS Microbiology Reviews 2016, 40(2):258-272.

[2]Ahlgren NA, Ren J, Lu YY, Fuhrman JA, Sun F: Alignment-free $d_2^*$ oligonucleotide frequency dissimilarity measure improves prediction of hosts from metagenomically-derived viral sequences. Nucleic Acids Research 2017, 45(1):39-53.

[3]Liu Y, Wu M, Miao C, Zhao P, Li XL: Neighborhood Regularized Logistic Matrix Factorization for Drug-Target Interaction Prediction. PLoS computational biology 2016, 12(2):e1004760.
