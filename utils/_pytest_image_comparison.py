
def _pytest_image_comparison(baseline_images, extensions, tol,
                             freetype_version, remove_text, savefig_kwargs,
                             style):
    """
    Decorate function with image comparison for pytest.

    This function creates a decorator that wraps a figure-generating function
    with image comparison code.
    """
    import pytest

    KEYWORD_ONLY = inspect.Parameter.KEYWORD_ONLY

    def decorator(func):
        old_sig = inspect.signature(func)

        @functools.wraps(func)
        @pytest.mark.parametrize('extension', extensions)
        @matplotlib.style.context(style)
        @_checked_on_freetype_version(freetype_version)
        @functools.wraps(func)
        def wrapper(*args, extension, request, **kwargs):
            __tracebackhide__ = True
            if 'extension' in old_sig.parameters:
                kwargs['extension'] = extension
            if 'request' in old_sig.parameters:
                kwargs['request'] = request

            if extension not in comparable_formats():
                reason = {
                    'gif': 'because ImageMagick is not installed',
                    'pdf': 'because Ghostscript is not installed',
                    'eps': 'because Ghostscript is not installed',
                    'svg': 'because Inkscape is not installed',
                }.get(extension, 'on this system')
                pytest.skip(f"Cannot compare {extension} files {reason}")

            img = _ImageComparisonBase(func, tol=tol, remove_text=remove_text,
                                       savefig_kwargs=savefig_kwargs)
            matplotlib.testing.set_font_settings_for_testing()

            with _collect_new_figures() as figs:
                func(*args, **kwargs)

            # If the test is parametrized in any way other than applied via
            # this decorator, then we need to use a lock to prevent two
            # processes from touching the same output file.
            needs_lock = any(
                marker.args[0] != 'extension'
                for marker in request.node.iter_markers('parametrize'))

            if baseline_images is not None:
                our_baseline_images = baseline_images
            else:
                # Allow baseline image list to be produced on the fly based on
                # current parametrization.
                our_baseline_images = request.getfixturevalue(
                    'baseline_images')

            assert len(figs) == len(our_baseline_images), (
                f"Test generated {len(figs)} images but there are "
                f"{len(our_baseline_images)} baseline images")
            for fig, baseline in zip(figs, our_baseline_images):
                img.compare(fig, baseline, extension, _lock=needs_lock)

        parameters = list(old_sig.parameters.values())
        if 'extension' not in old_sig.parameters:
            parameters += [inspect.Parameter('extension', KEYWORD_ONLY)]
        if 'request' not in old_sig.parameters:
            parameters += [inspect.Parameter("request", KEYWORD_ONLY)]
        new_sig = old_sig.replace(parameters=parameters)
        wrapper.__signature__ = new_sig

        # Reach a bit into pytest internals to hoist the marks from our wrapped
        # function.
        new_marks = getattr(func, 'pytestmark', []) + wrapper.pytestmark
        wrapper.pytestmark = new_marks

        return wrapper

    return decorator

