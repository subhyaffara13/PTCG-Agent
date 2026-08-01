
def test_suite(options, args):
    """
    Create a PNG test image and write the file to stdout.
    """

    # Below is a big stack of test image generators.
    # They're all really tiny, so PEP 8 rules are suspended.

    def test_gradient_horizontal_lr(x, y):
        return x

    def test_gradient_horizontal_rl(x, y):
        return 1 - x

    def test_gradient_vertical_tb(x, y):
        return y

    def test_gradient_vertical_bt(x, y):
        return 1 - y

    def test_radial_tl(x, y):
        return max(1 - math.sqrt(x * x + y * y), 0.0)

    def test_radial_center(x, y):
        return test_radial_tl(x - 0.5, y - 0.5)

    def test_radial_tr(x, y):
        return test_radial_tl(1 - x, y)

    def test_radial_bl(x, y):
        return test_radial_tl(x, 1 - y)

    def test_radial_br(x, y):
        return test_radial_tl(1 - x, 1 - y)

    def test_stripe(x, n):
        return float(int(x * n) & 1)

    def test_stripe_h_2(x, y):
        return test_stripe(x, 2)

    def test_stripe_h_4(x, y):
        return test_stripe(x, 4)

    def test_stripe_h_10(x, y):
        return test_stripe(x, 10)

    def test_stripe_v_2(x, y):
        return test_stripe(y, 2)

    def test_stripe_v_4(x, y):
        return test_stripe(y, 4)

    def test_stripe_v_10(x, y):
        return test_stripe(y, 10)

    def test_stripe_lr_10(x, y):
        return test_stripe(x + y, 10)

    def test_stripe_rl_10(x, y):
        return test_stripe(1 + x - y, 10)

    def test_checker(x, y, n):
        return float((int(x * n) & 1) ^ (int(y * n) & 1))

    def test_checker_8(x, y):
        return test_checker(x, y, 8)

    def test_checker_15(x, y):
        return test_checker(x, y, 15)

    def test_zero(x, y):
        return 0

    def test_one(x, y):
        return 1

    test_patterns = {
        "GLR": test_gradient_horizontal_lr,
        "GRL": test_gradient_horizontal_rl,
        "GTB": test_gradient_vertical_tb,
        "GBT": test_gradient_vertical_bt,
        "RTL": test_radial_tl,
        "RTR": test_radial_tr,
        "RBL": test_radial_bl,
        "RBR": test_radial_br,
        "RCTR": test_radial_center,
        "HS2": test_stripe_h_2,
        "HS4": test_stripe_h_4,
        "HS10": test_stripe_h_10,
        "VS2": test_stripe_v_2,
        "VS4": test_stripe_v_4,
        "VS10": test_stripe_v_10,
        "LRS": test_stripe_lr_10,
        "RLS": test_stripe_rl_10,
        "CK8": test_checker_8,
        "CK15": test_checker_15,
        "ZERO": test_zero,
        "ONE": test_one,
    }

    def test_pattern(width, height, bitdepth, pattern):
        """Create a single plane (monochrome) test pattern.  Returns a
        flat row flat pixel array.
        """

        maxval = 2**bitdepth - 1
        if maxval > 255:
            a = array("H")
        else:
            a = array("B")
        fw = float(width)
        fh = float(height)
        pfun = test_patterns[pattern]
        for y in range(height):
            fy = float(y) / fh
            for x in range(width):
                a.append(int(round(pfun(float(x) / fw, fy) * maxval)))
        return a

    def test_rgba(size=256, bitdepth=8, red="GTB", green="GLR", blue="RTL", alpha=None):
        """
        Create a test image.  Each channel is generated from the
        specified pattern; any channel apart from red can be set to
        None, which will cause it not to be in the image.  It
        is possible to create all PNG channel types (L, RGB, LA, RGBA),
        as well as non PNG channel types (RGA, and so on).
        """

        i = test_pattern(size, size, bitdepth, red)
        psize = 1
        for channel in (green, blue, alpha):
            if channel:
                c = test_pattern(size, size, bitdepth, channel)
                i = interleave_planes(i, c, psize, 1)
                psize += 1
        return i

    def pngsuite_image(name):
        """
        Create a test image by reading an internal copy of the files
        from the PngSuite.  Returned in flat row flat pixel format.
        """

        if name not in _pngsuite:
            raise NotImplementedError(
                f"cannot find PngSuite file {name} (use -L for a list)"
            )
        r = Reader(bytes=_pngsuite[name])
        w, h, pixels, meta = r.asDirect()
        assert w == h
        # LAn for n < 8 is a special case for which we need to rescale
        # the data.
        if meta["greyscale"] and meta["alpha"] and meta["bitdepth"] < 8:
            factor = 255 // (2 ** meta["bitdepth"] - 1)

            def rescale(data):
                for row in data:
                    yield map(factor.__mul__, row)

            pixels = rescale(pixels)
            meta["bitdepth"] = 8
        arraycode = "BH"[meta["bitdepth"] > 8]
        return w, array(arraycode, itertools.chain(*pixels)), meta

    # The body of test_suite()
    size = 256
    if options.test_size:
        size = options.test_size
    options.bitdepth = options.test_depth
    options.greyscale = bool(options.test_black)

    kwargs = {}
    if options.test_red:
        kwargs["red"] = options.test_red
    if options.test_green:
        kwargs["green"] = options.test_green
    if options.test_blue:
        kwargs["blue"] = options.test_blue
    if options.test_alpha:
        kwargs["alpha"] = options.test_alpha
    if options.greyscale:
        if options.test_red or options.test_green or options.test_blue:
            raise ValueError(
                "cannot specify colours (R, G, B) when greyscale image (black channel, K) is specified"
            )
        kwargs["red"] = options.test_black
        kwargs["green"] = None
        kwargs["blue"] = None
    options.alpha = bool(options.test_alpha)
    if not args:
        pixels = test_rgba(size, options.bitdepth, **kwargs)
    else:
        size, pixels, meta = pngsuite_image(args[0])
        for k in ["bitdepth", "alpha", "greyscale"]:
            setattr(options, k, meta[k])

    writer = Writer(
        size,
        size,
        bitdepth=options.bitdepth,
        transparent=options.transparent,
        background=options.background,
        gamma=options.gamma,
        greyscale=options.greyscale,
        alpha=options.alpha,
        compression=options.compression,
        interlace=options.interlace,
    )
    writer.write_array(sys.stdout, pixels)

