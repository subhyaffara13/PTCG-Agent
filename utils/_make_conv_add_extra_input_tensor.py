
def _make_conv_add_extra_input_tensor(scale, zero_point, sizes):
    (X_value_min, X_value_max) = (0, 4)
    X_init = torch.randint(
        X_value_min,
        X_value_max,
        sizes,  # Infer the size of tensor to do the add
    )
    X = scale * (X_init - zero_point).float()
    X_q = torch.quantize_per_tensor(
        X, scale=scale, zero_point=zero_point, dtype=torch.quint8
    )
    return X, X_q

