
def _maybe_broadcast(*args, preserve_cpu_scalar_tensors=True):
    # Computes common shape
    common_shape = _broadcast_shapes(
        *(t.shape if isinstance(t, TensorLike) else None for t in args)
    )

    def should_expand(a: ShapeType, b: ShapeType) -> bool:
        from torch.fx.experimental.symbolic_shapes import (
            guard_or_false,
            sym_and,
            sym_or,
        )

        if len(a) != len(b):
            return True

        for x, y in zip(a, b):
            if guard_or_false(x != y):
                # We know they are not the same.
                return True

            # They are the same or we do not know if they are the same or not.
            # 1==1 no-broadcast
            # u0==1 and 1==u0 cases. We broadcast!
            if guard_or_false(sym_and(x == 1, y == 1)):
                pass
            elif guard_or_false(sym_or(x == 1, y == 1)):
                # assume broadcasting.
                return True

            # u0==u1 assume the same, no broadcasting!
            torch._check(
                x == y,
                lambda: "sizes assumed to be the same due to unbacked broadcasting semantics",
            )

        return False

    def __maybe_broadcast(x, shape):
        if x is None:
            return None
        elif isinstance(x, Number):
            return x
        elif isinstance(x, TensorLike):
            if preserve_cpu_scalar_tensors and utils.is_cpu_scalar_tensor(x):
                return x

            if should_expand(x.shape, common_shape):
                return x.expand(common_shape)

            return x
        else:
            raise RuntimeError(
                "Unexpected type when broadcasting: " + str(type(x)) + "!"
            )

    return tuple(__maybe_broadcast(x, common_shape) for x in args)


def _maybe_broadcast(target_shape, x, target_sharding):
  x_shape = np.shape(x)
  x_sharding = typeof(x).sharding
  if (core.definitely_equal_shape(x_shape, target_shape) and
      x_sharding == target_sharding):
    return x
  elif not x_shape:
    return broadcast_in_dim(x, target_shape, (), out_sharding=target_sharding)
  else:
    dims = [i for i, (a, b) in enumerate(zip(x_shape, target_shape))
            if core.definitely_equal(a, b)]
    squeeze_shape = [x_shape[i] for i in dims]
    return broadcast_in_dim(reshape(x, squeeze_shape), target_shape, dims,
                            out_sharding=target_sharding)

