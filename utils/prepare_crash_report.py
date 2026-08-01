
def prepare_crash_report(ex: Exception, filepath: str, crash_file_path: str) -> Path:
    issue_template_path = (
        Path(PYLINT_HOME) / datetime.now().strftime(str(crash_file_path))
    ).resolve()
    with open(filepath, encoding="utf8") as f:
        file_content = f.read()
    template = ""
    if not issue_template_path.exists():
        template = """\
First, please verify that the bug is not already filled:
https://github.com/pylint-dev/pylint/issues/

Then create a new issue:
https://github.com/pylint-dev/pylint/issues/new?labels=Crash 💥%2CNeeds triage 📥


"""
    template += f"""
Issue title:
Crash ``{ex}`` (if possible, be more specific about what made pylint crash)

### Bug description

When parsing the following ``a.py``:

<!--
 If sharing the code is not an option, please state so,
 but providing only the stacktrace would still be helpful.
 -->

```python
{file_content}
```

### Command used

```shell
pylint a.py
```

### Pylint output

<details open>
    <summary>
        pylint crashed with a ``{ex.__class__.__name__}`` and with the following stacktrace:
    </summary>

```python
"""
    template += traceback.format_exc()
    template += f"""
```


</details>

### Expected behavior

No crash.

### Pylint version

```shell
{full_version}
```

### OS / Environment

{sys.platform} ({platform.system()})

### Additional dependencies

<!--
Please remove this part if you're not using any of
your dependencies in the example.
 -->
"""
    try:
        with open(issue_template_path, "a", encoding="utf8") as f:
            f.write(template)
    except Exception as exc:  # pylint: disable=broad-except
        print(
            f"Can't write the issue template for the crash in {issue_template_path} "
            f"because of: '{exc}'\nHere's the content anyway:\n{template}.",
            file=sys.stderr,
        )
    return issue_template_path

