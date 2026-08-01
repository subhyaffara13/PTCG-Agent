
def test_boxplot_mod_artist_after_plotting():
    x = [0.15, 0.11, 0.06, 0.06, 0.12, 0.56, -0.56]
    fig, ax = plt.subplots()
    bp = ax.boxplot(x, sym="o")
    for key in bp:
        for obj in bp[key]:
            obj.set_color('green')

