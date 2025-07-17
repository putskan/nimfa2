import numpy as np

import nimfa2

V = np.random.rand(40, 100)
nmf = nimfa2.Nmf(V, seed="random_c", rank=10, max_iter=12, update='divergence',
                 objective='div')
nmf_fit = nmf()
