
def test_read_metadata(name, attrs):
    dist = Distribution(attrs)
    metadata_out = dist.metadata
    dist_class = metadata_out.__class__

    # Write to PKG_INFO and then load into a new metadata object
    PKG_INFO = io.StringIO()

    metadata_out.write_pkg_file(PKG_INFO)
    PKG_INFO.seek(0)
    pkg_info = PKG_INFO.read()
    assert _valid_metadata(pkg_info)

    PKG_INFO.seek(0)
    metadata_in = dist_class()
    metadata_in.read_pkg_file(PKG_INFO)

    tested_attrs = [
        ('name', dist_class.get_name),
        ('version', dist_class.get_version),
        ('author', dist_class.get_contact),
        ('author_email', dist_class.get_contact_email),
        ('metadata_version', dist_class.get_metadata_version),
        ('provides', dist_class.get_provides),
        ('description', dist_class.get_description),
        ('long_description', dist_class.get_long_description),
        ('download_url', dist_class.get_download_url),
        ('keywords', dist_class.get_keywords),
        ('platforms', dist_class.get_platforms),
        ('obsoletes', dist_class.get_obsoletes),
        ('requires', dist_class.get_requires),
        ('classifiers', dist_class.get_classifiers),
        ('project_urls', lambda s: getattr(s, 'project_urls', {})),
        ('provides_extras', lambda s: getattr(s, 'provides_extras', {})),
    ]

    for attr, getter in tested_attrs:
        assert getter(metadata_in) == getter(metadata_out)

