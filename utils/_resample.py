
def _resample(
        image_obj, data, out_shape, transform, *, resample=None, alpha=1):
    """
    Convenience wrapper around `._image.resample` to resample *data* to
    *out_shape* (with a third dimension if *data* is RGBA) that takes care of
    allocating the output array and fetching the relevant properties from the
    Image object *image_obj*.
    """
    # AGG can only handle coordinates smaller than 24-bit signed integers,
    # so raise errors if the input data is larger than _image.resample can
    # handle.
    msg = ('Data with more than {n} cannot be accurately displayed. '
           'Downsampling to less than {n} before displaying. '
           'To remove this warning, manually downsample your data.')
    if data.shape[1] > 2**23:
        warnings.warn(msg.format(n='2**23 columns'))
        step = int(np.ceil(data.shape[1] / 2**23))
        data = data[:, ::step]
        transform = Affine2D().scale(step, 1) + transform
    if data.shape[0] > 2**24:
        warnings.warn(msg.format(n='2**24 rows'))
        step = int(np.ceil(data.shape[0] / 2**24))
        data = data[::step, :]
        transform = Affine2D().scale(1, step) + transform
    # decide if we need to apply anti-aliasing if the data is upsampled:
    # compare the number of displayed pixels to the number of
    # the data pixels.
    interpolation = image_obj.get_interpolation()
    if interpolation in ['antialiased', 'auto']:
        # don't antialias if upsampling by an integer number or
        # if zooming in more than a factor of 3
        pos = np.array([[0, 0], [data.shape[1], data.shape[0]]])
        disp = transform.transform(pos)
        dispx = np.abs(np.diff(disp[:, 0]))
        dispy = np.abs(np.diff(disp[:, 1]))
        if ((dispx > 3 * data.shape[1] or
                dispx == data.shape[1] or
                dispx == 2 * data.shape[1]) and
            (dispy > 3 * data.shape[0] or
                dispy == data.shape[0] or
                dispy == 2 * data.shape[0])):
            interpolation = 'nearest'
        else:
            interpolation = 'hanning'
    out = np.zeros(out_shape + data.shape[2:], data.dtype)  # 2D->2D, 3D->3D.
    if resample is None:
        resample = image_obj.get_resample()

    # When an output pixel falls exactly on the edge between two input pixels, the Agg
    # resampler will use the right input pixel as the nearest neighbor.  We want the
    # left input pixel to be chosen instead, so we flip the input data and the supplied
    # transform.  If origin != 'upper', the transform will already include a flip in the
    # vertical direction.
    if interpolation == 'nearest':
        transform = Affine2D().translate(-data.shape[1], 0).scale(-1, 1) + transform
        data = np.flip(data, axis=1)
        if image_obj.origin == 'upper':
            transform = Affine2D().translate(0, -data.shape[0]).scale(1, -1) + transform
            data = np.flip(data, axis=0)

    _image.resample(data, out, transform,
                    _interpd_[interpolation],
                    resample,
                    alpha,
                    image_obj.get_filternorm(),
                    image_obj.get_filterrad())

    return out


def _resample(
    samples: "FloatArray", source_rate: int, target_rate: int
) -> "FloatArray":
    """
    Resample mono float32 ``samples`` from ``source_rate`` to ``target_rate``.

    Prefers high-quality polyphase resampling when ``soxr`` or ``scipy`` is
    available (anti-aliased, important for downsampling 44.1/48 kHz -> 16 kHz
    where naive interpolation folds high frequencies back into the speech
    band). Falls back to linear interpolation if neither is installed —
    acceptable for speech-only mono input but lossy for wideband content.
    """
    import numpy as np  # type: ignore

    if source_rate == target_rate or samples.size == 0:
        return samples

    try:
        import soxr  # type: ignore

        return cast(
            "FloatArray",
            np.asarray(
                soxr.resample(samples, source_rate, target_rate), dtype=np.float32
            ),
        )
    except ImportError:
        pass

    try:
        from math import gcd

        from scipy.signal import resample_poly  # type: ignore

        g = gcd(int(source_rate), int(target_rate))
        up = int(target_rate) // g
        down = int(source_rate) // g
        return cast(
            "FloatArray", np.asarray(resample_poly(samples, up, down), dtype=np.float32)
        )
    except ImportError:
        pass

    return _linear_resample(samples, source_rate, target_rate)

