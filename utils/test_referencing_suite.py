import json

def test_referencing_suite(test_path, subtests):
    dialect_id = DIALECT_IDS[test_path.relative_to(SUITE).parts[0]]
    specification = referencing.jsonschema.specification_with(dialect_id)
    loaded = json.loads(test_path.read_text())
    registry = loaded["registry"]
    registry = Registry().with_resources(
        (uri, specification.create_resource(contents))
        for uri, contents in loaded["registry"].items()
    )
    for test in loaded["tests"]:
        with subtests.test(test=test):
            if "normalization" in test_path.stem:
                pytest.xfail("APIs need to change for proper URL support.")

            resolver = registry.resolver(base_uri=test.get("base_uri", ""))

            if test.get("error"):
                with pytest.raises(Unresolvable):
                    resolver.lookup(test["ref"])
            else:
                resolved = resolver.lookup(test["ref"])
                assert resolved.contents == test["target"]

                then = test.get("then")
                while then:  # pragma: no cover
                    with subtests.test(test=test, then=then):
                        resolved = resolved.resolver.lookup(then["ref"])
                        assert resolved.contents == then["target"]
                    then = then.get("then")

