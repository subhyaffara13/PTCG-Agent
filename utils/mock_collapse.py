
def mock_collapse():
  with mock.patch('etils.ecolab.colab_utils.collapse', contextlib.nullcontext):
    yield

