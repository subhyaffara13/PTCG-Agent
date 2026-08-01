
def test_fancyarrow_units():
    from datetime import datetime
    # Smoke test to check that FancyArrowPatch works with units
    dtime = datetime(2000, 1, 1)
    fig, ax = plt.subplots()
    arrow = FancyArrowPatch((0, dtime), (0.01, dtime))

