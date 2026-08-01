
def __maintainer_test_cases():
    attrs = {"name": "package", "version": "1.0", "description": "xxx"}

    def merge_dicts(d1, d2):
        d1 = d1.copy()
        d1.update(d2)

        return d1

    return [
        ('No author, no maintainer', attrs.copy()),
        (
            'Author (no e-mail), no maintainer',
            merge_dicts(attrs, {'author': 'Author Name'}),
        ),
        (
            'Author (e-mail), no maintainer',
            merge_dicts(
                attrs, {'author': 'Author Name', 'author_email': 'author@name.com'}
            ),
        ),
        (
            'No author, maintainer (no e-mail)',
            merge_dicts(attrs, {'maintainer': 'Maintainer Name'}),
        ),
        (
            'No author, maintainer (e-mail)',
            merge_dicts(
                attrs,
                {
                    'maintainer': 'Maintainer Name',
                    'maintainer_email': 'maintainer@name.com',
                },
            ),
        ),
        (
            'Author (no e-mail), Maintainer (no-email)',
            merge_dicts(
                attrs, {'author': 'Author Name', 'maintainer': 'Maintainer Name'}
            ),
        ),
        (
            'Author (e-mail), Maintainer (e-mail)',
            merge_dicts(
                attrs,
                {
                    'author': 'Author Name',
                    'author_email': 'author@name.com',
                    'maintainer': 'Maintainer Name',
                    'maintainer_email': 'maintainer@name.com',
                },
            ),
        ),
        (
            'No author (e-mail), no maintainer (e-mail)',
            merge_dicts(
                attrs,
                {
                    'author_email': 'author@name.com',
                    'maintainer_email': 'maintainer@name.com',
                },
            ),
        ),
        ('Author unicode', merge_dicts(attrs, {'author': '鉄沢寛'})),
        ('Maintainer unicode', merge_dicts(attrs, {'maintainer': 'Jan Łukasiewicz'})),
    ]

