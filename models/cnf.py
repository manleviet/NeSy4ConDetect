"""
Read CNF
@Son N. Tran
"""
import numpy as np
import glob
import pickle
import os
#import mk_problem
#import tensorflow as tf

def extract_groundtruth(fname):
    try:
        inx = fname.index("sat=")
        is_sat = int(fname[inx + 4]) == 1
    except:
        is_sat = None

    return is_sat


class DIMACSReader:
    def __init__(self,fpath):
        self.fpath = fpath
        self.clauses = None
        self.f = None
        self.read_meta()

    def read_meta(self):
        if self.f is not None:
            self.f.close()
            self.f = None

        fname = os.path.basename(self.fpath)
        self.is_sat = extract_groundtruth(fname)
        self.f = open(self.fpath,"rb")
        while True:
            line = self.f.readline()
            if line is None or len(line)<=0:
                break
            line = line.decode('utf-8')
            #print(line)
            if line[0]=='c': # comment
                continue
            elif line[0] =='p':
                strs =  line.split(" ")
                self.n_vars = int(strs[2])
                self.n_clauses = int(strs[3])
                break

    def has_next(self):
        if self.f is None:
            return False
        line = self.f.readline()
        line = line.decode('utf-8')
        if line is None or len(line)==0:
            self.f.close()
            self.f = None
            return False
        else:
            #print(line)
            self.clause = [int(x) for x in line.split(" ")[:-1]]
            return True

    def next_clause(self):
        return self.clause


if __name__ == "__main__":
    kb = "../data/busybox/kb/busybox.dimacs"
    dr = DIMACSReader(kb)

    i = 0
    while dr.has_next():
        clause = dr.next_clause()
        print(clause)
        i += 1
    
