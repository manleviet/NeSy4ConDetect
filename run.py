"""
Run experiments
@SNT
"""
from models.data import SingleConflictData

import argparse

from utils.hyperlist import dnn_grid

parser = argparse.ArgumentParser()
parser.add_argument('-task','--task', action='store', type=str, help='path to the task')

parser.add_argument('-model','--model',action='store',type=str,help='model used',required=True)

parser.add_argument('-op','--op',action='store',type=str,help='optimizer, only use with optimization approachs')

parser.add_argument('-lr','--lr',action='store',type=float,help='learning rate for the optimiser')

parser.add_argument('-batch_size','--batch_size',action='store',type=int,help='number of seed (initial) assignments')

parser.add_argument('-cvalue','--cvalue',action='store',type=float,help='confidence value')


args = parser.parse_args()

def logging(writer,fnum,params,param_grid,macc,sacc):
    row = [fnum]
    for param in param_grid:
        row.append(params[param])
        
    row += [macc,sacc]
    
    writer.writerow(row)
    

if __name__=="__main__":
    
    stime = time.time()
    
    # Prepare the log file
    taskname = os.path.basename(args.task)
    print(taskname)

    dlog = os.path.join("./results",taskname,args.model)

    print(dlog)

    if not os.path.isdir(dlog):
        os.makedirs(dlog)
        
    lfname  = os.path.join(dlog,"log.csv")
    logfile = open(lfname, 'a')
    writer = csv.writer(logfile)
    
    if os.path.getsize(lfname)==0:
        # creat header for log file
        write_header(writer,pgrid)


    # Create model and run
    if args.model=="dnn":
        experiment = dnn_run
        grid = dnn_grid
    elif args.model=="gnn":
        experiment = gnn_run
    elif args.model=="cnl":
        experiment = cnl_run
        hgrid = cnl_grid
    else:
        raise ValueError(args.model + " does not exist!!!")


    # hyper parameters search
    hgrid = ParameterGrid(hgrid)

    for hparams in hgrid:
        dataset = SingleConflict(arg.task)
        accs = []
        f1s  = []
        fold = 0
        while True:
            train_dataloader, test_dataloader = dataset.next_fold()
            if train_dataloader is None:
                break

        
            acc = experiment(train_dataloader,
                             test_dataloader,
                             hparams
                             kb=kb)

            accs.append(acc)
            fold +=1
            print("[ConDetect] Fold %d acc= "%(fold,acc))

        macc = mean(accs)
        sacc = std(accs)
        
        print("[ConDetect] Avg  acc= %.5f +- %.5f "%(macc,sacc))
        logging(writer,pgrid,macc,sacc)

    
    logfile.flush()
    logfile.close()
