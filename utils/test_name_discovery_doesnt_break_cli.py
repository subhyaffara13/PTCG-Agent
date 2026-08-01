
def test_name_discovery_doesnt_break_cli(tmpdir_cwd):
    jaraco.path.build({"pkg.py": ""})
    dist = Distribution({})
    dist.script_args = ["--name"]
    dist.set_defaults()
    dist.parse_command_line()  # <-- no exception should be raised here.
    assert dist.get_name() == "pkg"

