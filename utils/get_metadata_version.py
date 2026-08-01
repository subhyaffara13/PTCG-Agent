
def get_metadata_version(self):
    mv = getattr(self, 'metadata_version', None)
    if mv is None:
        mv = Version('2.4')
        self.metadata_version = mv
    return mv

