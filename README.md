# NeSy4ConDetect


busybox-1.18.0.xml - original knowledge base  - feature model (no need)

busybox-1.18.0.txt - CNF of knowledge base

busybox.dimacs - knowledge in dimacs

allConflictSets.da - list of conflict sets



sau khi train thì đầu vào sẽ là một conflict user requirement, dạng feature1=true, feature2=false, ...

đầu ra, mình muốn là một diagnosis, ví dụ, feature11=true và feature12=true là một conflict. Thì nó sẽ có 2 diagnoses là {feature11=true} và {feature12=true}.

## busybox
bao gồm tổng cộng 854 features

chỉ xét 683 features/variables (leaf features)
allConflictSets.da chứa 161 conflict sets

Input: invalid_confs.csv
Output: conflicts.csv

## 655.zip

655 rows 
684 columns
First column - id

one conflict set for each invalid configuration.

conflict set sizes:  1.0 - 4.0
conflicts per sample: 1 - 1
 
## 126725.zip

126725 rows
684 columns
First column - id

one invalid configurations have multiple conflict sets.
each row is a conflict set.

conflict set sizes:  1.0 - 4.0
conflicts per sample: 1 - 32

## arcade-game
bao gồm tổng cộng 61 features

chỉ xét 47 features/variables (leaf features)
allConflictSets.da chứa 142 conflict sets

### 410.zip

410 rows
48 columns
First column - id

one conflict set for each invalid configuration.

conflict set sizes:  1.0 - 6.0
conflicts per sample: 1 - 1

### 48752.zip

48752 rows
48 columns
First column - id

one invalid configurations have multiple conflict sets.
each row is a conflict set.

conflict set sizes:  1.0 - 7.0
conflicts per sample: 1 - 16


