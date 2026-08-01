
def check_array_values(
    values: Sequence[Union[jax.Array, np.ndarray]],
    infos: Sequence[types.ParamInfo],
    raise_error: bool = True,
):
  """Checks array values for zero size."""
  for v, info in zip(values, infos):
    if v.size == 0:
      if raise_error:
        raise ValueError(
            f'Cannot save arrays with zero size: ParamInfo: [name={info.name},'
            f'value_typestr={info.value_typestr}]'
        )
      else:
        logging.warning(
            'Saving array with zero size: ParamInfo: [name=%s,'
            ' value_typestr=%s]',
            info.name,
            info.value_typestr,
        )

