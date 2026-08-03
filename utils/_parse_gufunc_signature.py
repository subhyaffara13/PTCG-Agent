import re

def _parse_gufunc_signature(signature):
    """
    Parse string signatures for a generalized universal function.

    Arguments
    ---------
    signature : string
        Generalized universal function signature, e.g., ``(m,n),(n,p)->(m,p)``
        for ``np.matmul``.

    Returns
    -------
    Tuple of input and output core dimensions parsed from the signature, each
    of the form List[Tuple[str, ...]].
    """
    signature = re.sub(r'\s+', '', signature)

    if not re.match(_SIGNATURE, signature):
        raise ValueError(
            f'not a valid gufunc signature: {signature}')
    return tuple([tuple(re.findall(_DIMENSION_NAME, arg))
                  for arg in re.findall(_ARGUMENT, arg_list)]
                 for arg_list in signature.split('->'))


def _parse_gufunc_signature(
    signature: str,
) -> tuple[list[CoreDims], list[CoreDims]]:
  """Parse string signatures for a generalized universal function.

  Args:
    signature: generalized universal function signature, e.g.,
      ``(m,n),(n,p)->(m,p)`` for ``jnp.matmul``.

  Returns:
    Input and output core dimensions parsed from the signature.
  """
  if not re.match(_SIGNATURE, signature):
    raise ValueError(
        f'not a valid gufunc signature: {signature}')
  args, retvals = ([tuple(re.findall(_DIMENSION_NAME, arg))
                   for arg in re.findall(_ARGUMENT, arg_list)]
                   for arg_list in signature.split('->'))
  return args, retvals

