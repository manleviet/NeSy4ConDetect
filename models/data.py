"""
Read conflict data
@SNT
"""
import numpy as np
import os
import glob

import torch

from sklearn.model_selection import KFold
from torch.utils.data import Dataset, DataLoader


class SingleConflictData():
    def __init__(self,dpath,batch_size=16,nfold=None):
        """
        Use leave-one-out
        """
        self.X, self.Y = load_single_conflict_data(dpath)
        self.nvar = self.X.shape[1]
        self.kb = load_knowledge(dpath)
        self.batch_size = batch_size
        
        self.fid = 0
        if nfold is None:
            self.nfold = self.X.shape[0]
        else:
            self.nfold = nfold
            
        self.kfold = list(KFold(n_splits=self.nfold, shuffle=True).split(self.X))
        
    def next_data_fold(self):
        if self.fid >= self.nfold:
            return None, None

        
        train_ids, test_ids = self.kfold[self.fid]
        #print(train_ids)
        #print(test_ids)
        #input("")
        self.fid+=1
        

        # convert into PyTorch tensors
        Xtrain = torch.tensor(self.X[train_ids,:], dtype=torch.float32)
        Ytrain = torch.tensor(self.Y[train_ids,:], dtype=torch.float32)
         
        train_dataloader = DataLoader(list(zip(Xtrain,Ytrain)), shuffle=True, batch_size=self.batch_size)

        
        Xtest = torch.tensor(self.X[test_ids,:], dtype=torch.float32)
        Ytest = torch.tensor(self.Y[test_ids,:], dtype=torch.float32)

        test_dataloader = DataLoader(list(zip(Xtest,Ytest)),batch_size=self.batch_size)

        return train_dataloader, test_dataloader
    
def load_single_conflict_data(datapath):
    X,Y =  load_data(datapath)
    X = X[:,1:]
    Y = np.abs(Y[:,1:])

    return X,Y

def load_data(datapath):
    inv_con_file = glob.glob(os.path.join(datapath,"invalid_confs_*.csv"))[0]
    
    con_file = glob.glob(os.path.join(datapath,"conflicts_*.csv"))[0]
    
    X = np.genfromtxt(inv_con_file,delimiter=",")
    
    Y = np.genfromtxt(con_file,delimiter=",")


    return X,Y
    
def load_knowledge(datapath):
    
    #TODO
    return None


def check_data(datapath):
    X,Y = load_data(datapath)
    
    if (X.shape[0] == Y.shape[0]) and (X.shape[1] == Y.shape[1]):
        print("Number of rows: ", X.shape[0], " Number of cols: ", X.shape[1])

    # conflict sizes
    csizes = np.sum(abs(Y[:,1:]),axis=1)
    print("conflict set sizes: ", min(csizes),"-", max(csizes))

    # conflicts per sample
    #[ids,freqs] = hist(X[:,0])
    hist = {}
    for id in X[:,0]:
        if id not in hist:
            hist[id] = 1
        else:
            hist[id] += 1
            
    ids = list(hist.keys())
    freqs = list(hist.values())
    print("conflicts per sample:", min(freqs), "-", max(freqs))

    
if __name__=="__main__":
    datapath = "../data/busybox/655"
    check_data(datapath)
    

