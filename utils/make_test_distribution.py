import os

def make_test_distribution(metadata_path, metadata):
    """
    Make a test Distribution object, and return it.

    :param metadata_path: the path to the metadata file that should be
        created. This should be inside a distribution directory that should
        also be created. For example, an argument value might end with
        "<project>.dist-info/METADATA".
    :param metadata: the desired contents of the metadata file, as bytes.
    """
    dist_dir = os.path.dirname(metadata_path)
    os.mkdir(dist_dir)
    with open(metadata_path, 'wb') as f:
        f.write(metadata)
    dists = list(pkg_resources.distributions_from_metadata(dist_dir))
    (dist,) = dists

    return dist

