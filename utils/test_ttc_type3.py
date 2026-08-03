from pathlib import Path


def test_ttc_type3():
    fp = fm.FontProperties(family=['WenQuanYi Zen Hei'])
    if Path(fm.findfont(fp)).name != 'wqy-zenhei.ttc':
        pytest.skip('Font wqy-zenhei.ttc may be missing')

    fonts = ['WenQuanYi Zen Hei', 'WenQuanYi Zen Hei Mono']
    plt.rc('font', size=16)
    plt.rc('pdf', fonttype=3)

    figs = plt.figure(figsize=(7, len(fonts) / 2)).subfigures(len(fonts))
    for font, fig in zip(fonts, figs):
        fig.text(0.5, 0.5, f'{font}: {string.ascii_uppercase}', font=font,
                 horizontalalignment='center', verticalalignment='center')


def test_ttc_type3():
    fp = font_manager.FontProperties(family=['WenQuanYi Zen Hei'])
    if Path(font_manager.findfont(fp)).name != 'wqy-zenhei.ttc':
        pytest.skip('Font wqy-zenhei.ttc may be missing')

    fonts = ['WenQuanYi Zen Hei', 'WenQuanYi Zen Hei Mono']
    plt.rc('font', size=16)
    plt.rc('pdf', fonttype=3)

    figs = plt.figure(figsize=(7, len(fonts) / 2)).subfigures(len(fonts))
    for font, fig in zip(fonts, figs):
        fig.text(0.5, 0.5, f'{font}: {string.ascii_uppercase}', font=font,
                 horizontalalignment='center', verticalalignment='center')

