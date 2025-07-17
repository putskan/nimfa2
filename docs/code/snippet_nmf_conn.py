import numpy as np

import nimfa2

V = np.random.rand(40, 100)
nmf = nimfa2.Nmf(V, rank=10, seed="random_vcol", max_iter=200, update='euclidean',
                 objective='conn', conn_change=40)
nmf_fit = nmf()
