
def _variance_scaling(tensor, mode="fan_in", distribution="normal"):
    fan_in, fan_out = torch.nn.init._calculate_fan_in_and_fan_out(tensor)
    if mode == "fan_in":
        denom = fan_in
    elif mode == "fan_out":
        denom = fan_out
    elif mode == "fan_avg":
        denom = (fan_in + fan_out) / 2

    variance = 1.0 / denom

    if distribution == "truncated_normal":
        trunc_normal_(tensor, std=math.sqrt(variance) / 0.87962566103423978)
    elif distribution == "normal":
        normal_(tensor, std=math.sqrt(variance))
    elif distribution == "uniform":
        bound = math.sqrt(3 * variance)
        uniform_(tensor, -bound, bound)
    else:
        raise ValueError(f"invalid distribution {distribution}")

