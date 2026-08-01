
def test_font_wrap():
    fig = plt.figure(figsize=(8, 6))
    plt.axis([0, 10, 0, 10])
    t = "This is a really long string that I'd rather have wrapped so that" \
        " it doesn't go outside of the figure, but if it's long enough it" \
        " will go off the top or bottom!"
    plt.text(4, -1, t, fontsize=18, family='serif', ha='left', rotation=15,
             wrap=True)
    plt.text(6, 5, t, family='sans serif', ha='left', rotation=15, wrap=True)
    plt.text(5, 10, t, weight='heavy', ha='center', va='top', wrap=True)
    plt.text(3, 4, t, family='monospace', ha='right', wrap=True)
    plt.text(-1, 0, t, fontsize=14, style='italic', ha='left', rotation=-15,
             wrap=True)

