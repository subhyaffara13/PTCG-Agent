
def test_embed_limit(method_name, caplog, anim):
    caplog.set_level("WARNING")
    with mpl.rc_context({"animation.embed_limit": 1e-6}):  # ~1 byte.
        getattr(anim, method_name)()
    assert len(caplog.records) == 1
    record, = caplog.records
    assert (record.name == "matplotlib.animation"
            and record.levelname == "WARNING")

