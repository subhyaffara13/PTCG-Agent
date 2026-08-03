import math


def _cubic_coeff(signal):
    signal = np.asarray(signal)

    zi = -2 + math.sqrt(3)
    K = len(signal)
    powers = zi ** np.arange(K)

    if K == 1:
        yplus = signal[0] + zi * add.reduce(powers * signal)
        output = zi / (zi - 1) * yplus
        return atleast_1d(output)

    # Forward filter:
    # yplus[0] = signal[0] + zi * add.reduce(powers * signal)
    # for k in range(1, K):
    #     yplus[k] = signal[k] + zi * yplus[k - 1]

    state = lfiltic(1, np.r_[1, -zi], np.atleast_1d(add.reduce(powers * signal)))

    b = np.ones(1)
    a = np.r_[1, -zi]
    yplus, _ = lfilter(b, a, signal, zi=state)

    # Reverse filter:
    # output[K - 1] = zi / (zi - 1) * yplus[K - 1]
    # for k in range(K - 2, -1, -1):
    #     output[k] = zi * (output[k + 1] - yplus[k])
    out_last = zi / (zi - 1) * yplus[K - 1]
    state = lfiltic(-zi, r_[1, -zi], np.atleast_1d(out_last))

    b = np.asarray([-zi])
    output, _ = lfilter(b, a, yplus[-2::-1], zi=state)
    output = np.r_[output[::-1], out_last]
    return output * 6.0

