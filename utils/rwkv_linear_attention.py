
def rwkv_linear_attention(time_decay, time_first, key, value, state=None, return_state=False):
    no_cuda = any(t.device.type != "cuda" for t in [time_decay, time_first, key, value])
    # Launching the CUDA kernel for just one token will actually be slower (there is no for loop in the CPU version
    # in this case).
    one_token = key.size(1) == 1
    if rwkv_cuda_kernel is None or no_cuda or one_token:
        return rwkv_linear_attention_cpu(time_decay, time_first, key, value, state=state, return_state=return_state)
    else:
        return RwkvLinearAttention.apply(time_decay, time_first, key, value, state, return_state)

