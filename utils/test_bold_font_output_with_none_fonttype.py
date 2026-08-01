
def test_bold_font_output_with_none_fonttype():
    plt.rcParams['svg.fonttype'] = 'none'
    fig, ax = plt.subplots()
    ax.plot(np.arange(10), np.arange(10))
    ax.set_xlabel('nonbold-xlabel')
    ax.set_ylabel('bold-ylabel', fontweight='bold')
    # set weight as integer to assert it's handled properly
    ax.set_title('bold-title', fontweight=600)

