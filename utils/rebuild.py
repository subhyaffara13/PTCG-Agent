
def rebuild(expr):
    """ Rebuild a SymPy tree.

    Explanation
    ===========

    This function recursively calls constructors in the expression tree.
    This forces canonicalization and removes ugliness introduced by the use of
    Basic.__new__
    """
    if expr.is_Atom:
        return expr
    else:
        return expr.func(*list(map(rebuild, expr.args)))


def rebuild(s):
    """ Rebuild a SymPy expression.

    This removes harm caused by Expr-Rules interactions.
    """
    return construct(deconstruct(s))


def rebuild(filename, tag=None, format="gz", zonegroups=[], metadata=None):
    """Rebuild the internal timezone info in dateutil/zoneinfo/zoneinfo*tar*

    filename is the timezone tarball from ``ftp.iana.org/tz``.

    """
    tmpdir = tempfile.mkdtemp()
    zonedir = os.path.join(tmpdir, "zoneinfo")
    moduledir = os.path.dirname(__file__)
    try:
        with TarFile.open(filename) as tf:
            for name in zonegroups:
                tf.extract(name, tmpdir)
            filepaths = [os.path.join(tmpdir, n) for n in zonegroups]

            _run_zic(zonedir, filepaths)

        # write metadata file
        with open(os.path.join(zonedir, METADATA_FN), 'w') as f:
            json.dump(metadata, f, indent=4, sort_keys=True)
        target = os.path.join(moduledir, ZONEFILENAME)
        with TarFile.open(target, "w:%s" % format) as tf:
            for entry in os.listdir(zonedir):
                entrypath = os.path.join(zonedir, entry)
                tf.add(entrypath, entry)
    finally:
        shutil.rmtree(tmpdir)

