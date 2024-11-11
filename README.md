# NeSy4ConDetect


busybox-1.18.0.xml - original knowledge base  - feature model (no need)

busybox-1.18.0.txt - CNF of knowledge base

busybox.dimacs - knowledge in dimacs

allConflictSets.da - list of conflict sets



sau khi train thì đầu vào sẽ là một conflict user requirement, dạng feature1=true, feature2=false, ...

đầu ra, mình muốn là một diagnosis, ví dụ, feature11=true và feature12=true là một conflict. Thì nó sẽ có 2 diagnoses là {feature11=true} và {feature12=true}.

## busybox

bao gồm 854 features/variables
allConflictSets.da chứa 161 conflict sets

Input: invalid_confs.csv
Output: conflicts.csv

## 655

655 rows
855 columns
First column - id

one conflict set for each invalid configuration.

## 126725

126725 rows
855 columns
First column - id

one invalid configurations have multiple conflict sets.
each row is a conflict set.