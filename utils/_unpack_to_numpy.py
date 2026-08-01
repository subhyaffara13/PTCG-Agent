
def _unpack_to_numpy(x):
    """Internal helper to extract data from e.g. pandas and xarray objects."""
    if isinstance(x, np.ndarray):
        # If numpy, return directly
        return x
    if hasattr(x, 'to_numpy'):
        # Assume that any to_numpy() method actually returns a numpy array
        return x.to_numpy()
    if hasattr(x, 'values'):
        xtmp = x.values
        # For example a dict has a 'values' attribute, but it is not a property
        # so in this case we do not want to return a function
        if isinstance(xtmp, np.ndarray):
            return xtmp
    if _is_torch_array(x) \
        or _is_jax_array(x) \
        or _is_tensorflow_array(x) \
        or _is_mlx_array(x):
        # using np.asarray() instead of explicitly __array__(), as the latter is
        # only _one_ of many methods, and it's the last resort, see also
        # https://numpy.org/devdocs/user/basics.interoperability.html#using-arbitrary-objects-in-numpy
        # therefore, let arrays do better if they can
        xtmp = np.asarray(x)

        # In case np.asarray method does not return a numpy array in future
        if isinstance(xtmp, np.ndarray):
            return xtmp
    return x


def _unpack_to_numpy(values, cast_onnx_accepted=True) -> list:
    value_unpacked = []
    for value in values:
        value_unpacked.extend(
            utils.unpack_quantized_tensor(value, cast_onnx_accepted=cast_onnx_accepted)
        )
    return [_to_numpy(v) for v in value_unpacked]

