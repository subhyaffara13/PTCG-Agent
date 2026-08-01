
def direct_tilbert(x,h=1,period=None):
    fx = fft(x)
    n = len(fx)
    if period is None:
        period = 2*pi
    w = fftfreq(n)*h*2*pi/period*n
    w[0] = 1
    w = 1j/tanh(w)
    w[0] = 0j
    return ifft(w*fx)

