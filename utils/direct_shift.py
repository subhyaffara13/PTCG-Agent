
def direct_shift(x,a,period=None):
    n = len(x)
    if period is None:
        k = fftfreq(n)*1j*n
    else:
        k = fftfreq(n)*2j*pi/period*n
    return ifft(fft(x)*exp(k*a)).real

