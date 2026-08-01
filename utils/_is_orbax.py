
def _is_orbax(array: Array) -> bool:
  if 'orbax.checkpoint' not in sys.modules:
    return False
  from orbax.checkpoint.metadata import value  # pylint: disable=g-import-not-at-top  # pytype: disable=import-error

  return isinstance(
      array,
      (
          value.ArrayMetadata,
          value.ScalarMetadata,
      ),
  )

