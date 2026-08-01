
def test_errorbar_mapview_kwarg():
    D = {ii: ii for ii in range(10)}
    fig, ax = plt.subplots()
    ax.errorbar(x=D.keys(), y=D.values(), xerr=D.values())

