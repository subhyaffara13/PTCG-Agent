
def _dhtm(mag, xp):
    """Compute the modified 1-D discrete Hilbert transform

    Parameters
    ----------
    mag : ndarray
        The magnitude spectrum. Should be 1-D with an even length, and
        preferably a fast length for FFT/IFFT.
    """
    # Adapted based on code by Niranjan Damera-Venkata,
    # Brian L. Evans and Shawn R. McCaslin (see refs for `minimum_phase`)
    sig = xp.zeros(mag.shape[0])
    # Leave Nyquist and DC at 0, knowing np.abs(fftfreq(N)[midpt]) == 0.5
    midpt = mag.shape[0] // 2
    sig = xpx.at(sig)[1:midpt].set(1.0)
    sig = xpx.at(sig)[midpt+1:].set(-1.0)
    # eventually if we want to support complex filters, we will need a
    # np.abs() on the mag inside the log, and should remove the .real
    recon = xp.real(ifft(mag * xp.exp(fft(sig * ifft(xp.log(mag))))))
    return recon

