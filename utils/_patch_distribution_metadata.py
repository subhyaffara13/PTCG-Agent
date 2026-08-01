
def _patch_distribution_metadata():
    from . import _core_metadata

    """Patch write_pkg_file and read_pkg_file for higher metadata standards"""
    for attr in (
        'write_pkg_info',
        'write_pkg_file',
        'read_pkg_file',
        'get_metadata_version',
        'get_fullname',
    ):
        new_val = getattr(_core_metadata, attr)
        setattr(distutils.dist.DistributionMetadata, attr, new_val)

