
def test_empty_line():
    # Smoke-test for gh#23954
    figure = Figure()
    figure.text(0.5, 0.5, "\nfoo\n\n")
    buf = io.BytesIO()
    figure.savefig(buf, format='eps')
    figure.savefig(buf, format='ps')

