
def get_weight_scale(weight, group_size):
    """Get the scale of weight."""
    org_shape = weight.shape
    weight = np.reshape(weight, (-1, group_size)) if group_size != -1 else weight
    scale = np.mean(np.reshape(np.abs(weight) / np.max(np.abs(weight), axis=1, keepdims=True), org_shape), axis=0)
    return scale

