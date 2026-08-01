
def _write_provides_extra(file, processed_extras, safe, unsafe):
    previous = processed_extras.get(safe)
    if previous == unsafe:
        SetuptoolsDeprecationWarning.emit(
            'Ambiguity during "extra" normalization for dependencies.',
            f"""
            {previous!r} and {unsafe!r} normalize to the same value:\n
                {safe!r}\n
            In future versions, setuptools might halt the build process.
            """,
            see_url="https://peps.python.org/pep-0685/",
        )
    else:
        processed_extras[safe] = unsafe
        file.write(f"Provides-Extra: {safe}\n")

