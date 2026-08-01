
def doctests(filter=[]):
    import sys
    from timeit import default_timer as clock
    for i, arg in enumerate(sys.argv):
        if '__init__.py' in arg:
            filter = [sn for sn in sys.argv[i+1:] if not sn.startswith("-")]
            break
    import doctest
    globs = globals().copy()
    for obj in globs: #sorted(globs.keys()):
        if filter:
            if not sum([pat in obj for pat in filter]):
                continue
        sys.stdout.write(str(obj) + " ")
        sys.stdout.flush()
        t1 = clock()
        doctest.run_docstring_examples(globs[obj], {}, verbose=("-v" in sys.argv))
        t2 = clock()
        print(round(t2-t1, 3))

