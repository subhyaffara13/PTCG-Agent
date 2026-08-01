
def compare_images(expected, actual, tol, in_decorator=False):
    """
    Compare two "image" files checking differences within a tolerance.

    The two given filenames may point to files which are convertible to
    PNG via the `!converter` dictionary. The underlying RMS is calculated
    in a similar way to the `.calculate_rms` function.

    Parameters
    ----------
    expected : str
        The filename of the expected image.
    actual : str
        The filename of the actual image.
    tol : float
        The tolerance (a color value difference, where 255 is the
        maximal difference).  The test fails if the average pixel
        difference is greater than this value.
    in_decorator : bool
        Determines the output format. If called from image_comparison
        decorator, this should be True. (default=False)

    Returns
    -------
    None or dict or str
        Return *None* if the images are equal within the given tolerance.

        If the images differ, the return value depends on  *in_decorator*.
        If *in_decorator* is true, a dict with the following entries is
        returned:

        - *rms*: The RMS of the image difference.
        - *expected*: The filename of the expected image.
        - *actual*: The filename of the actual image.
        - *diff_image*: The filename of the difference image.
        - *tol*: The comparison tolerance.

        Otherwise, a human-readable multi-line string representation of this
        information is returned.

    Examples
    --------
    ::

        img1 = "./baseline/plot.png"
        img2 = "./output/plot.png"
        compare_images(img1, img2, 0.001)

    """
    actual = os.fspath(actual)
    if not os.path.exists(actual):
        raise Exception(f"Output image {actual} does not exist.")
    if os.stat(actual).st_size == 0:
        raise Exception(f"Output image file {actual} is empty.")

    # Convert the image to png
    expected = os.fspath(expected)
    if not os.path.exists(expected):
        raise OSError(f'Baseline image {expected!r} does not exist.')
    extension = expected.split('.')[-1]
    if extension != 'png':
        actual = convert(actual, cache=True)
        expected = convert(expected, cache=True)

    # open the image files
    expected_image = _load_image(expected)
    actual_image = _load_image(actual)

    actual_image, expected_image = crop_to_same(
        actual, actual_image, expected, expected_image)

    diff_image = make_test_filename(actual, 'failed-diff')

    if tol <= 0:
        if np.array_equal(expected_image, actual_image):
            return None

    rms, abs_diff = _image.calculate_rms_and_diff(expected_image, actual_image)

    if rms <= tol:
        return None

    Image.fromarray(abs_diff).save(diff_image, format="png")

    results = dict(rms=rms, expected=str(expected),
                   actual=str(actual), diff=str(diff_image), tol=tol)

    if not in_decorator:
        # Then the results should be a string suitable for stdout.
        template = ['Error: Image files did not match.',
                    'RMS Value: {rms}',
                    'Expected:  \n    {expected}',
                    'Actual:    \n    {actual}',
                    'Difference:\n    {diff}',
                    'Tolerance: \n    {tol}', ]
        results = '\n  '.join([line.format(**results) for line in template])
    return results

