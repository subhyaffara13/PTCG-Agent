
def test_radio_grid_buttons():
    fig = plt.figure()
    rb_horizontal = widgets.RadioButtons(
        fig.add_axes((0.1, 0.05, 0.65, 0.05)),
        ["tea", "coffee", "chocolate milk", "water", "soda", "coke"],
        layout='horizontal',
        active=4,
    )
    cb_grid = widgets.CheckButtons(
        fig.add_axes((0.1, 0.15, 0.25, 0.05*3)),
        ["Chicken", "Salad", "Rice", "Sushi", "Pizza", "Fries"],
        layout=(3, 2),
        actives=[True, True, False, False, False, True],
    )
    rb_vertical = widgets.RadioButtons(
        fig.add_axes((0.1, 0.35, 0.2, 0.05*4)),
        ["Trinity Cream", "Cake", "Ice Cream", "Muhallebi"],
        layout='vertical',
        active=3,
    )

