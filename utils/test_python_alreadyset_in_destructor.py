
def test_python_alreadyset_in_destructor(monkeypatch, capsys):
    hooked = False
    triggered = False

    if hasattr(sys, "unraisablehook"):  # Python 3.8+
        hooked = True
        # Don't take `sys.unraisablehook`, as that's overwritten by pytest
        default_hook = sys.__unraisablehook__

        def hook(unraisable_hook_args):
            exc_type, exc_value, exc_tb, err_msg, obj = unraisable_hook_args
            if obj == "already_set demo":
                nonlocal triggered
                triggered = True
            default_hook(unraisable_hook_args)
            return

        # Use monkeypatch so pytest can apply and remove the patch as appropriate
        monkeypatch.setattr(sys, "unraisablehook", hook)

    assert m.python_alreadyset_in_destructor("already_set demo") is True
    if hooked:
        assert triggered is True

    _, captured_stderr = capsys.readouterr()
    assert captured_stderr.startswith("Exception ignored in: 'already_set demo'")
    assert captured_stderr.rstrip().endswith("KeyError: 'bar'")

