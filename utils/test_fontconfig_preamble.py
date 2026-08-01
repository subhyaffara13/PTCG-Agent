
def test_fontconfig_preamble():
    """Test that the preamble is included in the source."""
    plt.rcParams['text.usetex'] = True

    src1 = TexManager()._get_tex_source("", fontsize=12)
    plt.rcParams['text.latex.preamble'] = '\\usepackage{txfonts}'
    src2 = TexManager()._get_tex_source("", fontsize=12)

    assert src1 != src2

