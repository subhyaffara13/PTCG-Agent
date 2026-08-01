
def test_pie_linewidth_0():
    # The slices will be ordered and plotted counter-clockwise.
    labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
    sizes = [15, 30, 45, 10]
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90,
            wedgeprops={'linewidth': 0})
    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')

    # Reuse testcase from above for a labeled data test
    data = {"l": labels, "s": sizes, "c": colors, "ex": explode}
    fig = plt.figure()
    ax = fig.gca()
    ax.pie("s", explode="ex", labels="l", colors="c",
           autopct='%1.1f%%', shadow=True, startangle=90,
           wedgeprops={'linewidth': 0}, data=data)
    ax.axis('equal')

    # And again to test the pyplot functions which should also be able to be
    # called with a data kwarg
    plt.figure()
    plt.pie("s", explode="ex", labels="l", colors="c",
            autopct='%1.1f%%', shadow=True, startangle=90,
            wedgeprops={'linewidth': 0}, data=data)
    plt.axis('equal')

