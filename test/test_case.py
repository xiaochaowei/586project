from test3 import Matching
import math

# empty input graph
match = Matching()
match.initEdges([])
print (match.maxWeightmatching() == [])

match = Matching()
match.initEdges([ (0,1,1) ])
print (match.maxWeightmatching() == [1, 0])

match = Matching()
match.initEdges([ (1,2,10), (2,3,11) ])
print (match.maxWeightmatching()== [ -1, -1, 3, 2] )

match = Matching()
match.initEdges([ (1,2,5), (2,3,11), (3,4,5) ])
print (match.maxWeightmatching() == [ -1, -1, 3, 2, -1 ])

# maximum cardinality
match = Matching()
match.initEdges([ (1,2,5), (2,3,11), (3,4,5) ])
print (match.maxWeightmatching(True) == [ -1, 2, 1, 4, 3 ])

# floating point weigths
match = Matching()
match.initEdges([ (1,2,math.pi), (2,3,math.exp(1)), (1,3,3.0), (1,4,math.sqrt(2.0)) ])
print (match.maxWeightmatching() == [ -1, 4, 3, 2, 1 ])

# negative weights
print "test16_negative..."
match = Matching()
match.initEdges([ (1,2,2), (1,3,-2), (2,3,1), (2,4,-1), (3,4,-6) ])
print (match.maxWeightmatching(False) == [ -1, 2, 1, -1, -1 ])

print "test16_negative..."
match = Matching()
match.initEdges([ (1,2,2), (1,3,-2), (2,3,1), (2,4,-1), (3,4,-6) ])
print (match.maxWeightmatching(True) == [ -1, 3, 4, 1, 2 ])

# create S-blossom and use it for augmentation
print "test20_sblossom..."
match = Matching()
match.initEdges([ (1,2,8), (1,3,9), (2,3,10), (3,4,7) ])
print (match.maxWeightmatching() == [ -1, 2, 1, 4, 3 ])
print "test20_sblossom..."
matching = Matching()
match.initEdges([ (1,2,8), (1,3,9), (2,3,10), (3,4,7), (1,6,5), (4,5,6) ])
print (match.maxWeightmatching([ (1,2,8), (1,3,9), (2,3,10), (3,4,7), (1,6,5), (4,5,6) ]) == [ -1, 6, 3, 2, 5, 4, 1 ])

print "test21_s_nest..."
match= Matching()
match.initEdges([ (1,2,9), (1,3,8), (2,3,10), (1,4,5), (4,5,4), (1,6,3) ])
print (match.maxWeightmatching() == [ -1, 6, 3, 2, 5, 4, 1 ])

print "test21_s_nest..."
match = Matching()
match.initEdges([ (1,2,9), (1,3,8), (2,3,10), (1,4,5), (4,5,3), (1,6,4) ])
print (match.maxWeightmatching() == [ -1, 6, 3, 2, 5, 4, 1 ])

print "test21_s_nest..."
match = Matching()
match.initEdges([ (1,2,9), (1,3,8), (2,3,10), (1,4,5), (4,5,3), (3,6,4) ])
print (match.maxWeightmatching() == [ -1, 2, 1, 6, 5, 4, 3 ])

print "test22_s_nest..."
match = Matching()
match.initEdges([ (1,2,9), (1,3,9), (2,3,10), (2,4,8), (3,5,8), (4,5,10), (5,6,6) ])
print (match.maxWeightmatching() ==  [ -1, 3, 4, 1, 2, 6, 5 ])

# create S-blossom, relabel as S, include in nested S-blossom
print "test23_s_relabel_nest..."
match = Matching()
match.initEdges([ (1,2,10), (1,7,10), (2,3,12), (3,4,20), (3,5,20), (4,5,25), (5,6,10), (6,7,10), (7,8,8) ])
print (match.maxWeightmatching() == [ -1, 2, 1, 4, 3, 6, 5, 8, 7 ])

# create nested S-blossom, augment, expand recursively
print "test24_s_nest_expand(self)..."
match = Matching()
match.initEdges([ (1,2,8), (1,3,8), (2,3,10), (2,4,12), (3,5,12), (4,5,14), (4,6,12), (5,7,12), (6,7,14), (7,8,12) ])
print (match.maxWeightmatching() == [ -1, 2, 1, 5, 6, 3, 4, 8, 7 ])

# create S-blossom, relabel as T, expand
print "test25_s_t_expand(self)...."
match = Matching()
match.initEdges([ (1,2,23), (1,5,22), (1,6,15), (2,3,25), (3,4,22), (4,5,25), (4,8,14), (5,7,13) ])
print match.maxWeightmatching()
print (match.maxWeightmatching() == [ -1, 6, 3, 2, 8, 7, 1, 5, 4 ])
# print "[ -1, 6, 3, 2, 8, 7, 1, 5, 4 ]"

print "test26_s_nest_t_expand(self)..."
match = Matching()
match.initEdges([ (1,2,19), (1,3,20), (1,8,8), (2,3,25), (2,4,18), (3,5,18), (4,5,13), (4,7,7), (5,6,7) ])
print (match.maxWeightmatching() == [ -1, 8, 3, 2, 7, 6, 5, 4, 1 ])

#    create nested S-blossom, relabel as T, expand
#    self.assertEqual(maxWeightMatching([ (1,2,19), (1,3,20), (1,8,8), (2,3,25), (2,4,18), (3,5,18), (4,5,13), (4,7,7), (5,6,7) ]), [ -1, 8, 3, 2, 7, 6, 5, 4, 1 ])

# def test30_tnasty_expand(self):
# create blossom, relabel as T in more than one way, expand, augment
match = Matching()
match.initEdges([ (1,2,45), (1,5,45), (2,3,50), (3,4,45), (4,5,50), (1,6,30), (3,9,35), (4,8,35), (5,7,26), (9,10,5) ])
print (match.maxWeightmatching() == [ -1, 6, 3, 2, 8, 7, 1, 5, 4, 10, 9 ])

# def test31_tnasty2_expand(self):
# again but slightly different
match = Matching()
match.initEdges([ (1,2,45), (1,5,45), (2,3,50), (3,4,45), (4,5,50), (1,6,30), (3,9,35), (4,8,26), (5,7,40), (9,10,5) ])
print (match.maxWeightmatching() == [ -1, 6, 3, 2, 8, 7, 1, 5, 4, 10, 9 ])

# def test32_t_expand_leastslack(self):
# create blossom, relabel as T, expand such that a new least-slack S-to-free edge is produced, augment
match = Matching()
match.initEdges([ (1,2,45), (1,5,45), (2,3,50), (3,4,45), (4,5,50), (1,6,30), (3,9,35), (4,8,28), (5,7,26), (9,10,5) ])
# print match.maxWeightmatching(), "[ -1, 6, 3, 2, 8, 7, 1, 5, 4, 10, 9 ]"
print (match.maxWeightmatching() == [ -1, 6, 3, 2, 8, 7, 1, 5, 4, 10, 9 ])

# def test33_nest_tnasty_expand(self):
# create nested blossom, relabel as T in more than one way, expand outer blossom such that inner blossom ends up on an augmenting path
print "test33_nest_tnasty_expand..."
match = Matching()
match.initEdges([ (1,2,45), (1,7,45), (2,3,50), (3,4,45), (4,5,95), (4,6,94), (5,6,94), (6,7,50), (1,8,30), (3,11,35), (5,9,36), (7,10,26), (11,12,5) ])
print (match.maxWeightmatching() == [ -1, 8, 3, 2, 6, 9, 4, 10, 1, 5, 7, 12, 11 ])

# def test34_nest_relabel_expand(self):
# create nested S-blossom, relabel as S, expand recursively
match = Matching()
match.initEdges([ (1,2,40), (1,3,40), (2,3,60), (2,4,55), (3,5,55), (4,5,50), (1,8,15), (5,7,30), (7,6,10), (8,10,10), (4,9,30) ])
print (match.maxWeightmatching() == [ -1, 2, 1, 5, 9, 3, 7, 6, 10, 4, 8 ])
