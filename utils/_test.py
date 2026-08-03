import os
import random

def _test(n, base, s, t):
    """Miller-Rabin strong pseudoprime test for one base.
    Return False if n is definitely composite, True if n is
    probably prime, with a probability greater than 3/4.

    """
    # do the Fermat test
    b = pow(base, t, n)
    if b == 1 or b == n - 1:
        return True
    for _ in range(s - 1):
        b = pow(b, 2, n)
        if b == n - 1:
            return True
        # see I. Niven et al. "An Introduction to Theory of Numbers", page 78
        if b == 1:
            return False
    return False


def _test(*paths,
        verbose=False, tb="short", kw=None, pdb=False, colors=True,
        force_colors=False, sort=True, seed=None, timeout=False,
        fail_on_timeout=False, slow=False, enhance_asserts=False, split=None,
        time_balance=True, blacklist=(),
        fast_threshold=None, slow_threshold=None):
    """
    Internal function that actually runs the tests.

    All keyword arguments from ``test()`` are passed to this function except for
    ``subprocess``.

    Returns 0 if tests passed and 1 if they failed.  See the docstring of
    ``test()`` for more information.
    """
    kw = kw or ()
    # ensure that kw is a tuple
    if isinstance(kw, str):
        kw = (kw,)
    post_mortem = pdb
    if seed is None:
        seed = random.randrange(100000000)
    if ON_CI and timeout is False:
        timeout = 595
        fail_on_timeout = True
    if ON_CI:
        blacklist = list(blacklist) + ['sympy/plotting/pygletplot/tests']
    blacklist = convert_to_native_paths(blacklist)
    r = PyTestReporter(verbose=verbose, tb=tb, colors=colors,
        force_colors=force_colors, split=split)
    # This won't strictly run the test for the corresponding file, but it is
    # good enough for copying and pasting the failing test.
    _paths = []
    for path in paths:
        if '::' in path:
            path, _kw = path.split('::', 1)
            kw += (_kw,)
        _paths.append(path)
    paths = _paths

    t = SymPyTests(r, kw, post_mortem, seed,
                   fast_threshold=fast_threshold,
                   slow_threshold=slow_threshold)

    test_files = t.get_test_files('sympy')

    not_blacklisted = [f for f in test_files
                       if not any(b in f for b in blacklist)]

    if len(paths) == 0:
        matched = not_blacklisted
    else:
        paths = convert_to_native_paths(paths)
        matched = []
        for f in not_blacklisted:
            basename = os.path.basename(f)
            for p in paths:
                if p in f or fnmatch(basename, p):
                    matched.append(f)
                    break

    density = None
    if time_balance:
        if slow:
            density = SPLIT_DENSITY_SLOW
        else:
            density = SPLIT_DENSITY

    if split:
        matched = split_list(matched, split, density=density)

    t._testfiles.extend(matched)

    return int(not t.test(sort=sort, timeout=timeout, slow=slow,
        enhance_asserts=enhance_asserts, fail_on_timeout=fail_on_timeout))


def _test(number, number_type, read_offset, should_byteswap):
    number = number_type(number)
    data = np.random.default_rng(2).integers(0, 256, size=20, dtype="uint8")
    data[read_offset : read_offset + number.itemsize] = number[None].view("uint8")
    swap_func = {
        np.float32: read_float_with_byteswap,
        np.float64: read_double_with_byteswap,
        np.uint16: read_uint16_with_byteswap,
        np.uint32: read_uint32_with_byteswap,
        np.uint64: read_uint64_with_byteswap,
    }[type(number)]
    output_number = number_type(swap_func(bytes(data), read_offset, should_byteswap))
    if should_byteswap:
        tm.assert_equal(output_number, number.byteswap())
    else:
        tm.assert_equal(output_number, number)


def _test():
    """
    >>> import math
    >>> calcBounds([])
    (0, 0, 0, 0)
    >>> calcBounds([(0, 40), (0, 100), (50, 50), (80, 10)])
    (0, 10, 80, 100)
    >>> updateBounds((0, 0, 0, 0), (100, 100))
    (0, 0, 100, 100)
    >>> pointInRect((50, 50), (0, 0, 100, 100))
    True
    >>> pointInRect((0, 0), (0, 0, 100, 100))
    True
    >>> pointInRect((100, 100), (0, 0, 100, 100))
    True
    >>> not pointInRect((101, 100), (0, 0, 100, 100))
    True
    >>> list(pointsInRect([(50, 50), (0, 0), (100, 100), (101, 100)], (0, 0, 100, 100)))
    [True, True, True, False]
    >>> vectorLength((3, 4))
    5.0
    >>> vectorLength((1, 1)) == math.sqrt(2)
    True
    >>> list(asInt16([0, 0.1, 0.5, 0.9]))
    [0, 0, 1, 1]
    >>> normRect((0, 10, 100, 200))
    (0, 10, 100, 200)
    >>> normRect((100, 200, 0, 10))
    (0, 10, 100, 200)
    >>> scaleRect((10, 20, 50, 150), 1.5, 2)
    (15.0, 40, 75.0, 300)
    >>> offsetRect((10, 20, 30, 40), 5, 6)
    (15, 26, 35, 46)
    >>> insetRect((10, 20, 50, 60), 5, 10)
    (15, 30, 45, 50)
    >>> insetRect((10, 20, 50, 60), -5, -10)
    (5, 10, 55, 70)
    >>> intersects, rect = sectRect((0, 10, 20, 30), (0, 40, 20, 50))
    >>> not intersects
    True
    >>> intersects, rect = sectRect((0, 10, 20, 30), (5, 20, 35, 50))
    >>> intersects
    1
    >>> rect
    (5, 20, 20, 30)
    >>> unionRect((0, 10, 20, 30), (0, 40, 20, 50))
    (0, 10, 20, 50)
    >>> rectCenter((0, 0, 100, 200))
    (50.0, 100.0)
    >>> rectCenter((0, 0, 100, 199.0))
    (50.0, 99.5)
    >>> intRect((0.9, 2.9, 3.1, 4.1))
    (0, 2, 4, 5)
    """


def _test():
    fmt = """
		# comments are allowed
		>  # big endian (see documentation for struct)
		# empty lines are allowed:

		ashort: h
		along: l
		abyte: b	# a byte
		achar: c
		astr: 5s
		afloat: f; adouble: d	# multiple "statements" are allowed
		afixed: 16.16F
		abool: ?
		apad: x
	"""

    print("size:", calcsize(fmt))

    class foo(object):
        pass

    i = foo()

    i.ashort = 0x7FFF
    i.along = 0x7FFFFFFF
    i.abyte = 0x7F
    i.achar = "a"
    i.astr = "12345"
    i.afloat = 0.5
    i.adouble = 0.5
    i.afixed = 1.5
    i.abool = True

    data = pack(fmt, i)
    print("data:", repr(data))
    print(unpack(fmt, data))
    i2 = foo()
    unpack(fmt, data, i2)
    print(vars(i2))


def _test(glyphset, upem, glyphs, quiet=False, *, control=False):
    from fontTools.pens.transformPen import TransformPen
    from fontTools.misc.transform import Scale

    wght_sum = 0
    wght_sum_perceptual = 0
    wdth_sum = 0
    slnt_sum = 0
    slnt_sum_perceptual = 0
    for glyph_name in glyphs:
        glyph = glyphset[glyph_name]
        if control:
            pen = StatisticsControlPen(glyphset=glyphset)
        else:
            pen = StatisticsPen(glyphset=glyphset)
        transformer = TransformPen(pen, Scale(1.0 / upem))
        glyph.draw(transformer)

        area = abs(pen.area)
        width = glyph.width
        wght_sum += area
        wght_sum_perceptual += pen.area * width
        wdth_sum += width
        slnt_sum += pen.slant
        slnt_sum_perceptual += pen.slant * width

        if quiet:
            continue

        print()
        print("glyph:", glyph_name)

        for item in [
            "area",
            "momentX",
            "momentY",
            "momentXX",
            "momentYY",
            "momentXY",
            "meanX",
            "meanY",
            "varianceX",
            "varianceY",
            "stddevX",
            "stddevY",
            "covariance",
            "correlation",
            "slant",
        ]:
            print("%s: %g" % (item, getattr(pen, item)))

    if not quiet:
        print()
        print("font:")

    print("weight: %g" % (wght_sum * upem / wdth_sum))
    print("weight (perceptual): %g" % (wght_sum_perceptual / wdth_sum))
    print("width:  %g" % (wdth_sum / upem / len(glyphs)))
    slant = slnt_sum / len(glyphs)
    print("slant:  %g" % slant)
    print("slant angle:  %g" % -degrees(atan(slant)))
    slant_perceptual = slnt_sum_perceptual / wdth_sum
    print("slant (perceptual):  %g" % slant_perceptual)
    print("slant (perceptual) angle:  %g" % -degrees(atan(slant_perceptual)))


def _test():
    """
    >>> _test()
    True
    """

    bc = b"""@;:9876543210/.-,+*)(\'&%$#"! \037\036\035\034\033\032\031\030\027\026\025\024\023\022\021\020\017\016\015\014\013\012\011\010\007\006\005\004\003\002\001\000,\001\260\030CXEj\260\031C`\260F#D#\020 \260FN\360M/\260\000\022\033!#\0213Y-,\001\260\030CX\260\005+\260\000\023K\260\024PX\261\000@8Y\260\006+\033!#\0213Y-,\001\260\030CXN\260\003%\020\362!\260\000\022M\033 E\260\004%\260\004%#Jad\260(RX!#\020\326\033\260\003%\020\362!\260\000\022YY-,\260\032CX!!\033\260\002%\260\002%I\260\003%\260\003%Ja d\260\020PX!!!\033\260\003%\260\003%I\260\000PX\260\000PX\270\377\3428!\033\260\0208!Y\033\260\000RX\260\0368!\033\270\377\3608!YYYY-,\001\260\030CX\260\005+\260\000\023K\260\024PX\271\000\000\377\3008Y\260\006+\033!#\0213Y-,N\001\212\020\261F\031CD\260\000\024\261\000F\342\260\000\025\271\000\000\377\3608\000\260\000<\260(+\260\002%\020\260\000<-,\001\030\260\000/\260\001\024\362\260\001\023\260\001\025M\260\000\022-,\001\260\030CX\260\005+\260\000\023\271\000\000\377\3408\260\006+\033!#\0213Y-,\001\260\030CXEdj#Edi\260\031Cd``\260F#D#\020 \260F\360/\260\000\022\033!! \212 \212RX\0213\033!!YY-,\001\261\013\012C#Ce\012-,\000\261\012\013C#C\013-,\000\260F#p\261\001F>\001\260F#p\261\002FE:\261\002\000\010\015-,\260\022+\260\002%E\260\002%Ej\260@\213`\260\002%#D!!!-,\260\023+\260\002%E\260\002%Ej\270\377\300\214`\260\002%#D!!!-,\260\000\260\022+!!!-,\260\000\260\023+!!!-,\001\260\006C\260\007Ce\012-, i\260@a\260\000\213 \261,\300\212\214\270\020\000b`+\014d#da\\X\260\003aY-,\261\000\003%EhT\260\034KPZX\260\003%E\260\003%E`h \260\004%#D\260\004%#D\033\260\003% Eh \212#D\260\003%Eh`\260\003%#DY-,\260\003% Eh \212#D\260\003%Edhe`\260\004%\260\001`#D-,\260\011CX\207!\300\033\260\022CX\207E\260\021+\260G#D\260Gz\344\033\003\212E\030i \260G#D\212\212\207 \260\240QX\260\021+\260G#D\260Gz\344\033!\260Gz\344YYY\030-, \212E#Eh`D-,EjB-,\001\030/-,\001\260\030CX\260\004%\260\004%Id#Edi\260@\213a \260\200bj\260\002%\260\002%a\214\260\031C`\260F#D!\212\020\260F\366!\033!!!!Y-,\001\260\030CX\260\002%E\260\002%Ed`j\260\003%Eja \260\004%Ej \212\213e\260\004%#D\214\260\003%#D!!\033 EjD EjDY-,\001 E\260\000U\260\030CZXEh#Ei\260@\213a \260\200bj \212#a \260\003%\213e\260\004%#D\214\260\003%#D!!\033!!\260\031+Y-,\001\212\212Ed#EdadB-,\260\004%\260\004%\260\031+\260\030CX\260\004%\260\004%\260\003%\260\033+\001\260\002%C\260@T\260\002%C\260\000TZX\260\003% E\260@aDY\260\002%C\260\000T\260\002%C\260@TZX\260\004% E\260@`DYY!!!!-,\001KRXC\260\002%E#aD\033!!Y-,\001KRXC\260\002%E#`D\033!!Y-,KRXED\033!!Y-,\001 \260\003%#I\260@`\260 c \260\000RX#\260\002%8#\260\002%e8\000\212c8\033!!!!!Y\001-,KPXED\033!!Y-,\001\260\005%\020# \212\365\000\260\001`#\355\354-,\001\260\005%\020# \212\365\000\260\001a#\355\354-,\001\260\006%\020\365\000\355\354-,F#F`\212\212F# F\212`\212a\270\377\200b# \020#\212\261KK\212pE` \260\000PX\260\001a\270\377\272\213\033\260F\214Y\260\020`h\001:-, E\260\003%FRX\260\002%F ha\260\003%\260\003%?#!8\033!\021Y-, E\260\003%FPX\260\002%F ha\260\003%\260\003%?#!8\033!\021Y-,\000\260\007C\260\006C\013-,\212\020\354-,\260\014CX!\033 F\260\000RX\270\377\3608\033\260\0208YY-, \260\000UX\270\020\000c\260\003%Ed\260\003%Eda\260\000SX\260\002\033\260@a\260\003Y%EiSXED\033!!Y\033!\260\002%E\260\002%Ead\260(QXED\033!!YY-,!!\014d#d\213\270@\000b-,!\260\200QX\014d#d\213\270 \000b\033\262\000@/+Y\260\002`-,!\260\300QX\014d#d\213\270\025Ub\033\262\000\200/+Y\260\002`-,\014d#d\213\270@\000b`#!-,KSX\260\004%\260\004%Id#Edi\260@\213a \260\200bj\260\002%\260\002%a\214\260F#D!\212\020\260F\366!\033!\212\021#\022 9/Y-,\260\002%\260\002%Id\260\300TX\270\377\3708\260\0108\033!!Y-,\260\023CX\003\033\002Y-,\260\023CX\002\033\003Y-,\260\012+#\020 <\260\027+-,\260\002%\270\377\3608\260(+\212\020# \320#\260\020+\260\005CX\300\033<Y \020\021\260\000\022\001-,KS#KQZX8\033!!Y-,\001\260\002%\020\320#\311\001\260\001\023\260\000\024\020\260\001<\260\001\026-,\001\260\000\023\260\001\260\003%I\260\003\0278\260\001\023-,KS#KQZX E\212`D\033!!Y-, 9/-"""

    p = Program()
    p.fromBytecode(bc)
    asm = p.getAssembly(preserve=True)
    p.fromAssembly(asm)
    print(bc == p.getBytecode())

