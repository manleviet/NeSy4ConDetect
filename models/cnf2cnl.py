"""
Encode CNF to Confidence Neural Logic (LBM version with PyTorch)
@Son N. Tran
"""
import glob
import numpy as np
from cnf import DIMACSReader
import tensorflow.compat.v1 as tf

def clause2sdnf(c,n_vars,conf_val,epsilon):
    sdnf = []
    c = np.array(c)
    W= None
    hb = np.array([])
    xb = np.zeros((n_vars))
    
    for i in range(len(c)):
        # variable elimination
        cclause = np.append(c[i],-1*c[i+1:])
        w = np.zeros((1,n_vars))
        s = np.sign(cclause)
        w[0,np.abs(cclause)-1] = s
        
        if W is None:
            W = w
        else:
            W = np.append(W,w,axis=0)
            
        b = -np.sum((s+1)/2)+epsilon
        hb = np.append(hb,[b])
        
        sdnf.append((cclause))

    
    params = {"W":W*conf_val, "hb":hb*conf_val, "xb":xb}
    
    return sdnf,params

def free_en(W,hb,x):
    inp = np.matmul(x,W) + hb
    #print(inp)
    fen = -np.sum(np.log(1+np.exp(inp)),axis=1)
    return fen

class RBMSAT():
    def __init__(self,cnf_reader,conf_val=None,epsilon=0.5):
        if conf_val is  None:
            self.conf_val_const = 1
        else:
            self.conf_val_const = conf_val
            
        self.conf_val_var  = conf_val
            
        self.epsilon = epsilon
        self.cnf_reader = cnf_reader
        self.build_model()

    def build_model(self):
        self.W  = None
        self.xb = 0
        self.hb = None
        i =  0
        self.clause2hinds = {}
        while self.cnf_reader.has_next():
            clause = self.cnf_reader.next_clause()
            sdnf,params = clause2sdnf(clause,self.cnf_reader.n_vars,self.conf_val_const,self.epsilon)
            if self.W is None:
                self.W  = params["W"]
                self.xb = params["xb"]
                self.hb = params["hb"]
                self.clause2hinds[i] = list(range(self.W.shape[0]))
            else:
                
                self.W  = np.append(self.W,params["W"],axis=0)
                self.xb += params["xb"]
                self.hb = np.append(self.hb,params["hb"])

                self.clause2hinds[i] = list(range(self.clause2hinds[i-1][-1]+1,self.W.shape[0]))
                
            i+=1
        print("Total %d of clauses have been encoded"%(i))
        self.W = np.transpose(self.W)

        # convert to tensorflow format
        self.W_tf = tf.convert_to_tensor(self.W,dtype=tf.float32)
        self.hb_tf = tf.convert_to_tensor(self.hb,dtype=tf.float32)
        self.xb_tf = tf.convert_to_tensor(self.xb,dtype=tf.float32)


    def has_sat(self,x,sigmoid=True,sigmoid_scale=1):
        if x.ndim==1:
            x = x[np.newaxis,:]
            
        if sigmoid:
            x = 1/(1+np.exp(-sigmoid_scale*x))
            
        hi = np.matmul(x,self.W) + self.hb
        sat_clause = (hi>0)*1.0
        total_sat_clause = np.sum(sat_clause,axis=1)
        numsat = np.max(total_sat_clause)

        assert numsat<= self.cnf_reader.n_clauses, "Number of satisfied clauses cannot larger than total clauses"
        has_sat = (numsat==self.cnf_reader.n_clauses)
        
        all_e_rank= -np.sum(hi*sat_clause,axis=1)
        e_rank = np.min(all_e_rank)
        fen = np.min(free_en(self.W,self.hb,x))
        total_sat_clause = np.max(total_sat_clause)
    
        return has_sat,e_rank,fen,total_sat_clause,all_e_rank

    def sat_graph_tf(self,x):
        hi = tf.matmul(x,self.W_tf) + self.hb_tf
        sat_clause = tf.cast(hi>0,tf.float32)
    
        total_sat_clause = tf.reduce_sum(sat_clause,axis=1)

        numsat = tf.reduce_max(total_sat_clause)

        #valid =  numsat> self.cnf_reader.n_clause
        #is_sat = (numsat==self.cnf_reader.n_clauses)
        
        e_ranks= -tf.reduce_sum(hi*sat_clause,axis=1)

        if tf.is_tensor(self.conf_val_var):
            hi = hi*self.conf_val_var[:,tf.newaxis]
            
        fe = -(tf.reduce_sum(self.xb_tf) + tf.reduce_sum(tf.log(1+tf.exp(hi)),axis=1))
        
        return fe,numsat,e_ranks
    
    def e_rank(self,x,sigmoid=False,sigmoid_scale=1):
        """
        Compute e_rank from the assignments x
        """
        if x.ndim==1:
            x = x[np.newaxis,:]

        if sigmoid:
            x = 1/(1+np.exp(-sigmoid_scale*x))

            
        i = np.matmul(x,self.W) + self.hb
        h = (i>0)*1.0

        """
        ## Forr debug
        self.truth_clauses  = {}
        for ci in self.clause2hinds:
            sdnf_true = np.sum(h[:,self.clause2hinds[ci]],axis=1)
            #print(ci)
            #print(sdnf_true)

            self.truth_clauses[ci] = sdnf_true 
          """ 
        e_rank = -(np.sum(i*h,axis=1) + np.sum(x*self.xb,axis=1))
        return e_rank

    
    def free_en(self,x,sigmoid=True,sigmoid_scale=1):
        """
        Compute free energy from the assignments x
        """
        if x.ndim ==1:
            x = x[np.newaxis,:]

        if sigmoid:
            x = 1/(1 + np.exp(-sigmoid_scale*x))

        
        i = np.matmul(x,self.W) + self.hb
      
        fe = -(np.sum(self.xb)  + np.sum(np.log(1+np.exp(i)),axis=1))
        return fe

    def free_en_tf(self,x):
        """
        Compute free energy from assignments  x
        Tensorflow format
        """
        i  = tf.matmul(x,self.W_tf) + self.hb_tf
        if tf.is_tensor(self.conf_val_var):
            i = i*self.conf_val_var[:,tf.newaxis]
            
        fe = -(tf.reduce_sum(self.xb_tf) + tf.reduce_sum(tf.log(1+tf.exp(i)),axis=1)) 
        return fe
    
    
if __name__=="__main__":
    fs = "../data/busybox/kb/busybox.dimacs"
    dr = DIMACSReader(fn)
    print(dr.n_vars)
    #rbmsat = RBMSAT(n)

