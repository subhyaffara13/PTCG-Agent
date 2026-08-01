
def test_pie_center_radius():
    # The slices will be ordered and plotted counter-clockwise.
    labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
    sizes = [15, 30, 45, 10]
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90,
            wedgeprops={'linewidth': 0}, center=(1, 2), radius=1.5)

    plt.annotate("Center point", xy=(1, 2), xytext=(1, 1.3),
                 arrowprops=dict(arrowstyle="->",
                                 connectionstyle="arc3"),
                 bbox=dict(boxstyle="square", facecolor="lightgrey"))
    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')

