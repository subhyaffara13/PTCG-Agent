
def test_rcupdate():
    rc_sets = [{'font.family': 'sans-serif',
                'font.size': 30,
                'figure.subplot.left': .2,
                'lines.markersize': 10,
                'pgf.rcfonts': False,
                'pgf.texsystem': 'xelatex'},
               {'font.family': 'monospace',
                'font.size': 10,
                'figure.subplot.left': .1,
                'lines.markersize': 20,
                'pgf.rcfonts': False,
                'pgf.texsystem': 'pdflatex',
                'pgf.preamble': ('\\usepackage[utf8x]{inputenc}'
                                 '\\usepackage[T1]{fontenc}'
                                 '\\usepackage{sfmath}')}]
    tol = [0, 13.2] if _old_gs_version else [0, 0]
    for i, rc_set in enumerate(rc_sets):
        with mpl.rc_context(rc_set):
            for substring, pkg in [('sfmath', 'sfmath'), ('utf8x', 'ucs')]:
                if (substring in mpl.rcParams['pgf.preamble']
                        and not _has_tex_package(pkg)):
                    pytest.skip(f'needs {pkg}.sty')
            create_figure()
            compare_figure(f'pgf_rcupdate{i + 1}.pdf', tol=tol[i])

