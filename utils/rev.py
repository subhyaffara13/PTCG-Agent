
def rev(x, dims):
    # note - dims pre-canonicalized
    x_loader = x.make_loader()
    sizes = x.get_size()

    def loader(idx):
        idx = list(idx)
        assert len(idx) == len(sizes)
        for dim in dims:
            idx[dim] = (sizes[dim] - 1) - idx[dim]

        return x_loader(idx)

    return Pointwise.create(
        device=x.get_device(),
        dtype=x.get_dtype(),
        inner_fn=loader,
        ranges=sizes,
    )


def rev(operand, dimensions):
  dimensions = frozenset(dimensions)
  indexer = (_slice(None, None, -1) if d in dimensions else _slice(None)
             for d in range(np.ndim(operand)))
  return operand[tuple(indexer)]


def rev(operand: ArrayLike, dimensions: Sequence[int]) -> Array:
  """Wraps XLA's `Rev
  <https://www.openxla.org/xla/operation_semantics#rev_reverse>`_
  operator.
  """
  return rev_p.bind(operand, dimensions=tuple(dimensions))

