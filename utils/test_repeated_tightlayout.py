
def test_repeated_tightlayout():
    fig = Figure()
    fig.tight_layout()
    # subsequent calls should not warn
    fig.tight_layout()
    fig.tight_layout()

