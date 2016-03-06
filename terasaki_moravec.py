#python version 3.4.3

import numpy as np
import math

#memo if one would like to package those codes into class
# this is may be good that variables like
#"global_domain"
#"shift_candidates"
#are refered freely from methods belonging in the class

#Testset Generator
#generate global domain

def generateTestDomain(domain_sizes=25):
    domain=np.zeros((domain_sizes,domain_sizes),dtype=int)
    #define test domain size
    row_size=14
    col_size=14
    upper_left_x=3
    upper_left_y=3
    #make square
    for i in range(row_size):
        domain[upper_left_x+i][upper_left_y]=1
        domain[upper_left_x+i][upper_left_y+(col_size-1)]=1
    for j in range(col_size):
        domain[upper_left_x,upper_left_y+j]=1
        domain[upper_left_x+(row_size-1),upper_left_y+j]=1
    return domain

#remark this is for test 
def getSample1():
    rand_generaterd=np.random.rand(9)
    rand_bit_seq=(rand_generaterd>0.5)*1
    return rand_bit_seq

def getSubDomain(global_domain,pt):
    return global_domain[pt[0]:pt[0]+3,pt[1]:pt[1]+3]

def getInspectionDomain(global_domain,inspection_point):
    return getSubDomain(global_domain,inspection_point)

def isDomainValid(glboal_domain,inspection_point,domain_len):
    dom=getInspectionDomain(global_domain,inspection_point)
    for i in dom.shape:
        if (i!=domain_len):
            return False
    return True

#evaluation system
def countDiff(ref_dom,shift_dom):
    return np.count_nonzero(ref_dom-shift_dom)

def getEvaluateValue(ref_dom,shift_mdom,size_of_dom):
    diff=ref_dom-shift_dom
    e_xy=0
    for row in range(size_of_dom):
        for col in range(size_of_dom):
             e_xy+=abs(cmat[row,col]-smat[row,col])
    return e_xy


#innner core algorithm

def generateShiftMat(global_domain,inspection_point,shift_vector):
    collect_point =inspection_point+shift_vector
    return getInspectionDomain(global_domain,collect_point)

def localMinimum(global_domain,inspection_point,shift_candidates,domain_len):
    domain=getInspectionDomain(global_domain,inspection_point)
    eval_list=[]
    for cand in shift_candidates:
        shifted_position=inspection_point+cand
        shift_domain=generateShiftMat(global_domain,inspection_point,cand)
        if(isDomainValid(global_domain,shifted_position,domain_len)):
            eval_list.append(countDiff(domain,shift_domain))
    if(len(eval_list)!=0):
        return min(eval_list)
    else:
        return 0

def cornerCriteriaUsingMoravec(global_domain,inspection_point,domain_len):
    eval_list=[]
    for i in np.arange(-1,2,1):
        for j in np.arange(-1,2,1):
            neighbor_point=np.array([inspection_point[0]+i,inspection_point[1]+j])
            if(isDomainValid(global_domain,neighbor_point,domain_len)):
                eval_list.append(localMinimum(global_domain,neighbor_point,shift_candidates,domain_len))
    return np.array(eval_list)

def searchMaximumPoint(global_domain,shift_candidates,domain_len):
    for j in range(global_domain.shape[0]):
        for i in range(global_domain.shape[1]):
            inspection_point=np.array([i,j])
            if isDomainValid(global_domain,inspection_point,domain_len):
                eval_list=cornerCriteriaUsingMoravec(global_domain,inspection_point,domain_len)
                index_center=math.floor((float(len(eval_list))/2))
                if(np.argmax(eval_list)==index_center and eval_list[index_center]-min(eval_list)>1):
                    print(np.argmax(eval_list))
                    print('corner point at (%s , %s)' % (i+1,j+1))
                    print(eval_list.reshape(3,3))




#Main 
if __name__ == '__main__':
    #testset
    global_domain=generateTestDomain()
    #inspection domain
    domain_len=3 
    shift_candidates=np.array([[0,1],[1,1],[1,-1],[1,0]])
    
    #set a positon of the center of inspection domain as inspection_point
    # 
    #HERE._ _ _  
    #    |_|_|_|
    #    |_|_|_|
    #    |_|_|_|
    #
    print(global_domain)
    searchMaximumPoint(global_domain,shift_candidates,domain_len)