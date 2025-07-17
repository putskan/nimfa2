import numpy as np

import nimfa2

V = np.random.rand(40, 100)
nmf = nimfa2.Nmf(V, seed="nndsvd", rank=10, max_iter=12, update='euclidean',
                 objective='fro')
nmf_fit = nmf()
