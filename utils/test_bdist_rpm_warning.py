
def test_bdist_rpm_warning(distutils_cmd, tmpdir_cwd):
    dist = Distribution(
        dict(
            script_name='setup.py',
            script_args=['bdist_rpm'],
            name='foo',
            py_modules=['hi'],
        )
    )
    dist.parse_command_line()
    with pytest.warns(SetuptoolsDeprecationWarning):
        dist.run_commands()

    distutils_cmd.run.assert_called_once()

