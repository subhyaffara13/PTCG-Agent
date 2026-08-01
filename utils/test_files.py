
def test_files():
    """
    This test tests all files in SymPy and checks that:
      o no lines contains a trailing whitespace
      o no lines end with \r\n
      o no line uses tabs instead of spaces
      o that the file ends with a single newline
      o there are no general or string exceptions
      o there are no old style raise statements
      o name of arg-less test suite functions start with _ or test_
      o no duplicate function names that start with test_
      o no assignments to self variable in class methods
      o no lines contain ".func is" except in the test suite
      o there is no do-nothing expression like `a == b` or `x + 1`
    """

    def test(fname):
        with open(fname, encoding="utf8") as test_file:
            test_this_file(fname, test_file)
        with open(fname, encoding='utf8') as test_file:
            _test_this_file_encoding(fname, test_file)

    def test_this_file(fname, test_file):
        idx = None
        code = test_file.read()
        test_file.seek(0)  # restore reader to head
        py = fname if sep not in fname else fname.rsplit(sep, 1)[-1]
        if py.startswith('test_'):
            idx = line_with_bare_expr(code)
        if idx is not None:
            assert False, message_bare_expr % (fname, idx + 1)

        line = None  # to flag the case where there were no lines in file
        tests = 0
        test_set = set()
        for idx, line in enumerate(test_file):
            if test_file_re.match(fname):
                if test_suite_def_re.match(line):
                    assert False, message_test_suite_def % (fname, idx + 1)
                if test_ok_def_re.match(line):
                    tests += 1
                    test_set.add(line[3:].split('(')[0].strip())
                    if len(test_set) != tests:
                        assert False, message_duplicate_test % (fname, idx + 1)
            if line.endswith((" \n", "\t\n")):
                assert False, message_space % (fname, idx + 1)
            if line.endswith("\r\n"):
                assert False, message_carriage % (fname, idx + 1)
            if tab_in_leading(line):
                assert False, message_tabs % (fname, idx + 1)
            if str_raise_re.search(line):
                assert False, message_str_raise % (fname, idx + 1)
            if gen_raise_re.search(line):
                assert False, message_gen_raise % (fname, idx + 1)
            if (implicit_test_re.search(line) and
                    not list(filter(lambda ex: ex in fname, import_exclude))):
                assert False, message_implicit % (fname, idx + 1)
            if func_is_re.search(line) and not test_file_re.search(fname):
                assert False, message_func_is % (fname, idx + 1)

            result = old_raise_re.search(line)

            if result is not None:
                assert False, message_old_raise % (
                    fname, idx + 1, result.group(2))

        if line is not None:
            if line == '\n' and idx > 0:
                assert False, message_multi_eof % (fname, idx + 1)
            elif not line.endswith('\n'):
                # eof newline check
                assert False, message_eof % (fname, idx + 1)


    # Files to test at top level
    top_level_files = [join(TOP_PATH, file) for file in [
        "isympy.py",
        "build.py",
        "setup.py",
    ]]
    # Files to exclude from all tests
    exclude = {
        "%(sep)ssympy%(sep)sparsing%(sep)sautolev%(sep)s_antlr%(sep)sautolevparser.py" % sepd,
        "%(sep)ssympy%(sep)sparsing%(sep)sautolev%(sep)s_antlr%(sep)sautolevlexer.py" % sepd,
        "%(sep)ssympy%(sep)sparsing%(sep)sautolev%(sep)s_antlr%(sep)sautolevlistener.py" % sepd,
        "%(sep)ssympy%(sep)sparsing%(sep)slatex%(sep)s_antlr%(sep)slatexparser.py" % sepd,
        "%(sep)ssympy%(sep)sparsing%(sep)slatex%(sep)s_antlr%(sep)slatexlexer.py" % sepd,
    }
    # Files to exclude from the implicit import test
    import_exclude = {
        # glob imports are allowed in top-level __init__.py:
        "%(sep)ssympy%(sep)s__init__.py" % sepd,
        # these __init__.py should be fixed:
        # XXX: not really, they use useful import pattern (DRY)
        "%(sep)svector%(sep)s__init__.py" % sepd,
        "%(sep)smechanics%(sep)s__init__.py" % sepd,
        "%(sep)squantum%(sep)s__init__.py" % sepd,
        "%(sep)spolys%(sep)s__init__.py" % sepd,
        "%(sep)spolys%(sep)sdomains%(sep)s__init__.py" % sepd,
        # interactive SymPy executes ``from sympy import *``:
        "%(sep)sinteractive%(sep)ssession.py" % sepd,
        # isympy.py executes ``from sympy import *``:
        "%(sep)sisympy.py" % sepd,
        # these two are import timing tests:
        "%(sep)sbin%(sep)ssympy_time.py" % sepd,
        "%(sep)sbin%(sep)ssympy_time_cache.py" % sepd,
        # Taken from Python stdlib:
        "%(sep)sparsing%(sep)ssympy_tokenize.py" % sepd,
        # this one should be fixed:
        "%(sep)splotting%(sep)spygletplot%(sep)s" % sepd,
        # False positive in the docstring
        "%(sep)sbin%(sep)stest_external_imports.py" % sepd,
        "%(sep)sbin%(sep)stest_submodule_imports.py" % sepd,
        # These are deprecated stubs that can be removed at some point:
        "%(sep)sutilities%(sep)sruntests.py" % sepd,
        "%(sep)sutilities%(sep)spytest.py" % sepd,
        "%(sep)sutilities%(sep)srandtest.py" % sepd,
        "%(sep)sutilities%(sep)stmpfiles.py" % sepd,
        "%(sep)sutilities%(sep)squality_unicode.py" % sepd,
    }
    check_files(top_level_files, test)
    check_directory_tree(BIN_PATH, test, {"~", ".pyc", ".sh"}, "*")
    check_directory_tree(SYMPY_PATH, test, exclude)
    check_directory_tree(EXAMPLES_PATH, test, exclude)

