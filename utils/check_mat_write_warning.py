
def check_mat_write_warning(names_vars):
    class C:
        def items(self):
            return names_vars

    stream = BytesIO()
    with pytest.warns(MatWriteWarning, match='Starting field name with'):
        savemat(stream, C())

