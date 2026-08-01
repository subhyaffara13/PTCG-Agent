
def latex2png(latex, filename, fontset='cm', fontsize=10, dpi=100):
    with mpl.rc_context({'mathtext.fontset': fontset, 'font.size': fontsize}):
        try:
            depth = mathtext.math_to_image(
                f"${latex}$", filename, dpi=dpi, format="png")
        except Exception:
            _api.warn_external(f"Could not render math expression {latex}")
            depth = 0
    return depth

