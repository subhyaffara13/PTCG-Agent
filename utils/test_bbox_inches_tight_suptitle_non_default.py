
def test_bbox_inches_tight_suptitle_non_default():
    fig, ax = plt.subplots()
    fig.suptitle('Booo', x=0.5, y=1.1)

