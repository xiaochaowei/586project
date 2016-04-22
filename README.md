# Weighted Matching in General Graphs

### Prerequisities

NetworkX is required:
```
pip install networkx
```

### Files
baseline.py -- Edmonds algorithm 1965<br/>
gabow.py – Edmonds algorithm improved by Gabow 1974<br/>
scaling.py – Duan-Pettie algorithm<br/>
greedymatching.py<br/>

### Running the tests
tests are in the test folder:<br/>
use following command to test:<br/>
```
python test[algorithm_name].py [graph_input]
```
For example:
```
python testBaseline.py sample_data/dense_n1000_e374362.p
```