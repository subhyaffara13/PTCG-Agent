
def test_loc_validation_string_value():
    fig, ax = plt.subplots()
    labels = ["mock data"]
    ax.legend(loc='best', labels=labels)
    ax.legend(loc='upper right', labels=labels)
    ax.legend(loc='best', labels=labels)
    ax.legend(loc='upper right', labels=labels)
    ax.legend(loc='upper left', labels=labels)
    ax.legend(loc='lower left', labels=labels)
    ax.legend(loc='lower right', labels=labels)
    ax.legend(loc='right', labels=labels)
    ax.legend(loc='center left', labels=labels)
    ax.legend(loc='center right', labels=labels)
    ax.legend(loc='lower center', labels=labels)
    ax.legend(loc='upper center', labels=labels)
    with pytest.raises(ValueError, match="'wrong' is not a valid value for"):
        ax.legend(loc='wrong', labels=labels)

