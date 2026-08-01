
def direct_itilbert(x,h=1,period=None):
    fx = fft(x)
    n = len(fx)
    if period is None:
        period = 2*pi
    w = fftfreq(n)*h*2*pi/period*n
    w = -1j*tanh(w)
    return ifft(w*fx)

