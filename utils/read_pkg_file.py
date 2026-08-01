
def read_pkg_file(self, file):
    """Reads the metadata values from a file object."""
    msg = message_from_file(file)

    self.metadata_version = Version(msg['metadata-version'])
    self.name = _read_field_from_msg(msg, 'name')
    self.version = _read_field_from_msg(msg, 'version')
    self.description = _read_field_from_msg(msg, 'summary')
    # we are filling author only.
    self.author = _read_field_from_msg(msg, 'author')
    self.maintainer = None
    self.author_email = _read_field_from_msg(msg, 'author-email')
    self.maintainer_email = None
    self.url = _read_field_from_msg(msg, 'home-page')
    self.download_url = _read_field_from_msg(msg, 'download-url')
    self.license = _read_field_unescaped_from_msg(msg, 'license')
    self.license_expression = _read_field_unescaped_from_msg(msg, 'license-expression')

    self.long_description = _read_field_unescaped_from_msg(msg, 'description')
    if self.long_description is None and self.metadata_version >= Version('2.1'):
        self.long_description = _read_payload_from_msg(msg)
    self.description = _read_field_from_msg(msg, 'summary')

    if 'keywords' in msg:
        self.keywords = _read_field_from_msg(msg, 'keywords').split(',')

    self.platforms = _read_list_from_msg(msg, 'platform')
    self.classifiers = _read_list_from_msg(msg, 'classifier')

    # PEP 314 - these fields only exist in 1.1
    if self.metadata_version == Version('1.1'):
        self.requires = _read_list_from_msg(msg, 'requires')
        self.provides = _read_list_from_msg(msg, 'provides')
        self.obsoletes = _read_list_from_msg(msg, 'obsoletes')
    else:
        self.requires = None
        self.provides = None
        self.obsoletes = None

    self.license_files = _read_list_from_msg(msg, 'license-file')

