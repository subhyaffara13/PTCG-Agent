from pathlib import Path


def test_otf_font_smoke(family_name, file_name):
    # checks that there's no segfault
    fp = fm.FontProperties(family=[family_name])
    if Path(fm.findfont(fp)).name != file_name:
        pytest.skip(f"Font {family_name} may be missing")

    plt.rc('font', family=[family_name], size=27)

    fig = plt.figure()
    fig.text(0.15, 0.475, "Привет мир!")
    fig.savefig(io.BytesIO(), format="pdf")

