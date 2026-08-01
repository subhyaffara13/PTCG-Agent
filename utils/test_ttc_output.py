
def test_ttc_output():
    fp = FontProperties(family=['WenQuanYi Zen Hei'])
    if Path(findfont(fp)).name != 'wqy-zenhei.ttc':
        pytest.skip('Font wqy-zenhei.ttc may be missing')

    fonts = {'sans-serif': 'WenQuanYi Zen Hei', 'monospace': 'WenQuanYi Zen Hei Mono'}
    plt.rc('font', size=16, **fonts)

    figs = plt.figure(figsize=(7, len(fonts) / 2)).subfigures(len(fonts))
    for font, fig in zip(fonts.values(), figs):
        fig.text(0.5, 0.5, f'{font}: {string.ascii_uppercase}', font=font,
                 horizontalalignment='center', verticalalignment='center')

