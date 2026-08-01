
def test_issue_5399():
    args = [x, y, S(2), S.Half]

    def ok(a):
        """Return True if the input args for diff are ok"""
        if not a:
            return False
        if a[0].is_Symbol is False:
            return False
        s_at = [i for i in range(len(a)) if a[i].is_Symbol]
        n_at = [i for i in range(len(a)) if not a[i].is_Symbol]
        # every symbol is followed by symbol or int
        # every number is followed by a symbol
        return (all(a[i + 1].is_Symbol or a[i + 1].is_Integer
            for i in s_at if i + 1 < len(a)) and
            all(a[i + 1].is_Symbol
            for i in n_at if i + 1 < len(a)))
    eq = x**10*y**8
    for a in subsets(args):
        for v in variations(a, len(a)):
            if ok(v):
                eq.diff(*v) # does not raise
            else:
                raises(ValueError, lambda: eq.diff(*v))

