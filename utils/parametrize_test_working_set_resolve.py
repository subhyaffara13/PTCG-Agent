
def parametrize_test_working_set_resolve(*test_list):
    idlist = []
    argvalues = []
    for test in test_list:
        (
            name,
            installed_dists,
            installable_dists,
            requirements,
            expected1,
            expected2,
        ) = (
            strip_comments(s.lstrip())
            for s in textwrap.dedent(test).lstrip().split('\n\n', 5)
        )
        installed_dists = list(parse_distributions(installed_dists))
        installable_dists = list(parse_distributions(installable_dists))
        requirements = list(pkg_resources.parse_requirements(requirements))
        for id_, replace_conflicting, expected in (
            (name, False, expected1),
            (name + '_replace_conflicting', True, expected2),
        ):
            idlist.append(id_)
            expected = strip_comments(expected.strip())
            if re.match(r'\w+$', expected):
                expected = getattr(pkg_resources, expected)
                assert issubclass(expected, Exception)
            else:
                expected = list(parse_distributions(expected))
            argvalues.append(
                pytest.param(
                    installed_dists,
                    installable_dists,
                    requirements,
                    replace_conflicting,
                    expected,
                )
            )
    return pytest.mark.parametrize(
        (
            "installed_dists",
            "installable_dists",
            "requirements",
            "replace_conflicting",
            "resolved_dists_or_exception",
        ),
        argvalues,
        ids=idlist,
    )

