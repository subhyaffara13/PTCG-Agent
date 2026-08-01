
def test_pie_shadow():
    # Also acts as a test for the shade argument of Shadow
    sizes = [15, 30, 45, 10]
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice
    _, axes = plt.subplots(2, 2)
    axes[0][0].pie(sizes, explode=explode, colors=colors,
                   shadow=True, startangle=90,
                   wedgeprops={'linewidth': 0})

    axes[0][1].pie(sizes, explode=explode, colors=colors,
                   shadow=False, startangle=90,
                   wedgeprops={'linewidth': 0})

    axes[1][0].pie(sizes, explode=explode, colors=colors,
                   shadow={'ox': -0.05, 'oy': -0.05, 'shade': 0.9, 'edgecolor': 'none'},
                   startangle=90, wedgeprops={'linewidth': 0})

    axes[1][1].pie(sizes, explode=explode, colors=colors,
                   shadow={'ox': 0.05, 'linewidth': 2, 'shade': 0.2},
                   startangle=90, wedgeprops={'linewidth': 0})

