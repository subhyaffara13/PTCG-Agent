
def bilinear(tf, sample_per):
    r"""
    Returns falling coefficients of H(z) from numerator and denominator.

    Explanation
    ===========

    Where H(z) is the corresponding discretized transfer function,
    discretized with the bilinear transform method.
    H(z) is obtained from the continuous transfer function H(s)
    by substituting $s(z) = \frac{2}{T}\frac{z-1}{z+1}$ into H(s), where T is the
    sample period.
    Coefficients are falling, i.e. $H(z) = \frac{az+b}{cz+d}$ is returned
    as [a, b], [c, d].

    Examples
    ========

    >>> from sympy.physics.control.lti import TransferFunction, bilinear
    >>> from sympy.abc import s, L, R, T

    >>> tf = TransferFunction(1, s*L + R, s)
    >>> numZ, denZ = bilinear(tf, T)
    >>> numZ
    [T/(2*(L + R*T/2)), T/(2*(L + R*T/2))]
    >>> denZ
    [1, (-L + R*T/2)/(L + R*T/2)]
    """
    return gbt(tf, sample_per, S.Half)


def bilinear(b, a, fs=1.0):
    r"""Calculate a digital IIR filter from an analog transfer function by utilizing
    the bilinear transform.

    Parameters
    ----------
    b : array_like
        Coefficients of the numerator polynomial of the analog transfer function in
        form of a complex- or real-valued 1d array.
    a : array_like
        Coefficients of the denominator polynomial of the analog transfer function in
        form of a complex- or real-valued 1d array.
    fs : float
        Sample rate, as ordinary frequency (e.g., hertz). No pre-warping is
        done in this function.

    Returns
    -------
    beta : ndarray
        Coefficients of the numerator polynomial of the digital transfer function in
        form of a complex- or real-valued 1d array.
    alpha : ndarray
        Coefficients of the denominator polynomial of the digital transfer function in
        form of a complex- or real-valued 1d array.

    Notes
    -----
    The parameters :math:`b = [b_0, \ldots, b_Q]` and :math:`a = [a_0, \ldots, a_P]`
    are 1d arrays of length :math:`Q+1` and :math:`P+1`. They define the analog
    transfer function

    .. math::

        H_a(s) = \frac{b_0 s^Q + b_1 s^{Q-1} + \cdots + b_Q}{
                       a_0 s^P + a_1 s^{P-1} + \cdots + a_P}\ .

    The bilinear transform [1]_ is applied by substituting

    .. math::

        s = \kappa \frac{z-1}{z+1}\ , \qquad \kappa := 2 f_s\ ,

    into :math:`H_a(s)`, with :math:`f_s`  being the sampling rate.
    This results in the digital transfer function in the :math:`z`-domain

    .. math::

        H_d(z) = \frac{b_0 \left(\kappa \frac{z-1}{z+1}\right)^Q +
                       b_1 \left(\kappa \frac{z-1}{z+1}\right)^{Q-1} +
                       \cdots + b_Q}{
                       a_0 \left(\kappa \frac{z-1}{z+1}\right)^P +
                       a_1 \left(\kappa \frac{z-1}{z+1}\right)^{P-1} +
                       \cdots + a_P}\ .

    This expression can be simplified by multiplying numerator and denominator by
    :math:`(z+1)^N`, with :math:`N=\max(P, Q)`. This allows :math:`H_d(z)` to be
    reformulated as

    .. math::

       & & \frac{b_0 \big(\kappa (z-1)\big)^Q     (z+1)^{N-Q} +
                b_1 \big(\kappa (z-1)\big)^{Q-1} (z+1)^{N-Q+1} +
                \cdots + b_Q(z+1)^N}{
                a_0 \big(\kappa (z-1)\big)^P     (z+1)^{N-P} +
                a_1 \big(\kappa (z-1)\big)^{P-1} (z+1)^{N-P+1} +
                \cdots + a_P(z+1)^N}\\
        &=:& \frac{\beta_0 + \beta_1  z^{-1} + \cdots + \beta_N  z^{-N}}{
                 \alpha_0 + \alpha_1 z^{-1} + \cdots + \alpha_N z^{-N}}\ .


    This is the equation implemented to perform the bilinear transform. Note that for
    large :math:`f_s`, :math:`\kappa^Q` or :math:`\kappa^P` can cause a numeric
    overflow for sufficiently large :math:`P` or :math:`Q`.

    References
    ----------
    .. [1] "Bilinear Transform", Wikipedia,
           https://en.wikipedia.org/wiki/Bilinear_transform

    See Also
    --------
    lp2lp, lp2hp, lp2bp, lp2bs, bilinear_zpk

    Examples
    --------
    The following example shows the frequency response of an analog bandpass filter and
    the corresponding digital filter derived by utilitzing the bilinear transform:

    >>> from scipy import signal
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    ...
    >>> fs = 100  # sampling frequency
    >>> om_c = 2 * np.pi * np.array([7, 13])  # corner frequencies
    >>> bb_s, aa_s = signal.butter(4, om_c, btype='bandpass', analog=True, output='ba')
    >>> bb_z, aa_z = signal.bilinear(bb_s, aa_s, fs)
    ...
    >>> w_z, H_z = signal.freqz(bb_z, aa_z)  # frequency response of digitial filter
    >>> w_s, H_s = signal.freqs(bb_s, aa_s, worN=w_z*fs)  # analog filter response
    ...
    >>> f_z, f_s = w_z * fs / (2*np.pi), w_s / (2*np.pi)
    >>> Hz_dB, Hs_dB = (20*np.log10(np.abs(H_).clip(1e-10)) for H_ in (H_z, H_s))
    >>> fg0, ax0 = plt.subplots()
    >>> ax0.set_title("Frequency Response of 4-th order Bandpass Filter")
    >>> ax0.set(xlabel='Frequency $f$ in Hertz', ylabel='Magnitude in dB',
    ...         xlim=[f_z[1], fs/2], ylim=[-200, 2])
    >>> ax0.semilogx(f_z, Hz_dB, alpha=.5, label=r'$|H_z(e^{j 2 \pi f})|$')
    >>> ax0.semilogx(f_s, Hs_dB, alpha=.5, label=r'$|H_s(j 2 \pi f)|$')
    >>> ax0.legend()
    >>> ax0.grid(which='both', axis='x')
    >>> ax0.grid(which='major', axis='y')
    >>> plt.show()

    The difference in the higher frequencies shown in the plot is caused by an effect
    called "frequency warping". [1]_ describes a method called "pre-warping" to
    reduce those deviations.
    """
    xp = array_namespace(b, a)

    b, a = map(np.asarray, (b, a))
    b, a = np.atleast_1d(b), np.atleast_1d(a)  # convert scalars, if needed
    if not a.ndim == 1:
        raise ValueError(f"Parameter a is not a 1d array since {a.shape=}")
    if not b.ndim == 1:
        raise ValueError(f"Parameter b is not a 1d array since {b.shape=}")
    b, a = np.trim_zeros(b, 'f'), np.trim_zeros(a, 'f')  # remove leading zeros
    fs = _validate_fs(fs, allow_none=False)

    # Splitting the factor fs*2 between numerator and denominator reduces the chance of
    # numeric overflow for large fs and large N:
    fac = np.sqrt(fs*2)
    zp1 = np.polynomial.Polynomial((+1, 1)) / fac  # Polynomial (z + 1) / fac
    zm1 = np.polynomial.Polynomial((-1, 1)) * fac  # Polynomial (z - 1) * fac
    # Note that NumPy's Polynomial coefficient order is backward compared to a and b.

    N = max(len(a), len(b)) - 1
    numerator   = sum(b_ * zp1**(N-q) * zm1**q for q, b_ in enumerate(b[::-1]))
    denominator = sum(a_ * zp1**(N-p) * zm1**p for p, a_ in enumerate(a[::-1]))

    return normalize(
        xp.asarray(numerator.coef[::-1].copy()),
        xp.asarray(denominator.coef[::-1].copy())
    )

