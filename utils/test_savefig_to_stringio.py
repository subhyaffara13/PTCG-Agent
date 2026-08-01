
def test_savefig_to_stringio(format, use_log, rcParams, orientation, papersize):
    mpl.rcParams.update(rcParams)
    if mpl.rcParams["ps.usedistiller"] == "ghostscript":
        try:
            mpl._get_executable_info("gs")
        except mpl.ExecutableNotFoundError as exc:
            pytest.skip(str(exc))
    elif mpl.rcParams["ps.usedistiller"] == "xpdf":
        try:
            mpl._get_executable_info("gs")  # Effectively checks for ps2pdf.
            mpl._get_executable_info("pdftops")
        except mpl.ExecutableNotFoundError as exc:
            pytest.skip(str(exc))

    fig, ax = plt.subplots()

    with io.StringIO() as s_buf, io.BytesIO() as b_buf:

        if use_log:
            ax.set_yscale('log')

        ax.plot([1, 2], [1, 2])
        title = "Déjà vu"
        if not mpl.rcParams["text.usetex"]:
            title += " \N{MINUS SIGN}\N{EURO SIGN}"
        ax.set_title(title)
        allowable_exceptions = []
        if mpl.rcParams["text.usetex"]:
            allowable_exceptions.append(RuntimeError)
        if mpl.rcParams["ps.useafm"]:
            allowable_exceptions.append(mpl.MatplotlibDeprecationWarning)
        try:
            fig.savefig(s_buf, format=format, orientation=orientation,
                        papertype=papersize)
            fig.savefig(b_buf, format=format, orientation=orientation,
                        papertype=papersize)
        except tuple(allowable_exceptions) as exc:
            pytest.skip(str(exc))

        assert not s_buf.closed
        assert not b_buf.closed
        s_val = s_buf.getvalue().encode('ascii')
        b_val = b_buf.getvalue()

        if format == 'ps':
            # Default figsize = (8, 6) inches = (576, 432) points = (203.2, 152.4) mm.
            # Landscape orientation will swap dimensions.
            if mpl.rcParams["ps.usedistiller"] == "xpdf":
                # Some versions specifically show letter/203x152, but not all,
                # so we can only use this simpler test.
                if papersize == 'figure':
                    assert b'letter' not in s_val.lower()
                else:
                    assert b'letter' in s_val.lower()
            elif mpl.rcParams["ps.usedistiller"] or mpl.rcParams["text.usetex"]:
                width = b'432.0' if orientation == 'landscape' else b'576.0'
                wanted = (b'-dDEVICEWIDTHPOINTS=' + width if papersize == 'figure'
                          else b'-sPAPERSIZE')
                assert wanted in s_val
            else:
                if papersize == 'figure':
                    assert b'%%DocumentPaperSizes' not in s_val
                else:
                    assert b'%%DocumentPaperSizes' in s_val

        # Strip out CreationDate: ghostscript and cairo don't obey
        # SOURCE_DATE_EPOCH, and that environment variable is already tested in
        # test_determinism.
        s_val = re.sub(b"(?<=\n%%CreationDate: ).*", b"", s_val)
        b_val = re.sub(b"(?<=\n%%CreationDate: ).*", b"", b_val)

        assert s_val == b_val.replace(b'\r\n', b'\n')

