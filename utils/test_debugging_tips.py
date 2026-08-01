
def test_debugging_tips(tmpdir_cwd, monkeypatch):
    """Make sure to display useful debugging tips to the user."""
    jaraco.path.build({"module.py": "x = 42"})
    dist = Distribution()
    dist.script_name = "setup.py"
    dist.set_defaults()
    cmd = editable_wheel(dist)
    cmd.ensure_finalized()

    SimulatedErr = type("SimulatedErr", (Exception,), {})
    simulated_failure = Mock(side_effect=SimulatedErr())
    monkeypatch.setattr(cmd, "get_finalized_command", simulated_failure)

    with pytest.raises(SimulatedErr) as ctx:
        cmd.run()
    assert any('debugging-tips' in note for note in ctx.value.__notes__)

