"""
Test DNN on conflict detection
Son N. Tran
"""
import os
import torch
from torch import nn
from torch.utils.data import DataLoader
import logging

#logging.basicConfig(filename = 'dnn.log',
#                    level = logging.INFO,
#                    format = '%(asctime)s:%(levelname)s:%(name)s:%(message)s')

device = {"cuda" if torch.cuda.is_available()
          else "mps" if torch.backend.mps.is_available()
          else "cpu"
          }

class DNN(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.linear = nn.Sequential(
            nn.Linear(2, 20),
            nn.Tanh(),
            nn.Linear(20, 2),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.linear(x)
        return x


def train(model,train_dataloader):

    for epoch in range(MAX_EPOCH):
        for batch, (X, y) in enumerate(dataloader):   
            X, y = X.to(device), y.to(device)
            # Compute prediction error
            pred = model(X)

            loss = loss_fn(pred, y)
        
            # Backpropagation
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if batch % 100 == 0:
                loss, current = loss.item(), batch * len(X)
                print(f"loss: {loss:>7f} [{current:>5d}/{size:>5d}]")

            logging.info(str(epoch)+ ","
                         + str(epoch_loss) + ", "
                         + str(epoch_accu) + ","
                         + str(test_accu) + ","
                         + str(sparsity))
                    

def test(model,test_dataloader):
        size = len(dataloader.dataset)
        model = model.to(device)
        model.eval()

        corrects = []
        with torch.no_grad():
            for X, Y in dataloader:
                X, Y = X.to(device), Y.to(device)
                pred = model(X)
                
                corrects.append((torch.where(pred > 0.5, 1., 0.) == Y).sum(dim=0)) # CHECK
                
        acc = mean(corrects) 
        
        return acc

def dnn_run(train_dataloader,test_dataloader,hparams,kb=None):
    model = DNN()
    train(model,train_dataloader,hparams['lr'])
    acc = test(model,test_dataloader)
    return acc
    
    
