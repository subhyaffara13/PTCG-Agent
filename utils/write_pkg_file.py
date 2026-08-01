
def write_pkg_file(self, file):  # noqa: C901  # is too complex (14)  # FIXME
    """Write the PKG-INFO format data to a file object."""
    version = self.get_metadata_version()

    def write_field(key, value):
        file.write(f"{key}: {value}\n")

    write_field('Metadata-Version', str(version))
    write_field('Name', self.get_name())
    write_field('Version', self.get_version())

    summary = self.get_description()
    if summary:
        write_field('Summary', single_line(summary))

    optional_fields = (
        ('Home-page', 'url'),
        ('Download-URL', 'download_url'),
        ('Author', 'author'),
        ('Author-email', 'author_email'),
        ('Maintainer', 'maintainer'),
        ('Maintainer-email', 'maintainer_email'),
    )

    for field, attr in optional_fields:
        attr_val = getattr(self, attr, None)
        if attr_val is not None:
            write_field(field, attr_val)

    if license_expression := self.license_expression:
        write_field('License-Expression', license_expression)
    elif license := self.get_license():
        write_field('License', rfc822_escape(license))

    for label, url in self.project_urls.items():
        write_field('Project-URL', f'{label}, {url}')

    keywords = ','.join(self.get_keywords())
    if keywords:
        write_field('Keywords', keywords)

    platforms = self.get_platforms() or []
    for platform in platforms:
        write_field('Platform', platform)

    self._write_list(file, 'Classifier', self.get_classifiers())

    # PEP 314
    self._write_list(file, 'Requires', self.get_requires())
    self._write_list(file, 'Provides', self.get_provides())
    self._write_list(file, 'Obsoletes', self.get_obsoletes())

    # Setuptools specific for PEP 345
    if hasattr(self, 'python_requires'):
        write_field('Requires-Python', self.python_requires)

    # PEP 566
    if self.long_description_content_type:
        write_field('Description-Content-Type', self.long_description_content_type)

    safe_license_files = map(_safe_license_file, self.license_files or [])
    self._write_list(file, 'License-File', safe_license_files)
    _write_requirements(self, file)

    for field, attr in _POSSIBLE_DYNAMIC_FIELDS.items():
        if (val := getattr(self, attr, None)) and not is_static(val):
            write_field('Dynamic', field)

    long_description = self.get_long_description()
    if long_description:
        file.write(f"\n{long_description}")
        if not long_description.endswith("\n"):
            file.write("\n")

