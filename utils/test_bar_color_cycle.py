
def test_bar_color_cycle():
    to_rgb = mcolors.to_rgb
    fig, ax = plt.subplots()
    for j in range(5):
        ln, = ax.plot(range(3))
        brs = ax.bar(range(3), range(3))
        for br in brs:
            assert to_rgb(ln.get_color()) == to_rgb(br.get_facecolor())

