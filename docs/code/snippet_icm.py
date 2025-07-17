import numpy as np

import nimfa2

V = np.random.rand(40, 100)
icm = nimfa2.Icm(V, seed="nndsvd", rank=10, max_iter=12, iiter=20,
                 alpha=np.random.randn(V.shape[0], 10), beta=np.random.randn(10, V.shape[1]),
                 theta=0., k=0., sigma=1.)
icm_fit = icm()
