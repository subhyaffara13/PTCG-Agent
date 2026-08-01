
def _flatten(x, f):
    if isinstance(x, str):
        f.write('%ds%s' % (len(x), x))
    elif isinstance(x, dict):
        keys = sorted(x.keys())
        f.write('%dd' % len(keys))
        for key in keys:
            _flatten(key, f)
            _flatten(x[key], f)
    elif isinstance(x, (list, tuple)):
        f.write('%dl' % len(x))
        for value in x:
            _flatten(value, f)
    elif isinstance(x, int_or_long):
        f.write('%di' % (x,))
    else:
        raise TypeError(
            "the keywords to verify() contains unsupported object %r" % (x,))


def _flatten(xs, prefix, keep_empty_nodes, is_leaf, sep):
  def _key(path):
    if sep is None:
      return path
    return sep.join(path)

  if not isinstance(xs, (flax.core.FrozenDict, dict)) or (
      is_leaf and is_leaf(prefix, xs)
  ):
    return {_key(prefix): xs}
  result = {}
  is_empty = True
  for key, value in xs.items():
    is_empty = False
    path = prefix + (key,)
    result.update(_flatten(value, path, keep_empty_nodes, is_leaf, sep))
  if keep_empty_nodes and is_empty:
    if prefix == ():  # when the whole input is empty
      return {}
    return {_key(prefix): empty_node}
  return result


def _flatten(ll: Iterable) -> list:
    ret = []
    for i in ll:
        # Developer notes:
        # - do not collapse this section of code, isinstance checks are done
        # in optimal order
        if isinstance(i, str):
            ret.append(i)
        elif isinstance(i, Iterable):
            ret.extend(_flatten(i))
        else:
            ret.append(i)
    return ret


def _flatten(
    tensor_dict: Dict[str, np.ndarray], keep_alive_buffer: List
) -> Dict[str, Dict]:
    flattened = {}
    for k, v in tensor_dict.items():
        tensor = v
        if not _is_little_endian(tensor):
            tensor = tensor.byteswap(inplace=False)
            keep_alive_buffer.append(tensor)
        flattened[k] = TensorSpec(
            dtype=tensor.dtype.name,
            shape=tensor.shape,
            data_ptr=tensor.ctypes.data,
            data_len=tensor.nbytes,
        )
    return flattened


def _flatten(
    tensors: Dict[str, paddle.Tensor], keep_alive_buffer: List
) -> Dict[str, Dict[str, Any]]:
    if not isinstance(tensors, dict):
        raise ValueError(
            f"Expected a dict of [str, paddle.Tensor] but received {type(tensors)}"
        )

    for k, v in tensors.items():
        if not isinstance(v, paddle.Tensor):
            raise ValueError(
                f"Key `{k}` is invalid, expected paddle.Tensor but received {type(v)}"
            )

    flattened = {}
    for k, v in tensors.items():
        arr, tensor_ref = _to_ndarray(v, k)
        keep_alive_buffer.append((arr, tensor_ref))
        flattened[k] = TensorSpec(
            dtype=str(v.dtype).split(".")[-1],
            shape=v.shape,
            data_ptr=arr.ctypes.data,
            data_len=arr.nbytes,
        )
    return flattened


def _flatten(result: list[TOKEN | AppliedFunction]):
    result2: list[TOKEN] = []
    for tok in result:
        if isinstance(tok, AppliedFunction):
            result2.extend(tok.expand())
        else:
            result2.append(tok)
    return result2


def _flatten(L):
    ret = []
    for i in L:
        if isinstance(i, list):
            ret.extend(_flatten(i))
        else:
            ret.append(i)
    return ret


def _flatten(self: Array, order: str = "C", *, out_sharding=None) -> Array:
  """Flatten array into a 1-dimensional shape.

  Refer to :func:`jax.numpy.ravel` for the full documentation.
  """
  return lax_numpy.ravel(self, order=order, out_sharding=out_sharding)


def _flatten(args):
  return [x for arg in args for x in arg]

