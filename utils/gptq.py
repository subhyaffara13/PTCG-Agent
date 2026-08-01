
def gptq(
    W,
    H,
    num_bits=4,
    group_size=32,
    scheme="asym",
    blocksize=128,
    percdamp=0.01,
    actorder=False,
    mse=False,
    perchannel=True,
):
    """Quant the weight with GPTQ method.

    Args:
        W (array): weight.
        H (array): Hessian matrix.
        num_bits (int, optional): num_bits. Default is 4.
        group_size (int, optional): how many elements share one scale/zp. Default is 32.
        scheme (str, optional): sym or asym. Defaults to "asym".
        blocksize (int, optional): blocksize to quantize weight.
        percdamp (float, optional): percent of the average Hessian diagonal to use for dampening.
        actorder (bool, optional): whether rearrange Hessian matrix considering the diag's value.
        mse (bool, optional): whether get scale and zero point with mse error.
        perchannel (bool, optional): whether quantize weight per-channel.

    Returns:
        Q: fake quantized weight
    """
    maxq = 2**num_bits - 1
    grid = 100
    maxshrink = 0.8
    norm = 2.4

    def find_params(weight):
        org_shape = weight.shape
        # find zp, scale
        if not perchannel:
            weight = np.expand_dims(weight.flatten(), axis=1)
        tmp = np.zeros(weight.shape[1])
        xmin = np.minimum(np.min(weight, axis=0), tmp)
        xmax = np.maximum(np.max(weight, axis=0), tmp)
        if scheme == "sym":
            xmax = np.maximum(np.abs(xmin), xmax)
            tmp = xmin < 0
            if np.any(tmp):
                xmin[tmp] = -xmax[tmp]
        tmp = (xmin == 0) & (xmax == 0)
        xmin[tmp] = -1
        xmax[tmp] = +1

        scale = (xmax - xmin) / maxq
        if scheme == "sym":
            zero = np.ones(scale.shape) * (maxq + 1) / 2
        else:
            zero = np.round(-xmin / scale)
        if mse:
            best = np.ones([weight.shape[1]]) * float("inf")
            for i in range(int(maxshrink * grid)):
                p = 1 - i / grid
                xmin1 = p * xmin
                xmax1 = p * xmax
                scale1 = (xmax1 - xmin1) / maxq
                zero1 = np.round(-xmin1 / scale1) if scheme != "sym" else zero
                q = np.clip(np.round(weight / scale1) + zero1, 0, maxq)
                q -= weight
                q = np.power(np.abs(q), norm)
                err = np.sum(q, 0)
                tmp = err < best
                if np.any(tmp):
                    best[tmp] = err[tmp]
                    scale[tmp] = scale1[tmp]
                    zero[tmp] = zero1[tmp]
        if not perchannel:
            tmp = org_shape[1]
            scale = np.repeat(scale, tmp)
            zero = np.repeat(zero, tmp)
        shape = [-1] + [1] * (len(org_shape) - 1)
        scale = np.reshape(scale, shape)
        zero = np.reshape(zero, shape)
        return scale, zero

    shape = W.shape
    scale, zp = find_params(W)
    dead = np.diag(H) == 0
    H[dead, dead] = 1
    W[dead, :] = 0  # such channel makes no contribution to quantization computation

    # rearrange considering the diag's value
    if actorder:
        perm = np.argsort(np.diag(H))[::-1]
        W = W[perm, :]  # noqa: N806
        H = H[perm, :][:, perm]  # noqa: N806
    Losses = np.zeros_like(W)  # noqa: N806
    Q = np.zeros_like(W)  # noqa: N806
    damp = percdamp * np.mean(np.diag(H))
    diag = np.arange(shape[0])
    H[diag, diag] += damp  # add a average value of
    H = np.linalg.cholesky(np.linalg.inv(H)).T  # noqa: N806
    Hinv = H  # noqa: N806
    for i1 in range(0, shape[0], blocksize):
        i2 = min(i1 + blocksize, shape[0])
        count = i2 - i1

        W1 = copy.deepcopy(W[i1:i2, :])  # noqa: N806
        Q1 = np.zeros_like(W1)  # noqa: N806
        Err1 = np.zeros_like(W1)  # noqa: N806
        Losses1 = np.zeros_like(W1)  # noqa: N806
        Hinv1 = Hinv[i1:i2, i1:i2]  # noqa: N806

        for i in range(count):  # within a block, channel wise
            w = W1[i, :]
            d = Hinv1[i, i]

            if group_size != -1:
                if (i1 + i) % group_size == 0:
                    scale, zp = find_params(W[(i1 + i) : (i1 + i + group_size), :])

            q = (scale * (np.clip(np.round(w[:, np.newaxis] / scale) + zp, 0, maxq) - zp)).flatten()
            Q1[i, :] = q
            Losses1[i, :] = (w - q) ** 2 / d**2

            err1 = (w - q) / d
            W1[i:, :] -= np.matmul(np.expand_dims(Hinv1[i:, i], axis=1), np.expand_dims(err1, axis=0))
            Err1[i, :] = err1

        Q[i1:i2, :] = Q1
        Losses[i1:i2, :] = Losses1 / 2

        W[i2:, :] -= np.matmul(Hinv[i2:, i1:i2], Err1)

    if actorder:
        invperm = np.argsort(perm)
        Q = Q[invperm, :]  # noqa: N806

    Q = np.reshape(Q, W.shape)  # noqa: N806
    del W
    return Q

