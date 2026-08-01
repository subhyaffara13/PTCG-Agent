
def test_shared_axis_categorical():
    # str uses category.StrCategoryConverter
    d1 = {"a": 1, "b": 2}
    d2 = {"a": 3, "b": 4}
    fig, (ax1, ax2) = plt.subplots(1, 2, sharex=True, sharey=True)
    ax1.plot(d1.keys(), d1.values())
    ax2.plot(d2.keys(), d2.values())
    ax1.xaxis.set_units(UnitData(["c", "d"]))
    assert "c" in ax2.xaxis.get_units()._mapping.keys()

