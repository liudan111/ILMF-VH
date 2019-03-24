#820-2699
#caculate
import numpy as np
import pandas as pd
import math
def Gussian_similarity(intMat):
    
    #np.savetxt('vh_admat_dgc_list.csv', result, delimiter = ',')
    
    gamall=1

    
    #nd=max(result[:,0])

    #nl=max(result[:,1])
    nl=np.shape(intMat)[1]
    print nl
    
#    pp=np.shape(result)[0]
#    qq=np.shape(result)[1]
    


    
    #calculate gamal for Gaussian kernel calculation
    sl=np.zeros(nl)
    print(sl)
    for i in range(nl):
        sl[i]=np.square(np.linalg.norm(intMat[:,i]))
    gamal=nl/sum(np.transpose(sl))*gamall
    print gamal
    

    
    hostMat=np.zeros([nl,nl],float)
    for i in range(nl):
        for j in range(nl):
            hostMat[i,j]=math.exp(-gamal*np.square(np.linalg.norm(intMat[:,i]-intMat[:,j])))
   
   
    

    return hostMat 

