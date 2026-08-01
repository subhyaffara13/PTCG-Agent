
def test_mathtext_fallback(fallback, fontlist):
    mpl.font_manager.fontManager.addfont(
        (Path(__file__).resolve().parent / 'data/mpltest.ttf'))
    mpl.rcParams["svg.fonttype"] = 'none'
    mpl.rcParams['mathtext.fontset'] = 'custom'
    mpl.rcParams['mathtext.rm'] = 'mpltest'
    mpl.rcParams['mathtext.it'] = 'mpltest:italic'
    mpl.rcParams['mathtext.bf'] = 'mpltest:bold'
    mpl.rcParams['mathtext.bfit'] = 'mpltest:italic:bold'
    mpl.rcParams['mathtext.fallback'] = fallback

    test_str = r'a$A\AA\breve\gimel$'

    buff = io.BytesIO()
    fig, ax = plt.subplots()
    fig.text(.5, .5, test_str, fontsize=40, ha='center')
    fig.savefig(buff, format="svg")
    tspans = (ET.fromstring(buff.getvalue())
              .findall(".//{http://www.w3.org/2000/svg}tspan[@style]"))
    char_fonts = [
        re.search(r"font-family: '([\w ]+)'", tspan.attrib["style"]).group(1)
        for tspan in tspans]
    assert char_fonts == fontlist, f'Expected {fontlist}, got {char_fonts}'
    mpl.font_manager.fontManager.ttflist.pop()

