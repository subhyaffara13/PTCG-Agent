
def sample_inputs_pca_lowrank(op_info, device, dtype, requires_grad=False, **kwargs):
    # we reuse samples from svd_lowrank which come in group of two with
    # kwarg['M'] = None and with kwarg['M'] = <some tensor>
    samples = sample_inputs_svd_lowrank(op_info, device, dtype, requires_grad, **kwargs)
    for s1, s2 in chunk_iter(samples, 2):
        del s1.kwargs['M']
        del s2.kwargs['M']
        s1.kwargs['center'] = False
        s2.kwargs['center'] = True
        yield s1
        yield s2

