
def save_diff_image(expected, actual, output):
    """
    Parameters
    ----------
    expected : str
        File path of expected image.
    actual : str
        File path of actual image.
    output : str
        File path to save difference image to.
    """
    expected_image = _load_image(expected)
    actual_image = _load_image(actual)
    actual_image, expected_image = crop_to_same(
        actual, actual_image, expected, expected_image)
    expected_image = np.array(expected_image, float)
    actual_image = np.array(actual_image, float)
    if expected_image.shape != actual_image.shape:
        raise ImageComparisonFailure(
            f"Image sizes do not match expected size: {expected_image.shape} "
            f"actual size {actual_image.shape}")
    abs_diff = np.abs(expected_image - actual_image)

    # expand differences in luminance domain
    abs_diff *= 10
    abs_diff = np.clip(abs_diff, 0, 255).astype(np.uint8)

    if abs_diff.shape[2] == 4:  # Hard-code the alpha channel to fully solid
        abs_diff[:, :, 3] = 255

    Image.fromarray(abs_diff).save(output, format="png")

