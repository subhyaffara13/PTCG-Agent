
def test_bad_resolver_raises(engine, parser):
    cannot_resolve = 42, 3.0
    with pytest.raises(TypeError, match="Resolver of type .+"):
        pd.eval("1 + 2", resolvers=cannot_resolve, engine=engine, parser=parser)

