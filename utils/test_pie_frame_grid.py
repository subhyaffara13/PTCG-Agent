
def test_pie_frame_grid():
    # The slices will be ordered and plotted counter-clockwise.
    labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
    sizes = [15, 30, 45, 10]
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    # only "explode" the 2nd slice (i.e. 'Hogs')
    explode = (0, 0.1, 0, 0)

    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90,
            wedgeprops={'linewidth': 0},
            frame=True, center=(2, 2))

    plt.pie(sizes[::-1], explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90,
            wedgeprops={'linewidth': 0},
            frame=True, center=(5, 2))

    plt.pie(sizes, explode=explode[::-1], labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90,
            wedgeprops={'linewidth': 0},
            frame=True, center=(3, 5))
    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')

