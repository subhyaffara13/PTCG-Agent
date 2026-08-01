
def _test_axeswidget_interactive():
    ax = plt.figure().add_subplot()
    pickle.dumps(mpl.widgets.Button(ax, "button"))

