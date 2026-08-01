
def smooth_distribution(p, eps=0.0001):
    """Given a discrete distribution (may have not been normalized to 1),
    smooth it by replacing zeros with eps multiplied by a scaling factor
    and taking the corresponding amount off the non-zero values.
    Ref: http://web.engr.illinois.edu/~hanj/cs412/bk3/KL-divergence.pdf
         https://github.com//apache/incubator-mxnet/blob/master/python/mxnet/contrib/quantization.py
    """
    is_zeros = (p == 0).astype(numpy.float32)
    is_nonzeros = (p != 0).astype(numpy.float32)
    n_zeros = is_zeros.sum()
    n_nonzeros = p.size - n_zeros

    if not n_nonzeros:
        # raise ValueError('The discrete probability distribution is malformed. All entries are 0.')
        return None
    eps1 = eps * float(n_zeros) / float(n_nonzeros)
    assert eps1 < 1.0, f"n_zeros={n_zeros}, n_nonzeros={n_nonzeros}, eps1={eps1}"

    hist = p.astype(numpy.float32)
    hist += eps * is_zeros + (-eps1) * is_nonzeros
    assert (hist <= 0).sum() == 0

    return hist

