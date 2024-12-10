"""
Read conflict data
@SNT
"""
import numpy as np
import os
from sklearn.model_selection import KFold
from torch.utils.data import Dataset, DataLoader


class SingleConflictData():
    def __init__(self,dpath,nfold=None):
        """
        Use leave-one-out
        """
        self.dataset = load_single_conflict_data(dpath)
        self.kb = loadknowledge(dpath)
        self.dsource = os.path.dirname(args.db)
        self.tname = os.path.basename(args.dnf)
        self.fid = 0
        if nfold is None:
            nfold = self.X.shape[0]
            
        self.kfold = KFold(n_splits=nfold, shuffle=True).split(self.dataset)
        
    def next_fold(self):
        if self.fid >= self.X.shape[0]:
            return None, None

        train_ids, test_ids = self.kfold[self.fid]
        self.fid+=1
        

        # convert into PyTorch tensors
        Xtrain = torch.tensor(X[train_ids,:], dtype=torch.float32)
        Ytrain = torch.tensor(Y[train_ids,:], dtype=torch.float32)

        train_dataloader = DataLoader(list(zip(Xtrain,Ytrain)), shuffle=True, batch_size=16)


        Xtest = torch.tensor(X[test_ids,:], dtype=torch.float32)
        Ytest = torch.tensor(Y[test_ids,:], dtype=torch.float32)

        test_dataloader = DataLoader(list(zip(Xtest,Ytest)))

        return trainloader, testloader
    

def load_single_conflict_data(datasource,dataid):
    X = np.genfromtxt(os.path.join("../data/"+datasource,dataid,"invalid_confs_"+dataid+".csv"),delimiter=",")
    
    Y = np.genfromtxt(os.path.join("../data/"+datasource,dataid,"conflicts_"+dataid+".csv"),delimiter=",")


    return dataset
    
    
def check_data(datasource,dataid):
    X,Y = loadfiles(datasource,dataid)
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
    datasource = "arcade"
    dataid = "48752"

    check_data(datasource,dataid)
    

