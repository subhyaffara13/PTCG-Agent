import os
import sys

def pilinfo(out: IO[str] | None = None, supported_formats: bool = True) -> None:
    """
    Prints information about this installation of Pillow.
    This function can be called with ``python3 -m PIL``.
    It can also be called with ``python3 -m PIL.report`` or ``python3 -m PIL --report``
    to have "supported_formats" set to ``False``, omitting the list of all supported
    image file formats.

    :param out:
        The output stream to print to. Defaults to ``sys.stdout`` if ``None``.
    :param supported_formats:
        If ``True``, a list of all supported image file formats will be printed.
    """

    if out is None:
        out = sys.stdout

    Image.init()

    print("-" * 68, file=out)
    print(f"Pillow {PIL.__version__}", file=out)
    py_version_lines = sys.version.splitlines()
    print(f"Python {py_version_lines[0].strip()}", file=out)
    for py_version in py_version_lines[1:]:
        print(f"       {py_version.strip()}", file=out)
    print("-" * 68, file=out)
    print(f"Python executable is {sys.executable or 'unknown'}", file=out)
    if sys.prefix != sys.base_prefix:
        print(f"Environment Python files loaded from {sys.prefix}", file=out)
    print(f"System Python files loaded from {sys.base_prefix}", file=out)
    print("-" * 68, file=out)
    print(
        f"Python Pillow modules loaded from {os.path.dirname(Image.__file__)}",
        file=out,
    )
    print(
        f"Binary Pillow modules loaded from {os.path.dirname(Image.core.__file__)}",
        file=out,
    )
    print("-" * 68, file=out)

    for name, feature in [
        ("pil", "PIL CORE"),
        ("tkinter", "TKINTER"),
        ("freetype2", "FREETYPE2"),
        ("littlecms2", "LITTLECMS2"),
        ("webp", "WEBP"),
        ("avif", "AVIF"),
        ("jpg", "JPEG"),
        ("jpg_2000", "OPENJPEG (JPEG2000)"),
        ("zlib", "ZLIB (PNG/ZIP)"),
        ("libtiff", "LIBTIFF"),
        ("raqm", "RAQM (Bidirectional Text)"),
        ("libimagequant", "LIBIMAGEQUANT (Quantization method)"),
        ("xcb", "XCB (X protocol)"),
    ]:
        if check(name):
            v: str | None = None
            if name == "jpg":
                libjpeg_turbo_version = version_feature("libjpeg_turbo")
                if libjpeg_turbo_version is not None:
                    v = "mozjpeg" if check_feature("mozjpeg") else "libjpeg-turbo"
                    v += " " + libjpeg_turbo_version
            if v is None:
                v = version(name)
            if v is not None:
                version_static = name in ("pil", "jpg")
                if name == "littlecms2":
                    # this check is also in src/_imagingcms.c:setup_module()
                    version_static = tuple(int(x) for x in v.split(".")) < (2, 7)
                t = "compiled for" if version_static else "loaded"
                if name == "zlib":
                    zlib_ng_version = version_feature("zlib_ng")
                    if zlib_ng_version is not None:
                        v += ", compiled for zlib-ng " + zlib_ng_version
                elif name == "raqm":
                    for f in ("fribidi", "harfbuzz"):
                        v2 = version_feature(f)
                        if v2 is not None:
                            v += f", {f} {v2}"
                print("---", feature, "support ok,", t, v, file=out)
            else:
                print("---", feature, "support ok", file=out)
        else:
            print("***", feature, "support not installed", file=out)
    print("-" * 68, file=out)

    if supported_formats:
        extensions = collections.defaultdict(list)
        for ext, i in Image.EXTENSION.items():
            extensions[i].append(ext)

        for i in sorted(Image.ID):
            line = f"{i}"
            if i in Image.MIME:
                line = f"{line} {Image.MIME[i]}"
            print(line, file=out)

            if i in extensions:
                print(
                    "Extensions: {}".format(", ".join(sorted(extensions[i]))), file=out
                )

            features = []
            if i in Image.OPEN:
                features.append("open")
            if i in Image.SAVE:
                features.append("save")
            if i in Image.SAVE_ALL:
                features.append("save_all")
            if i in Image.DECODERS:
                features.append("decode")
            if i in Image.ENCODERS:
                features.append("encode")

            print("Features: {}".format(", ".join(features)), file=out)
            print("-" * 68, file=out)

