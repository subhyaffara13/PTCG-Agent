import copy

def test_copy(d, Asp):
    assert d.items() == Asp.items()
    dd = d.copy()
    asp = Asp.copy()
    assert dd.items() == asp.items()
    assert asp.items() == Asp.items()
    asp[(0, 1)] = 3
    assert Asp[(0, 1)] == 1


def test_copy():
    with pytest.raises(TypeError, match="Expression objects are not copiable"):
        copy.copy(pd.col("a"))


def test_copy():
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [0.1, 0.2, 0.3]})
    df_copy = df.copy()

    # the deep copy by defaults takes a shallow copy of the Index
    assert df_copy.index is not df.index
    assert df_copy.columns is not df.columns
    assert df_copy.index.is_(df.index)
    assert df_copy.columns.is_(df.columns)

    # the deep copy doesn't share memory
    assert not np.shares_memory(get_array(df_copy, "a"), get_array(df, "a"))
    assert not df_copy._mgr.blocks[0].refs.has_reference()
    assert not df_copy._mgr.blocks[1].refs.has_reference()

    assert df_copy.index is not df.index
    assert df_copy.columns is not df.columns

    # mutating copy doesn't mutate original
    df_copy.iloc[0, 0] = 0
    assert df.iloc[0, 0] == 1


def test_copy(propindexes, temp_file):
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD")),
        index=Index([f"i-{i}" for i in range(30)]),
    )

    with HDFStore(temp_file) as st:
        st.append("df", df, data_columns=["A"])
    with tempfile.NamedTemporaryFile() as new_f:
        with HDFStore(temp_file) as store:
            with contextlib.closing(
                store.copy(new_f.name, keys=None, propindexes=propindexes)
            ) as tstore:
                # check keys
                keys = store.keys()
                assert set(keys) == set(tstore.keys())
                # check indices & nrows
                for k in tstore.keys():
                    if tstore.get_storer(k).is_table:
                        new_t = tstore.get_storer(k)
                        orig_t = store.get_storer(k)

                        assert orig_t.nrows == new_t.nrows

                        # check propindixes
                        if propindexes:
                            for a in orig_t.axes:
                                if a.is_indexed:
                                    assert new_t[a.name].is_indexed


def test_copy(comprehensive, render, deepcopy, mi_styler, mi_styler_comp):
    styler = mi_styler_comp if comprehensive else mi_styler
    styler.uuid_len = 5

    s2 = copy.deepcopy(styler) if deepcopy else copy.copy(styler)  # make copy and check
    assert s2 is not styler

    if render:
        styler.to_html()

    excl = [
        "cellstyle_map",  # render time vars..
        "cellstyle_map_columns",
        "cellstyle_map_index",
        "template_latex",  # render templates are class level
        "template_html",
        "template_html_style",
        "template_html_table",
    ]
    if not deepcopy:  # check memory locations are equal for all included attributes
        for attr in [a for a in styler.__dict__ if (not callable(a) and a not in excl)]:
            assert id(getattr(s2, attr)) == id(getattr(styler, attr))
    else:  # check memory locations are different for nested or mutable vars
        shallow = [
            "data",
            "columns",
            "index",
            "uuid_len",
            "uuid",
            "caption",
            "cell_ids",
            "hide_index_",
            "hide_columns_",
            "hide_index_names",
            "hide_column_names",
            "table_attributes",
        ]
        for attr in shallow:
            assert id(getattr(s2, attr)) == id(getattr(styler, attr))

        for attr in [
            a
            for a in styler.__dict__
            if (not callable(a) and a not in excl and a not in shallow)
        ]:
            if getattr(s2, attr) is None:
                assert id(getattr(s2, attr)) == id(getattr(styler, attr))
            else:
                assert id(getattr(s2, attr)) != id(getattr(styler, attr))


def test_copy(idx):
    i_copy = idx.copy()

    assert_multiindex_copied(i_copy, idx)


def test_copy(Poly):
    p1 = Poly.basis(5)
    p2 = p1.copy()
    assert_(p1 == p2)
    assert_(p1 is not p2)
    assert_(p1.coef is not p2.coef)
    assert_(p1.domain is not p2.domain)
    assert_(p1.window is not p2.window)


def test_copy():
    tp = TextPath((0, 0), ".")
    assert copy.deepcopy(tp).vertices is not tp.vertices
    assert (copy.deepcopy(tp).vertices == tp.vertices).all()
    assert copy.copy(tp).vertices is tp.vertices

