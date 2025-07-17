import numpy as np

import nimfa2

V = np.random.rand(40, 100)
lfnmf = nimfa2.Lfnmf(V, seed=None, W=np.random.rand(V.shape[0], 10),
                     H=np.random.rand(10, V.shape[1]), rank=10, max_iter=12,
                     alpha=0.01)
lfnmf_fit = lfnmf()
