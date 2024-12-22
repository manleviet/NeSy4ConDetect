"""
Run experiments
@SNT
"""
from models.cnf2cnl_pytorch import cnl_run
from models.data import SingleConflictData
from models.dnn import dnn_run
from utils.hyperlist import dnn_grid, cnl_grid
import numpy as np

from sklearn.model_selection import ParameterGrid

import argparse
import time
import os
import csv

parser = argparse.ArgumentParser()

parser.add_argument('-task', '--task', action='store', type=str, help='path to the task')

parser.add_argument('-kb', '--kb', action='store', type=str, help='path to the dimacs file')

parser.add_argument('-model', '--model', action='store', type=str, help='model used', required=True)

parser.add_argument('-op', '--op', action='store', type=str, help='optimizer, only use with optimization approachs')

parser.add_argument('-lr', '--lr', action='store', type=float, help='learning rate for the optimiser')

parser.add_argument('-batch_size', '--batch_size', action='store', type=int,
                    help='number of seed (initial) assignments')

parser.add_argument('-cvalue', '--cvalue', action='store', type=float, help='confidence value')


args = parser.parse_args()

def write_header(writer, param_grid):
    header = []
    for param in param_grid:
        header.append(param)

    header += ["Test Acc", "STD"]

    writer.writerow(header)


def logging(writer, params, param_grid, macc, sacc):
    row = []
    for param in param_grid:
        row.append(params[param])

    row += [macc, sacc]

    writer.writerow(row)


if __name__ == "__main__":

    stime = time.time()

    # Prepare the log file
    taskname = os.path.basename(args.task)
    print(taskname)

    dlog = os.path.join("./results", taskname, args.model)

    print(dlog)

    if not os.path.isdir(dlog):
        os.makedirs(dlog)

    lfname = os.path.join(dlog, "log.csv")
    logfile = open(lfname, 'a')
    writer = csv.writer(logfile)

    # Create model and run
    if args.model == "dnn":
        experiment = dnn_run
        hgrid = dnn_grid
    elif args.model == "gnn":
        experiment = gnn_run
    elif args.model == "cnl":
        experiment = cnl_run
        hgrid = cnl_grid
    else:
        raise ValueError(args.model + " does not exist!!!")

    if os.path.getsize(lfname) == 0:
        # create header for log file
        write_header(writer, hgrid)

    # hyperparameters search
    for hparams in ParameterGrid(hgrid):
        if args.model == "cnl":
            task = SingleConflictData(args.task, kbpath=args.kb, batch_size=hparams["bsize"], nfold=10)
        else:
            task = SingleConflictData(args.task, kbpath=None, batch_size=hparams["bsize"], nfold=10)
        accs = []
        f1s = []
        fold = 0
        while True:
            train_dataloader, test_dataloader = task.next_data_fold()
            if train_dataloader is None:
                break

            acc = experiment(train_dataloader,
                             test_dataloader,
                             task.nvar,
                             hparams,
                             kb=task.kb)

            accs.append(acc)
            fold += 1
            print("[ConDetect] Fold %d acc= %.5f" % (fold, acc))
            # input("")
        macc = np.mean(accs)
        sacc = np.std(accs)

        print("[ConDetect] Avg  acc= %.5f +- %.5f " % (macc, sacc))
        print(hparams)
        print(hgrid)
        logging(writer, hparams, hgrid, macc, sacc)

    logfile.flush()
    logfile.close()
