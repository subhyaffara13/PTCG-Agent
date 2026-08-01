
def _Deprecated(
    name,
    alternative='get/find descriptors from generated code or query the descriptor_pool',
):
  if _Deprecated.count > 0:
    _Deprecated.count -= 1
    warnings.warn(
        'Call to deprecated %s, use %s instead.' % (name, alternative),
        category=DeprecationWarning,
        stacklevel=3,
    )

