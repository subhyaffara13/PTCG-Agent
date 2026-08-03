import sys

def mock_colabtools():
  """colabtools only works in Colab, so mock it.."""
  module_mock = _ColabtoolsFrontEndMock('colabtools.frontend')
  sys.modules['colabtools'] = mock.MagicMock()
  sys.modules['colabtools.frontend'] = module_mock
  yield
  del sys.modules['colabtools.frontend']
  del sys.modules['colabtools']

