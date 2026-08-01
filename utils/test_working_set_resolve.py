
def test_working_set_resolve(
    installed_dists,
    installable_dists,
    requirements,
    replace_conflicting,
    resolved_dists_or_exception,
):
    ws = pkg_resources.WorkingSet([])
    list(map(ws.add, installed_dists))
    resolve_call = functools.partial(
        ws.resolve,
        requirements,
        installer=FakeInstaller(installable_dists),
        replace_conflicting=replace_conflicting,
    )
    if inspect.isclass(resolved_dists_or_exception):
        with pytest.raises(resolved_dists_or_exception):
            resolve_call()
    else:
        assert sorted(resolve_call()) == sorted(resolved_dists_or_exception)

