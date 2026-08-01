
def test_appending_issue_gh_8625():
    stream = BytesIO()

    with make_simple(stream, mode='w') as f:
        f.createDimension('x', 2)
        f.createVariable('x', float, ('x',))
        f.variables['x'][...] = 1
        f.flush()
        contents = stream.getvalue()

    stream = BytesIO(contents)
    with netcdf_file(stream, mode='a') as f:
        f.variables['x'][...] = 2

