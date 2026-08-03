import re

def parse_distributions(s):
    """
    Parse a series of distribution specs of the form:
    {project_name}-{version}
       [optional, indented requirements specification]

    Example:

        foo-0.2
        bar-1.0
          foo>=3.0
          [feature]
          baz

    yield 2 distributions:
        - project_name=foo, version=0.2
        - project_name=bar, version=1.0,
          requires=['foo>=3.0', 'baz; extra=="feature"']
    """
    s = s.strip()
    for spec in re.split(r'\n(?=[^\s])', s):
        if not spec:
            continue
        fields = spec.split('\n', 1)
        assert 1 <= len(fields) <= 2
        name, version = fields.pop(0).rsplit('-', 1)
        if fields:
            requires = textwrap.dedent(fields.pop(0))
            metadata = Metadata(('requires.txt', requires))
        else:
            metadata = None
        dist = pkg_resources.Distribution(
            project_name=name, version=version, metadata=metadata
        )
        yield dist

