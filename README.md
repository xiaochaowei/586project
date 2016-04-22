# Weighted Matching in General Graphs

### Prerequisities

NetworkX is required:
```
pip install networkx
```

### Files
baseline.py - Edmonds algorithm 1965<br/>
gabow.py - Edmonds algorithm improved by Gabow 1974<br/>
scaling.py - Duan-Pettie algorithm<br/>
greedymatching.py - Greedy algorithm<br/>

### Running the tests
tests are in the test folder:<br/>
#### 1. Wall clock running time tests:<br/>
This test designed to measure the wall clock running time.
use following command to test:<br/>
```
python test[algorithm_name].py [graph_input]
```
For example:
```
python testBaseline.py sample_data/dense_n1000_e374362.p
```
Note, the epsilon value can be changed by modify the parameter of the function <em>maxWeightmatching(eps)</em> in testScale.py, by default it is set to 1/16.

#### 2. Approximating algorithm accuracy test:
This test designed to test approximation accuracy of the Duan-Pettie algorithm and the Greedy algorithm.  It tests on 1000 randomly generated graphs and compute the average error.

```
python random_small_graph_approx_test.py
```

