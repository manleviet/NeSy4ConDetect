"""
Test DNN on conflict detection
Son N. Tran
"""
import os
import torch
from torch import nn
from torch.utils.data import DataLoader
import logging
import numpy as np


MAX_EPOCH = 200
#logging.basicConfig(filename = 'dnn.log',
#                    level = logging.INFO,
#                    format = '%(asctime)s:%(levelname)s:%(name)s:%(message)s')

device = {"cuda" if torch.cuda.is_available()
          else "cpu"
          }

device = "cpu"

class DNN(nn.Module):
    def __init__(self, nvar):
        super(DNN, self).__init__()
        self.linear = nn.Sequential(
            nn.Linear(nvar, 200),
            nn.ReLU(),
            nn.Linear(200, nvar),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.linear(x)
        return x


def train(model, train_dataloader, lr):
    optimizer = torch.optim.Adam(model.parameters(), lr = lr, betas = (0.9, 0.999))
    size = len(train_dataloader.dataset)
    for epoch in range(MAX_EPOCH):
        total_loss = 0
        for batch, (X, Y) in enumerate(train_dataloader):
            X, Y = X.to(device), Y.to(device)
            # Compute prediction error
            pred = model(X)

            # reorder constraints on the basis of the prediction
            # filter out the constraints that are not satisfied
            # TODO execute the conflict detection, using the output to calculate the accuracy

            loss = nn.BCELoss()(pred, Y)

            # Backpropagation
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            #if batch % 10 == 0:
            #    loss, current = loss.item(), batch * len(X)
            #    print(f"loss: {loss:>7f} [{current:>5d}/{size:>5d}]")

            total_loss += loss.item()
        print(f"epoch: {epoch:>5d}  loss:{loss:>7f}")


def test(model, test_dataloader):
    size = len(test_dataloader.dataset)
    model = model.to(device)
    model.eval()

    corrects = []
    with torch.no_grad():
        for X, Y in test_dataloader:
            X, Y = X.to(device), Y.to(device)
            pred = model(X)

            # print((torch.where(pred > 0.5, 1., 0.) == Y).sum(dim=1)==Y.shape[1])
            # print(X.shape)
            #input("")
            #corrects.append((torch.where(pred > 0.5, 1., 0.) == Y).sum(dim=0)) # CHECK
            res= (torch.where(pred > 0.5, 1., 0.) == Y).sum(dim=1)==Y.shape[1]
            print((torch.where(pred > 0.5, 1., 0.) == Y).sum(dim=1))
            print(Y.shape[1])

            # TODO execute the conflict detection, using the output to calculate the accuracy

            #print(res)
            #input("")
            corrects = np.append(corrects,res.tolist())

    #print(size)
    #print(corrects.shape)
    #print(corrects)
    acc = np.sum(corrects) / size
    #input("")
    return acc


def dnn_run(train_dataloader, test_dataloader, nvar, hparams, kb=None):
    model = DNN(nvar)
    train(model, train_dataloader, hparams['lr'])
    acc = test(model, test_dataloader)
    return acc
    
    
