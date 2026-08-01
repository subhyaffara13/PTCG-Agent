
def grab(
    bbox: tuple[int, int, int, int] | None = None,
    include_layered_windows: bool = False,
    all_screens: bool = False,
    xdisplay: str | None = None,
    window: int | ImageWin.HWND | None = None,
    *,
    scale_down: bool = False,
) -> Image.Image:
    im: Image.Image
    if xdisplay is None:
        if sys.platform == "darwin":
            fh, filepath = tempfile.mkstemp(".png")
            os.close(fh)
            args = ["screencapture"]
            if window is not None:
                args += ["-l", str(window)]
            elif bbox:
                left, top, right, bottom = bbox
                args += ["-R", f"{left},{top},{right-left},{bottom-top}"]
            args += ["-x", filepath]
            retcode = subprocess.call(args)
            if retcode:
                raise subprocess.CalledProcessError(retcode, args)
            im = Image.open(filepath)
            im.load()
            os.unlink(filepath)
            if bbox:
                if window is not None:
                    # Determine if the window was in Retina mode or not
                    # by capturing it without the shadow,
                    # and checking how different the width is
                    fh, filepath = tempfile.mkstemp(".png")
                    os.close(fh)
                    args = ["screencapture", "-l", str(window), "-o", "-x", filepath]
                    retcode = subprocess.call(args)
                    if retcode:
                        raise subprocess.CalledProcessError(retcode, args)
                    with Image.open(filepath) as im_no_shadow:
                        retina = im.width - im_no_shadow.width > 100
                    os.unlink(filepath)

                    # Since screencapture's -R does not work with -l,
                    # crop the image manually
                    if retina:
                        left, top, right, bottom = bbox
                        scale = 1 if scale_down else 2
                        im_cropped = im.resize(
                            ((right - left) * scale, (bottom - top) * scale),
                            box=tuple(coord * 2 for coord in bbox),
                        )
                    else:
                        im_cropped = im.crop(bbox)
                    im.close()
                    return im_cropped
                elif scale_down:
                    im_resized = im.resize((right - left, bottom - top))
                    im.close()
                    return im_resized
            return im
        elif sys.platform == "win32":
            if window is not None:
                all_screens = -1
            offset, size, data = Image.core.grabscreen_win32(
                include_layered_windows,
                all_screens,
                int(window) if window is not None else 0,
            )
            im = Image.frombytes(
                "RGB",
                size,
                data,
                # RGB, 32-bit line padding, origin lower left corner
                "raw",
                "BGR",
                (size[0] * 3 + 3) & -4,
                -1,
            )
            if bbox:
                x0, y0 = offset
                left, top, right, bottom = bbox
                im = im.crop((left - x0, top - y0, right - x0, bottom - y0))
            return im
    # Cast to Optional[str] needed for Windows and macOS.
    display_name: str | None = xdisplay
    try:
        if not Image.core.HAVE_XCB:
            msg = "Pillow was built without XCB support"
            raise OSError(msg)
        size, data = Image.core.grabscreen_x11(display_name)
    except OSError:
        if display_name is None and sys.platform not in ("darwin", "win32"):
            if shutil.which("gnome-screenshot"):
                args = ["gnome-screenshot", "-f"]
            elif shutil.which("grim"):
                args = ["grim"]
            elif shutil.which("spectacle"):
                args = ["spectacle", "-n", "-b", "-f", "-o"]
            else:
                raise
            fh, filepath = tempfile.mkstemp(".png")
            os.close(fh)
            args.append(filepath)
            retcode = subprocess.call(args)
            if retcode:
                raise subprocess.CalledProcessError(retcode, args)
            im = Image.open(filepath)
            im.load()
            os.unlink(filepath)
            if bbox:
                im_cropped = im.crop(bbox)
                im.close()
                return im_cropped
            return im
        else:
            raise
    else:
        im = Image.frombytes("RGB", size, data, "raw", "BGRX", size[0] * 4, 1)
        if bbox:
            im = im.crop(bbox)
        return im

