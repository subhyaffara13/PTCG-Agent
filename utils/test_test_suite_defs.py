
def test_test_suite_defs():
    candidates_ok = [
        "    def foo():\n",
        "def foo(arg):\n",
        "def _foo():\n",
        "def test_foo():\n",
    ]
    candidates_fail = [
        "def foo():\n",
        "def foo() :\n",
        "def foo( ):\n",
        "def  foo():\n",
    ]
    for c in candidates_ok:
        assert test_suite_def_re.search(c) is None, c
    for c in candidates_fail:
        assert test_suite_def_re.search(c) is not None, c

