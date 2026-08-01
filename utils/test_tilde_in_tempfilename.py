
def test_tilde_in_tempfilename(tmp_path):
    # Tilde ~ in the tempdir path (e.g. TMPDIR, TMP or TEMP on windows
    # when the username is very long and windows uses a short name) breaks
    # latex before https://github.com/matplotlib/matplotlib/pull/5928
    base_tempdir = tmp_path / "short-1"
    base_tempdir.mkdir()
    # Change the path for new tempdirs, which is used internally by the ps
    # backend to write a file.
    with cbook._setattr_cm(tempfile, tempdir=str(base_tempdir)):
        # usetex results in the latex call, which does not like the ~
        mpl.rcParams['text.usetex'] = True
        plt.plot([1, 2, 3, 4])
        plt.xlabel(r'\textbf{time} (s)')
        # use the PS backend to write the file...
        plt.savefig(base_tempdir / 'tex_demo.eps', format="ps")

