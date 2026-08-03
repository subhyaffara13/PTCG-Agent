import os
import sys

def testit(importdir='', testdir='', exit_on_fail=False):
    """Run all tests in testdir while importing from importdir."""
    if importdir:
        sys.path.insert(1, importdir)
    if testdir:
        sys.path.insert(1, testdir)
    import os.path
    import mpmath
    print("mpmath imported from %s" % os.path.dirname(mpmath.__file__))
    print("mpmath backend: %s" % mpmath.libmp.backend.BACKEND)
    print("mpmath mp class: %s" % repr(mpmath.mp))
    print("mpmath version: %s" % mpmath.__version__)
    print("Python version: %s" % sys.version)
    print("")
    if "-py" in sys.argv:
        sys.argv.remove('-py')
        import py
        py.test.cmdline.main()
    else:
        import glob
        from timeit import default_timer as clock
        modules = []
        args = sys.argv[1:]
        excluded = []
        if '-skip' in args:
            excluded = args[args.index('-skip')+1:]
            args = args[:args.index('-skip')]
        # search for tests in directory of this file if not otherwise specified
        if not testdir:
            pattern = os.path.dirname(sys.argv[0])
        else:
            pattern = testdir
        if pattern:
            pattern += '/'
        pattern += 'test*.py'
        # look for tests (respecting specified filter)
        for f in glob.glob(pattern):
            name = os.path.splitext(os.path.basename(f))[0]
            # If run as a script, only run tests given as args, if any are given
            if args and __name__ == "__main__":
                ok = False
                for arg in args:
                    if arg in name:
                        ok = True
                        break
                if not ok:
                    continue
            elif name in excluded:
                continue
            module = __import__(name)
            priority = module.__dict__.get('priority', 100)
            if priority == 666:
                modules = [[priority, name, module]]
                break
            modules.append([priority, name, module])
        # execute tests
        modules.sort()
        tstart = clock()
        for priority, name, module in modules:
            print(name)
            for f in sorted(module.__dict__.keys()):
                if f.startswith('test_'):
                    if coverage and ('numpy' in f):
                        continue
                    sys.stdout.write("    " + f[5:].ljust(25) + " ")
                    t1 = clock()
                    try:
                        module.__dict__[f]()
                    except:
                        etype, evalue, trb = sys.exc_info()
                        if etype in (KeyboardInterrupt, SystemExit):
                            raise
                        print("")
                        print("TEST FAILED!")
                        print("")
                        traceback.print_exc()
                        if exit_on_fail:
                            return
                    t2 = clock()
                    print("ok " + "       " + ("%.7f" % (t2-t1)) + " s")
        tend = clock()
        print("")
        print("finished tests in " + ("%.2f" % (tend-tstart)) + " seconds")
        # clean sys.path
        if importdir:
            sys.path.remove(importdir)
        if testdir:
            sys.path.remove(testdir)


def testit(line):
    if filt in line:
        print(line)
        t1 = clock()
        exec_(line, globals(), locals())
        t2 = clock()
        elapsed = t2-t1
        print("Time:", elapsed, "for", line, "(OK)")

