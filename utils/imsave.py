import os
from pathlib import Path


def imsave(fname, arr, vmin=None, vmax=None, cmap=None, format=None,
           origin=None, dpi=100, *, metadata=None, pil_kwargs=None):
    """
    Colormap and save an array as an image file.

    RGB(A) images are passed through.  Single channel images will be
    colormapped according to *cmap* and *norm*.

    .. note::

       If you want to save a single channel image as gray scale please use an
       image I/O library (such as pillow, tifffile, or imageio) directly.

    Parameters
    ----------
    fname : str or path-like or file-like
        A path or a file-like object to store the image in.
        If *format* is not set, then the output format is inferred from the
        extension of *fname*, if any, and from :rc:`savefig.format` otherwise.
        If *format* is set, it determines the output format.
    arr : array-like
        The image data. Accepts NumPy arrays or sequences
        (e.g., lists or tuples). The shape can be one of
        MxN (luminance), MxNx3 (RGB) or MxNx4 (RGBA).
    vmin, vmax : float, optional
        *vmin* and *vmax* set the color scaling for the image by fixing the
        values that map to the colormap color limits. If either *vmin*
        or *vmax* is None, that limit is determined from the *arr*
        min/max value.
    cmap : str or `~matplotlib.colors.Colormap`, default: :rc:`image.cmap`
        A Colormap instance or registered colormap name. The colormap
        maps scalar data to colors. It is ignored for RGB(A) data.
    format : str, optional
        The file format, e.g. 'png', 'pdf', 'svg', ...  The behavior when this
        is unset is documented under *fname*.
    origin : {'upper', 'lower'}, default: :rc:`image.origin`
        Indicates whether the ``(0, 0)`` index of the array is in the upper
        left or lower left corner of the Axes.
    dpi : float
        The DPI to store in the metadata of the file.  This does not affect the
        resolution of the output image.  Depending on file format, this may be
        rounded to the nearest integer.
    metadata : dict, optional
        Metadata in the image file.  The supported keys depend on the output
        format, see the documentation of the respective backends for more
        information.
        Currently only supported for "png", "pdf", "ps", "eps", and "svg".
    pil_kwargs : dict, optional
        Keyword arguments passed to `PIL.Image.Image.save`.  If the 'pnginfo'
        key is present, it completely overrides *metadata*, including the
        default 'Software' key.
    """
    from matplotlib.figure import Figure

    # Normalizing input (e.g., list or tuples) to NumPy array if needed
    arr = np.asanyarray(arr)

    if isinstance(fname, os.PathLike):
        fname = os.fspath(fname)
    if format is None:
        format = (Path(fname).suffix[1:] if isinstance(fname, str)
                  else mpl.rcParams["savefig.format"]).lower()
    if format in ["pdf", "ps", "eps", "svg"]:
        # Vector formats that are not handled by PIL.
        if pil_kwargs is not None:
            raise ValueError(
                f"Cannot use 'pil_kwargs' when saving to {format}")
        fig = Figure(dpi=dpi, frameon=False)
        fig.figimage(arr, cmap=cmap, vmin=vmin, vmax=vmax, origin=origin,
                     resize=True)
        fig.savefig(fname, dpi=dpi, format=format, transparent=True,
                    metadata=metadata)
    else:
        # Don't bother creating an image; this avoids rounding errors on the
        # size when dividing and then multiplying by dpi.
        origin = mpl._val_or_rc(origin, "image.origin")
        _api.check_in_list(('upper', 'lower'), origin=origin)
        if origin == "lower":
            arr = arr[::-1]
        if (isinstance(arr, memoryview) and arr.format == "B"
                and arr.ndim == 3 and arr.shape[-1] == 4):
            # Such an ``arr`` would also be handled fine by sm.to_rgba below
            # (after casting with asarray), but it is useful to special-case it
            # because that's what backend_agg passes, and can be in fact used
            # as is, saving a few operations.
            rgba = arr
        else:
            sm = mcolorizer.Colorizer(cmap=cmap)
            sm.set_clim(vmin, vmax)
            rgba = sm.to_rgba(arr, bytes=True)
        if pil_kwargs is None:
            pil_kwargs = {}
        else:
            # we modify this below, so make a copy (don't modify caller's dict)
            pil_kwargs = pil_kwargs.copy()
        pil_shape = (rgba.shape[1], rgba.shape[0])
        rgba = np.require(rgba, requirements='C')
        image = PIL.Image.frombuffer(
            "RGBA", pil_shape, rgba, "raw", "RGBA", 0, 1)
        if format == "png":
            # Only use the metadata kwarg if pnginfo is not set, because the
            # semantics of duplicate keys in pnginfo is unclear.
            if "pnginfo" in pil_kwargs:
                if metadata:
                    _api.warn_external("'metadata' is overridden by the "
                                       "'pnginfo' entry in 'pil_kwargs'.")
            else:
                metadata = {
                    "Software": (f"Matplotlib version{mpl.__version__}, "
                                 f"https://matplotlib.org/"),
                    **(metadata if metadata is not None else {}),
                }
                pil_kwargs["pnginfo"] = pnginfo = PIL.PngImagePlugin.PngInfo()
                for k, v in metadata.items():
                    if v is not None:
                        pnginfo.add_text(k, v)
        elif metadata is not None:
            raise ValueError(f"metadata not supported for format {format!r}")
        if format in ["jpg", "jpeg"]:
            format = "jpeg"  # Pillow doesn't recognize "jpg".
            facecolor = mpl.rcParams["savefig.facecolor"]
            if cbook._str_equal(facecolor, "auto"):
                facecolor = mpl.rcParams["figure.facecolor"]
            color = tuple(int(x * 255) for x in mcolors.to_rgb(facecolor))
            background = PIL.Image.new("RGB", pil_shape, color)
            background.paste(image, image)
            image = background
        pil_kwargs.setdefault("format", format)
        pil_kwargs.setdefault("dpi", (dpi, dpi))
        image.save(fname, **pil_kwargs)


def imsave(
    fname: str | os.PathLike | BinaryIO, arr: ArrayLike, **kwargs
) -> None:
    matplotlib.image.imsave(fname, arr, **kwargs)

