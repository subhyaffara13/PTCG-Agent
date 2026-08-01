
def cases_64bit(sp_api):
    """Yield all tests for all formats

    This is more than testing get_index_dtype. It allows checking whether upcasting
    or downcasting the index dtypes affects test results. The approach used here
    does not try to figure out which tests might fail due to 32/64-bit issues.
    We just run them all.
    So, each test method in that uses cases_64bit reruns most of the test suite!
    """
    if sp_api == "sparray":
        TEST_CLASSES = [_TestBSR, _TestCOO, _TestCSC, _TestCSR, _TestDIA]
    elif sp_api == "sparray-extra":
        # lil/dok->other conversion operations use get_index_dtype
        # so we include lil & dok test suite even though they do not
        # use get_index_dtype within the class. That means many of
        # these tests are superfluous, but it's hard to pick which
        TEST_CLASSES = [_TestDOK, _TestLIL]
    elif sp_api == "spmatrix":
        TEST_CLASSES = [_TestBSRMatrix, _TestCOOMatrix, _TestCSCMatrix,
                        _TestCSRMatrix, _TestDIAMatrix]
    elif sp_api == "spmatrix-extra":
        # lil/dok->other conversion operations use get_index_dtype
        TEST_CLASSES = [_TestDOKMatrix, _TestLILMatrix]
    else:
        raise ValueError(f"parameter {sp_api=} is not valid")

    for cls in TEST_CLASSES:
        for method_name in sorted(dir(cls)):
            method = getattr(cls, method_name)
            if (method_name.startswith('test_') and
                    not getattr(method, 'slow', False)):
                marks = []

                msg = SKIP_TESTS.get(method_name)
                if msg:
                    marks.append(pytest.mark.skip(reason=msg))

                markers = getattr(method, 'pytestmark', [])
                for mark in markers:
                    if mark.name in ('skipif', 'skip', 'xfail', 'xslow'):
                        marks.append(mark)

                yield pytest.param(cls, method_name, marks=marks)

