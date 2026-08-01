
def check_missing_deps() -> Iterator[None]:
  """Raise a better error message in case of `ImportError`.

  Usage:

  ```python
  from etils.epy import _internal

  with _internal.check_missing_deps():
    # pylint: disable=g-import-not-at-top
    import xyz
    # pylint: enable=g-import-not-at-top
  ```

  Yields:
    None
  """
  try:
    yield
  except ImportError as e:
    reraise_utils.reraise(
        e,
        suffix=(
            '\nEach etils sub-modules require deps to be installed separately '
            '(e.g. `from etils import ecolab` -> `pip install etils[ecolab]`)'
        ),
    )

