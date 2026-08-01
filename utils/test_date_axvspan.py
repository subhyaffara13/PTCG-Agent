
def test_date_axvspan():
    # test axvspan with date inputs
    t0 = datetime.datetime(2000, 1, 20)
    tf = datetime.datetime(2010, 1, 21)
    fig, ax = plt.subplots()
    ax.axvspan(t0, tf, facecolor="blue", alpha=0.25)
    ax.set_xlim(t0 - datetime.timedelta(days=720),
                tf + datetime.timedelta(days=720))
    fig.autofmt_xdate()

