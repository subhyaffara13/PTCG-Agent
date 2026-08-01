
def test_shared_with_aspect_1():
    # allow sharing one axis
    for adjustable in ['box', 'datalim']:
        fig, axs = plt.subplots(nrows=2, sharex=True)
        axs[0].set_aspect(2, adjustable=adjustable, share=True)
        assert axs[1].get_aspect() == 2
        assert axs[1].get_adjustable() == adjustable

        fig, axs = plt.subplots(nrows=2, sharex=True)
        axs[0].set_aspect(2, adjustable=adjustable)
        assert axs[1].get_aspect() == 'auto'

