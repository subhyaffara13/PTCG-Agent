
def test_explicit_converter():
    d1 = {"a": 1, "b": 2}
    str_cat_converter = StrCategoryConverter()
    str_cat_converter_2 = StrCategoryConverter()
    date_converter = DateConverter()

    # Explicit is set
    fig1, ax1 = plt.subplots()
    ax1.xaxis.set_converter(str_cat_converter)
    assert ax1.xaxis.get_converter() == str_cat_converter
    # Explicit not overridden by implicit
    ax1.plot(d1.keys(), d1.values())
    assert ax1.xaxis.get_converter() == str_cat_converter
    # No error when called twice with equivalent input
    ax1.xaxis.set_converter(str_cat_converter)
    # Error when explicit called twice
    with pytest.raises(RuntimeError):
        ax1.xaxis.set_converter(str_cat_converter_2)

    fig2, ax2 = plt.subplots()
    ax2.plot(d1.keys(), d1.values())

    # No error when equivalent type is used
    ax2.xaxis.set_converter(str_cat_converter)

    fig3, ax3 = plt.subplots()
    ax3.plot(d1.keys(), d1.values())

    # Warn when implicit overridden
    with pytest.warns():
        ax3.xaxis.set_converter(date_converter)

