
def direct_hilbert(x):
    fx = fft(x)
    n = len(fx)
    w = fftfreq(n)*n
    w = 1j*sign(w)
    return ifft(w*fx)

