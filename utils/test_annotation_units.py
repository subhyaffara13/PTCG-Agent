
def test_annotation_units(fig_test, fig_ref):
    ax = fig_test.add_subplot()
    ax.plot(datetime.now(), 1, "o")  # Implicitly set axes extents.
    ax.annotate("x", (datetime.now(), 0.5), xycoords=("data", "axes fraction"),
                # This used to crash before.
                xytext=(0, 0), textcoords="offset points")
    ax = fig_ref.add_subplot()
    ax.plot(datetime.now(), 1, "o")
    ax.annotate("x", (datetime.now(), 0.5), xycoords=("data", "axes fraction"))

