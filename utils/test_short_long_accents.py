
def test_short_long_accents(fig_test, fig_ref):
    acc_map = _mathtext.Parser._accent_map
    short_accs = [s for s in acc_map if len(s) == 1]
    corresponding_long_accs = []
    for s in short_accs:
        l, = (l for l in acc_map if len(l) > 1 and acc_map[l] == acc_map[s])
        corresponding_long_accs.append(l)
    fig_test.text(0, .5, "$" + "".join(rf"\{s}a" for s in short_accs) + "$")
    fig_ref.text(
        0, .5, "$" + "".join(fr"\{l} a" for l in corresponding_long_accs) + "$")

