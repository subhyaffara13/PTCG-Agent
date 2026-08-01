
def test_twin_axes_empty_and_removed():
    # Purely cosmetic font changes (avoid overlap)
    mpl.rcParams.update({"font.size": 8, "xtick.labelsize": 8, "ytick.labelsize": 8})
    generators = ["twinx", "twiny", "twin"]
    modifiers = ["", "host invisible", "twin removed", "twin invisible",
                 "twin removed\nhost invisible"]
    plt.figure(figsize=(8, 6))
    # Unmodified host subplot at the beginning for reference
    h = host_subplot(len(modifiers)+1, len(generators), 2)
    h.text(0.5, 0.5, "host_subplot",
           horizontalalignment="center", verticalalignment="center")
    # Host subplots with various modifications (twin*, visibility) applied
    for i, (mod, gen) in enumerate(product(modifiers, generators),
                                   len(generators) + 1):
        h = host_subplot(len(modifiers)+1, len(generators), i)
        t = getattr(h, gen)()
        if "twin invisible" in mod:
            t.axis[:].set_visible(False)
        if "twin removed" in mod:
            t.remove()
        if "host invisible" in mod:
            h.axis[:].set_visible(False)
        h.text(0.5, 0.5, gen + ("\n" + mod if mod else ""),
               horizontalalignment="center", verticalalignment="center")
    plt.subplots_adjust(wspace=0.5, hspace=1)

