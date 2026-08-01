
def test_patheffects_spaces_and_newlines():
    ax = plt.subplot()
    s1 = "         "
    s2 = "\nNewline also causes problems"
    text1 = ax.text(0.5, 0.75, s1, ha='center', va='center', size=20,
                    bbox={'color': 'salmon'})
    text2 = ax.text(0.5, 0.25, s2, ha='center', va='center', size=20,
                    bbox={'color': 'thistle'})
    text1.set_path_effects([path_effects.Normal()])
    text2.set_path_effects([path_effects.Normal()])

