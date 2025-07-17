import numpy as np

import nimfa2

V = np.random.rand(40, 100)
pmfcc = nimfa2.Pmfcc(V, seed="random_vcol", rank=10, max_iter=30,
                     theta=np.random.rand(V.shape[1], V.shape[1]))
pmfcc_fit = pmfcc()
