import os

def _apply(
    dist: Distribution,
    filepath: StrPath,
    other_files: Iterable[StrPath] = (),
    ignore_option_errors: bool = False,
) -> tuple[ConfigMetadataHandler, ConfigOptionsHandler]:
    """Read configuration from ``filepath`` and applies to the ``dist`` object."""
    from setuptools.dist import _Distribution

    filepath = os.path.abspath(filepath)

    if not os.path.isfile(filepath):
        raise FileError(f'Configuration file {filepath} does not exist.')

    current_directory = os.getcwd()
    os.chdir(os.path.dirname(filepath))
    filenames = [*other_files, filepath]

    try:
        # TODO: Temporary cast until mypy 1.12 is released with upstream fixes from typeshed
        _Distribution.parse_config_files(dist, filenames=cast(list[str], filenames))
        handlers = parse_configuration(
            dist, dist.command_options, ignore_option_errors=ignore_option_errors
        )
        dist._finalize_license_files()
    finally:
        os.chdir(current_directory)

    return handlers


def _apply(matrix: Array, vector: Array, inverse: bool) -> Array:
  return jnp.where(inverse, matrix.T, matrix) @ vector

