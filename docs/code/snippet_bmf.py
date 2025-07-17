import numpy as np

import nimfa2

V = np.random.rand(40, 100)
bmf = nimfa2.Bmf(V, seed="nndsvd", rank=10, max_iter=12, lambda_w=1.1, lambda_h=1.1)
bmf_fit = bmf()
