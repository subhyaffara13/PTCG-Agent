
def test_bbox_inches_tight_layout_notconstrained(tmp_path):
    # pad_inches='layout' should be ignored when not using constrained/
    # compressed layout.  Smoke test that savefig doesn't error in this case.
    fig, ax = plt.subplots()
    fig.savefig(tmp_path / 'foo.png', bbox_inches='tight', pad_inches='layout')

