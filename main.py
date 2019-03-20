#820-2699
#caculate
import numpy as np
import pandas as pd
from similarity_os import Gussian_similarity
from norm import normFun 

intMat = np.loadtxt("md39_admat_dgc.txt")
hostMat=Gussian_similarity(intMat)
#
#

np.savetxt('md39_admat_dg.csv', hostMat, delimiter = ',')















