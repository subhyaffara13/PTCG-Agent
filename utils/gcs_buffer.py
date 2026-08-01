
def gcs_buffer():
    """Emulate GCS using a binary buffer."""
    pytest.importorskip("gcsfs")
    fsspec = pytest.importorskip("fsspec")

    gcs_buffer = BytesIO()
    gcs_buffer.close = lambda: True

    class MockGCSFileSystem(fsspec.AbstractFileSystem):
        @staticmethod
        def open(*args, **kwargs):
            gcs_buffer.seek(0)
            return gcs_buffer

        def ls(self, path, **kwargs):
            # needed for pyarrow
            return [{"name": path, "type": "file"}]

    # Overwrites the default implementation from gcsfs to our mock class
    fsspec.register_implementation("gs", MockGCSFileSystem, clobber=True)

    return gcs_buffer

