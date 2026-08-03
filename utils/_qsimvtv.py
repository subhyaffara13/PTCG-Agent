import math


def _qsimvtv(m, nu, sigma, a, b, rng):
    """Estimates the multivariate t CDF using randomized QMC

    Parameters
    ----------
    m : int
        The number of points
    nu : float
        Degrees of freedom
    sigma : ndarray
        A 2D positive semidefinite covariance matrix
    a : ndarray
        Lower integration limits
    b : ndarray
        Upper integration limits.
    rng : Generator
        Pseudorandom number generator

    Returns
    -------
    p : float
        The estimated CDF.
    e : float
        An absolute error estimate.

    """
    # _qsimvtv is a Python translation of the Matlab function qsimvtv,
    # semicolons and all.
    #
    #   This function uses an algorithm given in the paper
    #      "Comparison of Methods for the Numerical Computation of
    #       Multivariate t Probabilities", in
    #      J. of Computational and Graphical Stat., 11(2002), pp. 950-971, by
    #          Alan Genz and Frank Bretz
    #
    #   The primary references for the numerical integration are
    #    "On a Number-Theoretical Integration Method"
    #    H. Niederreiter, Aequationes Mathematicae, 8(1972), pp. 304-11.
    #    and
    #    "Randomization of Number Theoretic Methods for Multiple Integration"
    #     R. Cranley & T.N.L. Patterson, SIAM J Numer Anal, 13(1976), pp. 904-14.
    #
    #   Alan Genz is the author of this function and following Matlab functions.
    #          Alan Genz, WSU Math, PO Box 643113, Pullman, WA 99164-3113
    #          Email : alangenz@wsu.edu
    #
    # Copyright (C) 2013, Alan Genz,  All rights reserved.
    #
    # Redistribution and use in source and binary forms, with or without
    # modification, are permitted provided the following conditions are met:
    #   1. Redistributions of source code must retain the above copyright
    #      notice, this list of conditions and the following disclaimer.
    #   2. Redistributions in binary form must reproduce the above copyright
    #      notice, this list of conditions and the following disclaimer in
    #      the documentation and/or other materials provided with the
    #      distribution.
    #   3. The contributor name(s) may not be used to endorse or promote
    #      products derived from this software without specific prior
    #      written permission.
    # THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    # "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    # LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
    # FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
    # COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
    # INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
    # BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
    # OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
    # ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
    # TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF USE
    # OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    # Initialization
    sn = max(1, math.sqrt(nu)); ch, az, bz = _chlrps(sigma, a/sn, b/sn)
    n = len(sigma); N = 10; P = math.ceil(m/N); on = np.ones(P); p = 0; e = 0
    ps = np.sqrt(_primes(5*n*math.log(n+4)/4)); q = ps[:, np.newaxis]  # Richtmyer gens.

    # Randomization loop for ns samples
    c = None; dc = None
    for S in range(N):
        vp = on.copy(); s = np.zeros((n, P))
        for i in range(n):
            x = np.abs(2*np.mod(q[i]*np.arange(1, P+1) + rng.random(), 1)-1)  # periodizing transform
            if i == 0:
                r = on
                if nu > 0:
                    r = np.sqrt(2*_gaminv(x, nu/2))
            else:
                y = _Phinv(c + x*dc)
                s[i:] += ch[i:, i-1:i] * y
            si = s[i, :]; c = on.copy(); ai = az[i]*r - si; d = on.copy(); bi = bz[i]*r - si
            c[ai <= -9] = 0; tl = abs(ai) < 9; c[tl] = _Phi(ai[tl])
            d[bi <= -9] = 0; tl = abs(bi) < 9; d[tl] = _Phi(bi[tl])
            dc = d - c; vp = vp * dc
        d = (np.mean(vp) - p)/(S + 1); p = p + d; e = (S - 1)*e/(S + 1) + d**2
    e = math.sqrt(e)  # error estimate is 3 times std error with N samples.
    return p, e

