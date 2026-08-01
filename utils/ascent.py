
def ascent():
    """
    Get an 8-bit grayscale bit-depth, 512 x 512 derived image for easy
    use in demos.

    The image is derived from
    https://pixnio.com/people/accent-to-the-top

    Returns
    -------
    ascent : ndarray
       convenient image to use for testing and demonstration

    Examples
    --------
    >>> import scipy.datasets
    >>> ascent = scipy.datasets.ascent()
    >>> ascent.shape
    (512, 512)
    >>> ascent.max()
    np.uint8(255)

    >>> import matplotlib.pyplot as plt
    >>> plt.gray()
    >>> plt.imshow(ascent)
    >>> plt.show()

    """
    import pickle

    # The file will be downloaded automatically the first time this is run,
    # returning the path to the downloaded file. Afterwards, Pooch finds
    # it in the local cache and doesn't repeat the download.
    fname = fetch_data("ascent.dat")
    # Now we just need to load it with our standard Python tools.
    with open(fname, 'rb') as f:
        ascent = array(pickle.load(f))
    return ascent

