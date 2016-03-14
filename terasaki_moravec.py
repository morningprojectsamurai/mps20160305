#python version 3.4.3
import numpy as np
import math
__author__ = 'Satoshi Terasaki<terasakisatoshi.math@gmail.com>'

class Moravec(object):
    """global_domain,shift_candidates"""
    def __init__(self,global_domain,shift_candidates):
        self.box_len=3#rename box_size later
        self.shift_candidates=shift_candidates
        self.global_domain=global_domain
    def getSubDomain(self,pt):
        return self.global_domain[pt[0]:pt[0]+3,pt[1]:pt[1]+3]
    def getInspectionDomain(self,inspection_point):
        return self.getSubDomain(inspection_point)
    def isDomainValid(self,inspection_point):
        dom=self.getInspectionDomain(inspection_point)
        for i in dom.shape:
            if (i!=domain_len):
                return False
        return True
    #evaluation system
    def countDiff(self,ref_dom,shift_dom):
        return np.count_nonzero(ref_dom-shift_dom)
    #if one needs 
    def getEvaluateValue(ref_dom,shift_mdom,size_of_dom):
        diff=ref_dom-shift_dom
        e_xy=0
        for row in range(size_of_dom):
            for col in range(size_of_dom):
                 e_xy+=abs(cmat[row,col]-smat[row,col])
        return e_xy
    #innner core algorithm
    def generateShiftMat(self,inspection_point,shift_vector):
        collect_point =inspection_point+shift_vector
        return self.getInspectionDomain(collect_point)

    def localMinimum(self,inspection_point):
        domain=self.getInspectionDomain(inspection_point)
        eval_list=[]
        for cand in self.shift_candidates:
            shifted_position=inspection_point+cand
            shift_domain=self.generateShiftMat(inspection_point,cand)
            if(self.isDomainValid(shifted_position)):
                eval_list.append(self.countDiff(domain,shift_domain))
        if(len(eval_list)!=0):
            return min(eval_list)
        else:
            return 0
    
    def cornerCriteriaUsingMoravec(self,inspection_point):
        eval_list=[]
        for i in np.arange(-1,2,1):
            for j in np.arange(-1,2,1):
                neighbor_point=np.array([inspection_point[0]+i,inspection_point[1]+j])
                if(self.isDomainValid(neighbor_point)):
                    eval_list.append(self.localMinimum(neighbor_point))
        return np.array(eval_list)
    
    def searchMaximumPoint(self):
        for j in range(global_domain.shape[0]):
            for i in range(global_domain.shape[1]):
                inspection_point=np.array([i,j])
                if self.isDomainValid(inspection_point):
                    eval_list=self.cornerCriteriaUsingMoravec(inspection_point)
                    index_center=math.floor((float(len(eval_list))/2))
                    if(np.argmax(eval_list)==index_center and eval_list[index_center]-min(eval_list)>1):
                        print(np.argmax(eval_list))
                        print('corner point at (%s , %s)' % (i+1,j+1))
                        print(eval_list.reshape(3,3))

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
    moravec=Moravec(global_domain,shift_candidates)
    moravec.searchMaximumPoint()
