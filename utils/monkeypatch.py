
def monkeypatch() -> Generator[MonkeyPatch]:
    """A convenient fixture for monkey-patching.

    The fixture provides these methods to modify objects, dictionaries, or
    :data:`os.environ`:

    * :meth:`monkeypatch.setattr(obj, name, value, raising=True) <pytest.MonkeyPatch.setattr>`
    * :meth:`monkeypatch.delattr(obj, name, raising=True) <pytest.MonkeyPatch.delattr>`
    * :meth:`monkeypatch.setitem(mapping, name, value) <pytest.MonkeyPatch.setitem>`
    * :meth:`monkeypatch.delitem(obj, name, raising=True) <pytest.MonkeyPatch.delitem>`
    * :meth:`monkeypatch.setenv(name, value, prepend=None) <pytest.MonkeyPatch.setenv>`
    * :meth:`monkeypatch.delenv(name, raising=True) <pytest.MonkeyPatch.delenv>`
    * :meth:`monkeypatch.syspath_prepend(path) <pytest.MonkeyPatch.syspath_prepend>`
    * :meth:`monkeypatch.chdir(path) <pytest.MonkeyPatch.chdir>`
    * :meth:`monkeypatch.context() <pytest.MonkeyPatch.context>`

    All modifications will be undone after the requesting test function or
    fixture has finished. The ``raising`` parameter determines if a :class:`KeyError`
    or :class:`AttributeError` will be raised if the set/deletion operation does not have the
    specified target.

    To undo modifications done by the fixture in a contained scope,
    use :meth:`context() <pytest.MonkeyPatch.context>`.
    """
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()

