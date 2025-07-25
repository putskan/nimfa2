
"""
###################################
Icm (``methods.factorization.icm``)
###################################

**Iterated Conditional Modes nonnegative matrix factorization (ICM)**
[Schmidt2009]_.

Iterated conditional modes algorithm is a deterministic algorithm for obtaining
the configuration that maximizes the joint probability of a Markov random field.
This is done iteratively by maximizing the probability of each variable
conditioned on the rest.

Most NMF algorithms can be seen as computing a maximum likelihood or maximum a
posteriori (MAP) estimate of the nonnegative factor matrices under some
assumptions on the distribution of the data and factors. ICM algorithm computes
the MAP estimate. In this approach, iterations over the parameters of the model
set each parameter equal to the conditional mode and after a number of
iterations the algorithm converges to a local maximum of the joint posterior
density. This is a block coordinate ascent algorithm with the benefit that the
optimum is computed for each block of parameters in each iteration.

ICM has low computational cost per iteration as the modes of conditional
densities have closed form expressions.

In [Schmidt2009]_ ICM is compared to the popular Lee and Seung's multiplicative
update algorithm and fast Newton algorithm on image feature extraction test.
ICM converges much faster than multiplicative update algorithm and with
approximately the same rate per iteration as fast Newton algorithm. All three
algorithms have approximately the same computational cost per iteration.

.. literalinclude:: /code/snippet_icm.py

"""

from nimfa2.models import *
from nimfa2.utils import *
from nimfa2.utils.linalg import *

__all__ = ['Icm']


class Icm(nmf_std.Nmf_std):
    """
    :param V: The target matrix to estimate.
    :type V: Instance of the :class:`scipy.sparse` sparse matrices types,
       :class:`numpy.ndarray`, :class:`numpy.matrix` or tuple of instances of
       the latter classes.

    :param seed: Specify method to seed the computation of a factorization. If
       specified :param:`W` and :param:`H` seeding must be None. If neither seeding
       method or initial fixed factorization is specified, random initialization is
       used.
    :type seed: `str` naming the method or :class:`methods.seeding.nndsvd.Nndsvd`
       or None

    :param W: Specify initial factorization of basis matrix W. Default is None.
       When specified, :param:`seed` must be None.
    :type W: :class:`scipy.sparse` or :class:`numpy.ndarray` or
       :class:`numpy.matrix` or None

    :param H: Specify initial factorization of mixture matrix H. Default is None.
       When specified, :param:`seed` must be None.
    :type H: Instance of the :class:`scipy.sparse` sparse matrices types,
       :class:`numpy.ndarray`, :class:`numpy.matrix`, tuple of instances of the
       latter classes or None

    :param rank: The factorization rank to achieve. Default is 30.
    :type rank: `int`

    :param n_run: It specifies the number of runs of the algorithm. Default is
       1. If multiple runs are performed, fitted factorization model with the
       lowest objective function value is retained.
    :type n_run: `int`

    :param callback: Pass a callback function that is called after each run when
       performing multiple runs. This is useful if one wants to save summary
       measures or process the result before it gets discarded. The callback
       function is called with only one argument :class:`models.mf_fit.Mf_fit` that
       contains the fitted model. Default is None.
    :type callback: `function`

    :param callback_init: Pass a callback function that is called after each
       initialization of the matrix factors. In case of multiple runs the function
       is called before each run (more precisely after initialization and before
       the factorization of each run). In case of single run, the passed callback
       function is called after the only initialization of the matrix factors.
       This is useful if one wants to obtain the initialized matrix factors for
       further analysis or additional info about initialized factorization model.
       The callback function is called with only one argument
       :class:`models.mf_fit.Mf_fit` that (among others) contains also initialized
       matrix factors. Default is None.
    :type callback_init: `function`

    :param track_factor: When :param:`track_factor` is specified, the fitted
        factorization model is tracked during multiple runs of the algorithm. This
        option is taken into account only when multiple runs are executed
        (:param:`n_run` > 1). From each run of the factorization all matrix factors
        are retained, which can be very space consuming. If space is the problem
        setting the callback function with :param:`callback` is advised which is
        executed after each run. Tracking is useful for performing some quality or
        performance measures (e.g. cophenetic correlation, consensus matrix,
        dispersion). By default fitted model is not tracked.
    :type track_factor: `bool`

    :param track_error: Tracking the residuals error. Only the residuals from
        each iteration of the factorization are retained. Error tracking is not
        space consuming. By default residuals are not tracked and only the final
        residuals are saved. It can be used for plotting the trajectory of the
        residuals.
    :type track_error: `bool`

    :param iiter: Number of inner iterations. Default is 20.
    :type iiter: `int`

    :param alpha: The prior for basis matrix (W) of proper dimensions. Default
       is uniformly distributed random sparse matrix prior with 0.8 density
       parameter.
    :type alpha: :class:`scipy.sparse.csr_matrix` or :class:`numpy.matrix`

    :param beta: The prior for mixture matrix (H) of proper dimensions.
       Default is uniformly distributed random sparse matrix prior with 0.8 density
       parameter.
    :type beta: :class:`scipy.sparse.csr_matrix` or :class:`numpy.matrix`

    :param theta: The prior for :param:`sigma`. Default is 0.
    :type theta: `float`

    :param k: The prior for :param:`sigma`. Default is 0.
    :type k: `float`

    :param sigma: Initial value for noise variance (sigma**2). Default is 1.
    :type sigma: `float`

    **Stopping criterion**

    Factorization terminates if any of specified criteria is satisfied.

    :param max_iter: Maximum number of factorization iterations. Note that the
       number of iterations depends on the speed of method convergence. Default
       is 30.
    :type max_iter: `int`

    :param min_residuals: Minimal required improvement of the residuals from the
       previous iteration. They are computed between the target matrix and its MF
       estimate using the objective function associated to the MF algorithm.
       Default is None.
    :type min_residuals: `float`

    :param test_conv: It indicates how often convergence test is done. By
       default convergence is tested each iteration.
    :type test_conv: `int`
    """
    def __init__(self, V, seed=None, W=None, H=None, H1=None,
                 rank=30, max_iter=30, min_residuals=1e-5, test_conv=None,
                 n_run=1, callback=None, callback_init=None, track_factor=False,
                 track_error=False, iiter=20, alpha=None, beta=None, theta=0.,
                 k=0., sigma=1., **options):
        self.name = "icm"
        self.aseeds = ["random", "fixed", "nndsvd", "random_c", "random_vcol"]
        nmf_std.Nmf_std.__init__(self, vars())
        if self.alpha is None:
            self.alpha = sp.rand(self.V.shape[0], self.rank, density=0.8, format='csr')
        self.alpha= self.alpha.tocsr() if sp.isspmatrix(self.alpha) else np.asarray(self.alpha)
        if self.beta is None:
            self.beta = sp.rand(self.rank, self.V.shape[1], density=0.8, format='csr')
        self.beta = self.beta.tocsr() if sp.isspmatrix(self.beta) else np.asarray(self.beta)
        self.tracker = mf_track.Mf_track() if self.track_factor and self.n_run > 1 \
                                              or self.track_error else None

    def factorize(self):
        """
        Compute matrix factorization.
         
        Return fitted factorization model.
        """
        self.v = multiply(self.V, self.V).sum() / 2.

        for run in range(self.n_run):
            self.W, self.H = self.seed.initialize(
                self.V, self.rank, self.options)
            p_obj = c_obj = sys.float_info.max
            best_obj = c_obj if run == 0 else best_obj
            iter = 0
            if self.callback_init:
                self.final_obj = c_obj
                self.n_iter = iter
                mffit = mf_fit.Mf_fit(self)
                self.callback_init(mffit)
            while self.is_satisfied(p_obj, c_obj, iter):
                p_obj = c_obj if not self.test_conv or iter % self.test_conv == 0 else p_obj
                self.update()
                iter += 1
                c_obj = self.objective(
                ) if not self.test_conv or iter % self.test_conv == 0 else c_obj
                if self.track_error:
                    self.tracker.track_error(run, c_obj)
            if self.callback:
                self.final_obj = c_obj
                self.n_iter = iter
                mffit = mf_fit.Mf_fit(self)
                self.callback(mffit)
            if self.track_factor:
                self.tracker.track_factor(
                    run, W=self.W, H=self.H, final_obj=c_obj, n_iter=iter)
            # if multiple runs are performed, fitted factorization model with
            # the lowest objective function value is retained
            if c_obj <= best_obj or run == 0:
                best_obj = c_obj
                self.n_iter = iter
                self.final_obj = c_obj
                mffit = mf_fit.Mf_fit(copy.deepcopy(self))

        mffit.fit.tracker = self.tracker
        return mffit

    def is_satisfied(self, p_obj, c_obj, iter):
        """
        Compute the satisfiability of the stopping criteria based on stopping
        parameters and objective function value.
        
        Return logical value denoting factorization continuation. 
        
        :param p_obj: Objective function value from previous iteration. 
        :type p_obj: `float`
        :param c_obj: Current objective function value.
        :type c_obj: `float`
        :param iter: Current iteration number. 
        :type iter: `int`
        """
        if self.max_iter and self.max_iter <= iter:
            return False
        if self.test_conv and iter % self.test_conv != 0:
            return True
        if self.min_residuals and iter > 0 and p_obj - c_obj < self.min_residuals:
            return False
        if iter > 0 and c_obj > p_obj:
            return False
        return True

    def update(self):
        """Update basis and mixture matrix."""
        # update basis matrix
        C = dot(self.H, self.H.T)
        D = dot(self.V, self.H.T)
        for _ in range(self.iiter):
            for n in range(self.rank):
                nn = list(range(n)) + list(range(n + 1, self.rank))
                op1 = D[:, n] - dot(self.W[:, nn], C[nn, n]) - self.sigma * self.alpha[:, n]
                op2 = C[n, n] + np.finfo(C.dtype).eps
                temp = max(sop(op1, op2, div), 0.)
                if not sp.isspmatrix(self.W):
                    self.W[:, n] = temp
                else:
                    for i in range(self.W.shape[0]):
                        self.W[i, n] = temp[i, 0]
        # 0/1 values special handling
        #l = np.logical_or((self.W == 0).all(0), (self.W == 1).all(0))
        #lz = len(nz_data(l))
        #l = [i for i in xrange(self.rank) if l[0, i] == True]
        #self.W[:, l] = multiply(repmat(self.alpha.mean(1), 1, lz), -np.log(np.random.rand(self.V.shape[0], lz)))
        # update sigma
        self.sigma = (self.theta + self.v + multiply(self.W, dot(self.W, C) - 2 * D).sum() / 2.) / \
            (self.V.shape[0] * self.V.shape[1] / 2. + self.k + 1.)
        # update mixture matrix
        E = dot(self.W.T, self.W)
        F = dot(self.W.T, self.V)
        for _ in range(self.iiter):
            for n in range(self.rank):
                nn = list(range(n)) + list(range(n + 1, self.rank))
                op1 = F[n, :] - dot(E[n, nn], self.H[nn, :]) - self.sigma * self.beta[n, :]
                op2 = E[n, n] + np.finfo(E.dtype).eps
                temp = max(sop(op1, op2, div), 0.)
                if not sp.isspmatrix(self.H):
                    self.H[n, :] = temp
                else:
                    for i in range(self.H.shape[1]):
                        self.H[n, i] = temp[0, i]
        # 0/1 values special handling
        #l = np.logical_or((self.H == 0).all(1), (self.H == 1).all(1))
        #lz = len(nz_data(l))
        #l = [i for i in xrange(self.rank) if l[i, 0] == True]
        #self.H[l, :] = multiply(repmat(self.beta.mean(0), lz, 1), -np.log(np.random.rand(lz, self.V.shape[1])))

    def objective(self):
        """Compute squared Frobenius norm of a target matrix and its NMF estimate."""
        return power(self.V - dot(self.W, self.H), 2).sum()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
