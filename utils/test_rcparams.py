
def test_rcparams(fig_test, fig_ref):
    fig_ref.supxlabel("xlabel", weight='bold', size=15)
    fig_ref.supylabel("ylabel", weight='bold', size=15)
    fig_ref.suptitle("Title", weight='light', size=20)
    with mpl.rc_context({'figure.labelweight': 'bold',
                         'figure.labelsize': 15,
                         'figure.titleweight': 'light',
                         'figure.titlesize': 20}):
        fig_test.supxlabel("xlabel")
        fig_test.supylabel("ylabel")
        fig_test.suptitle("Title")


def test_rcparams(tmp_path):
    mpl.rc('text', usetex=False)
    mpl.rc('lines', linewidth=22)

    usetex = mpl.rcParams['text.usetex']
    linewidth = mpl.rcParams['lines.linewidth']

    rcpath = tmp_path / 'test_rcparams.rc'
    rcpath.write_text('lines.linewidth: 33', encoding='utf-8')

    # test context given dictionary
    with mpl.rc_context(rc={'text.usetex': not usetex}):
        assert mpl.rcParams['text.usetex'] == (not usetex)
    assert mpl.rcParams['text.usetex'] == usetex

    # test context given filename (mpl.rc sets linewidth to 33)
    with mpl.rc_context(fname=rcpath):
        assert mpl.rcParams['lines.linewidth'] == 33
    assert mpl.rcParams['lines.linewidth'] == linewidth

    # test context given filename and dictionary
    with mpl.rc_context(fname=rcpath, rc={'lines.linewidth': 44}):
        assert mpl.rcParams['lines.linewidth'] == 44
    assert mpl.rcParams['lines.linewidth'] == linewidth

    # test context as decorator (and test reusability, by calling func twice)
    @mpl.rc_context({'lines.linewidth': 44})
    def func():
        assert mpl.rcParams['lines.linewidth'] == 44

    func()
    func()

    # test rc_file
    mpl.rc_file(rcpath)
    assert mpl.rcParams['lines.linewidth'] == 33

