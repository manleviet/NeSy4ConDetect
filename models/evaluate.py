def accuracy(pred_Y,Y):
    sum(sum(abs(pred_Y - Y),axis=1)==0)
