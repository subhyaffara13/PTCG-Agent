
def _show_fixture_action(
    fixturedef: FixtureDef[object], config: Config, msg: str
) -> None:
    capman = config.pluginmanager.getplugin("capturemanager")
    if capman:
        capman.suspend_global_capture()

    tw = config.get_terminal_writer()
    tw.line()
    # Use smaller indentation the higher the scope: Session = 0, Package = 1, etc.
    scope_indent = list(reversed(Scope)).index(fixturedef._scope)
    tw.write(" " * 2 * scope_indent)

    scopename = fixturedef.scope[0].upper()
    tw.write(f"{msg:<8} {scopename} {fixturedef.argname}")

    if msg == "SETUP":
        deps = sorted(arg for arg in fixturedef.argnames if arg != "request")
        if deps:
            tw.write(" (fixtures used: {})".format(", ".join(deps)))

    if hasattr(fixturedef, "cached_param"):
        tw.write(f"[{saferepr(fixturedef.cached_param, maxsize=42)}]")

    tw.flush()

    if capman:
        capman.resume_global_capture()

