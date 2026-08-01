
def test_latex_pie_percent(fig_test, fig_ref):

    data = [20, 10, 70]

    ax = fig_test.subplots()
    ax.pie(data, autopct="%1.0f%%", textprops={'usetex': True})

    ax1 = fig_ref.subplots()
    ax1.pie(data, autopct=r"%1.0f\%%", textprops={'usetex': True})

