import numpy as np

import nimfa2

V = np.random.rand(40, 100)
nsnmf = nimfa2.Nsnmf(V, seed="random", rank=10, max_iter=12, theta=0.5)
nsnmf_fit = nsnmf()
