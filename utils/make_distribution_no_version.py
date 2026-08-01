
def make_distribution_no_version(tmpdir, basename):
    """
    Create a distribution directory with no file containing the version.
    """
    dist_dir = tmpdir / basename
    dist_dir.ensure_dir()
    # Make the directory non-empty so distributions_from_metadata()
    # will detect it and yield it.
    dist_dir.join('temp.txt').ensure()

    dists = list(pkg_resources.distributions_from_metadata(dist_dir))
    assert len(dists) == 1
    (dist,) = dists

    return dist, dist_dir

