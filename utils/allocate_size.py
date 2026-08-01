
def allocate_size(shape_env, min_val=0, max_val=None):
    result = shape_env.create_unbacked_symint()
    torch.fx.experimental.symbolic_shapes._constrain_range_for_size(
        result, min=min_val, max=max_val
    )
    return result

