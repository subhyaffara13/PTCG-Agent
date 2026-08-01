
def _get_preamble():
    """Prepare a LaTeX preamble based on the rcParams configuration."""
    def _to_fontspec():
        for command, family in [("setmainfont", "serif"),
                                ("setsansfont", "sans\\-serif"),
                                ("setmonofont", "monospace")]:
            font_path = fm.findfont(family)
            path = pathlib.Path(font_path)
            yield r"  \%s{%s}[Path=\detokenize{%s/}%s]" % (
                command, path.name, path.parent.as_posix(),
                f',FontIndex={font_path.face_index:d}' if path.suffix == '.ttc' else '')

    font_size_pt = FontProperties(size=mpl.rcParams["font.size"]).get_size_in_points()
    return "\n".join([
        # Remove Matplotlib's custom command \mathdefault.  (Not using
        # \mathnormal instead since this looks odd with Computer Modern.)
        r"\def\mathdefault#1{#1}",
        # Use displaystyle for all math.
        r"\everymath=\expandafter{\the\everymath\displaystyle}",
        # Set up font sizes to match font.size setting.
        # If present, use the KOMA package scrextend to adjust the standard
        # LaTeX font commands (\tiny, ..., \normalsize, ..., \Huge) accordingly.
        # Otherwise, only set \normalsize, manually.
        r"\IfFileExists{scrextend.sty}{",
        r"  \usepackage[fontsize=%fpt]{scrextend}" % font_size_pt,
        r"}{",
        r"  \renewcommand{\normalsize}{\fontsize{%f}{%f}\selectfont}"
        % (font_size_pt, 1.2 * font_size_pt),
        r"  \normalsize",
        r"}",
        # Allow pgf.preamble to override the above definitions.
        mpl.rcParams["pgf.preamble"],
        *([
            r"\ifdefined\pdftexversion\else  % non-pdftex case.",
            r"  \usepackage{fontspec}",
            *_to_fontspec(),
            r"\fi"] if mpl.rcParams["pgf.rcfonts"] else []),
        # Documented as "must come last".
        mpl.texmanager._usepackage_if_not_loaded("underscore", option="strings"),
    ])

