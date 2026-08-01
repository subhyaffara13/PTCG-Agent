
def is_hoistable(v: Literal) -> bool:
  return (np.ndim(v.val) > 0 and
          getattr(v.val, "nbytes", 4) > config.embedded_constants_max_bytes.value)

