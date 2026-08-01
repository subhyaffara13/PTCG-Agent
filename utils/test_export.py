
def test_export(mi_styler_comp, mi_styler):
    exp_attrs = [
        "_todo",
        "hide_index_",
        "hide_index_names",
        "hide_columns_",
        "hide_column_names",
        "table_attributes",
        "table_styles",
        "css",
    ]
    for attr in exp_attrs:
        check = getattr(mi_styler, attr) == getattr(mi_styler_comp, attr)
        assert not (
            all(check) if (hasattr(check, "__iter__") and len(check) > 0) else check
        )

    export = mi_styler_comp.export()
    used = mi_styler.use(export)
    for attr in exp_attrs:
        check = getattr(used, attr) == getattr(mi_styler_comp, attr)
        assert all(check) if (hasattr(check, "__iter__") and len(check) > 0) else check

    used.to_html()

