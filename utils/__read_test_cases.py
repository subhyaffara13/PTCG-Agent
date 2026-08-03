import functools

def __read_test_cases():
    base = EXAMPLE_BASE_INFO

    params = functools.partial(dict, base)

    return [
        ('Metadata version 1.0', params()),
        (
            'Metadata Version 1.0: Short long description',
            params(
                long_description='Short long description',
            ),
        ),
        (
            'Metadata version 1.1: Classifiers',
            params(
                classifiers=[
                    'Programming Language :: Python :: 3',
                    'Programming Language :: Python :: 3.7',
                    'License :: OSI Approved :: MIT License',
                ],
            ),
        ),
        (
            'Metadata version 1.1: Download URL',
            params(
                download_url='https://example.com',
            ),
        ),
        (
            'Metadata Version 1.2: Requires-Python',
            params(
                python_requires='>=3.7',
            ),
        ),
        pytest.param(
            'Metadata Version 1.2: Project-Url',
            params(project_urls=dict(Foo='https://example.bar')),
            marks=pytest.mark.xfail(
                reason="Issue #1578: project_urls not read",
            ),
        ),
        (
            'Metadata Version 2.1: Long Description Content Type',
            params(
                long_description_content_type='text/x-rst; charset=UTF-8',
            ),
        ),
        (
            'License',
            params(
                license='MIT',
            ),
        ),
        (
            'License multiline',
            params(
                license='This is a long license \nover multiple lines',
            ),
        ),
        pytest.param(
            'Metadata Version 2.1: Provides Extra',
            params(provides_extras=['foo', 'bar']),
            marks=pytest.mark.xfail(reason="provides_extras not read"),
        ),
        (
            'Missing author',
            dict(
                name='foo',
                version='1.0.0',
                author_email='snorri@sturluson.name',
            ),
        ),
        (
            'Missing author e-mail',
            dict(
                name='foo',
                version='1.0.0',
                author='Snorri Sturluson',
            ),
        ),
        (
            'Missing author and e-mail',
            dict(
                name='foo',
                version='1.0.0',
            ),
        ),
        (
            'Bypass normalized version',
            dict(
                name='foo',
                version=sic('1.0.0a'),
            ),
        ),
    ]

