
def generate_tests(
    prefix: str,
    mixin: type[RpcAgentTestFixture],
    tests: list[type[RpcAgentTestFixture]],
    module_name: str,
) -> dict[str, type[RpcAgentTestFixture]]:
    """Mix in the classes needed to autogenerate the tests based on the params.

    Takes a series of test suites, each written against a "generic" agent (i.e.,
    derived from the abstract RpcAgentTestFixture class), as the `tests` args.
    Takes a concrete subclass of RpcAgentTestFixture, which specializes it for a
    certain agent, as the `mixin` arg. Produces all combinations of them.
    Returns a dictionary of class names to class type
    objects which can be inserted into the global namespace of the calling
    module. The name of each test will be a concatenation of the `prefix` arg
    and the original name of the test suite.
    The `module_name` should be the name of the calling module so
    that the classes can be fixed to make it look like they belong to it, which
    is necessary for pickling to work on them.
    """
    ret: dict[str, type[RpcAgentTestFixture]] = {}
    for test_class in tests:
        if IS_SANDCASTLE and TEST_WITH_DEV_DBG_ASAN:
            print(
                f"Skipping test {test_class} on sandcastle for the following reason: "
                "Skip dev-asan as torch + multiprocessing spawn have known issues",
                file=sys.stderr,
            )
            continue

        name = f"{prefix}{test_class.__name__}"
        class_ = type(name, (test_class, mixin, SpawnHelper), {})
        class_.__module__ = module_name
        ret[name] = class_
    return ret

