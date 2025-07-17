import numpy as np

import nimfa2

V = np.random.rand(40, 100)
pmf = nimfa2.Pmf(V, seed="random_vcol", rank=10, max_iter=12, rel_error=1e-5)
pmf_fit = pmf()
