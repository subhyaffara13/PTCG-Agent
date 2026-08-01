
def face(gray=False):
    """
    Get a 1024 x 768, color image of a raccoon face.

    The image is derived from
    https://pixnio.com/fauna-animals/raccoons/raccoon-procyon-lotor

    Parameters
    ----------
    gray : bool, optional
        If True return 8-bit grey-scale image, otherwise return a color image

    Returns
    -------
    face : ndarray
        image of a raccoon face

    Examples
    --------
    >>> import scipy.datasets
    >>> face = scipy.datasets.face()
    >>> face.shape
    (768, 1024, 3)
    >>> face.max()
    np.uint8(255)

    >>> import matplotlib.pyplot as plt
    >>> plt.gray()
    >>> plt.imshow(face)
    >>> plt.show()

    """
    import bz2
    fname = fetch_data("face.dat")
    with open(fname, 'rb') as f:
        rawdata = f.read()
    face_data = bz2.decompress(rawdata)
    face = frombuffer(face_data, dtype='uint8').reshape((768, 1024, 3))
    if gray is True:
        face = (0.21 * face[:, :, 0] + 0.71 * face[:, :, 1] +
                0.07 * face[:, :, 2]).astype('uint8')
    return face

