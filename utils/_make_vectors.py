
def _make_vectors(inp_tensors, outputs, *, use_forward_ad):
    # Use our own generator to avoid messing with the user's RNG state
    g_cpu = torch.Generator()

    def _vec_from_tensor_cpu(*args):
        # Default allocate all tensors on CPU, so they are on the same device as the generator
        # even if the user specified a default device
        with torch.device("cpu"):
            return _vec_from_tensor(*args)

    all_u = []
    all_u_dense = []
    for inp in inp_tensors:
        ur = _vec_from_tensor_cpu(inp, g_cpu, True)
        ur_dense = _to_flat_dense_if_sparse(ur)
        if inp.is_complex():
            ui = _vec_from_tensor_cpu(inp, g_cpu, True)
            all_u.append((ur, ui))
            ui_dense = _to_flat_dense_if_sparse(ui)
            all_u_dense.append((ur_dense, ui_dense))
        else:
            all_u.append(ur)
            all_u_dense.append(ur_dense)
    all_v = (
        None
        if use_forward_ad
        else [_vec_from_tensor_cpu(out, g_cpu) for out in outputs]
    )
    return all_v, all_u, all_u_dense

