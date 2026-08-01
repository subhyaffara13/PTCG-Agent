
def test_minus_signs_with_tex(fig_test, fig_ref, texsystem):
    if not _check_for_pgf(texsystem):
        pytest.skip(texsystem + ' + pgf is required')
    mpl.rcParams["pgf.texsystem"] = texsystem
    fig_test.text(.5, .5, "$-1$")
    fig_ref.text(.5, .5, "$\N{MINUS SIGN}1$")

