
def _get_latex_main(expr, *, preamble=None, packages=(), extra_preamble=None,
                    euler=True, fontsize=None, **latex_settings):
    """
    Generate string of a LaTeX document rendering ``expr``.
    """
    if preamble is None:
        actual_packages = packages + ("amsmath", "amsfonts")
        if euler:
            actual_packages += ("euler",)
        package_includes = "\n" + "\n".join(["\\usepackage{%s}" % p
                                             for p in actual_packages])
        if extra_preamble:
            package_includes += extra_preamble

        if not fontsize:
            fontsize = "12pt"
        elif isinstance(fontsize, int):
            fontsize = "{}pt".format(fontsize)
        preamble = r"""\documentclass[varwidth,%s]{standalone}
%s

\begin{document}
""" % (fontsize, package_includes)
    else:
        if packages or extra_preamble:
            raise ValueError("The \"packages\" or \"extra_preamble\" keywords"
                             "must not be set if a "
                             "custom LaTeX preamble was specified")

    if isinstance(expr, str):
        latex_string = expr
    else:
        latex_string = ('$\\displaystyle ' +
                        latex(expr, mode='plain', **latex_settings) +
                        '$')

    return preamble + '\n' + latex_string + '\n\n' + r"\end{document}"

