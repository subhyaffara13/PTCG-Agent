import os
import sys

def get_default_xml_output_filename() -> str | None:
  if os.environ.get('XML_OUTPUT_FILE'):
    return os.environ['XML_OUTPUT_FILE']
  elif os.environ.get('RUNNING_UNDER_TEST_DAEMON'):
    return os.path.join(os.path.dirname(TEST_TMPDIR.value), 'test_detail.xml')
  elif os.environ.get('TEST_XMLOUTPUTDIR'):
    return os.path.join(
        os.environ['TEST_XMLOUTPUTDIR'],
        os.path.splitext(os.path.basename(sys.argv[0]))[0] + '.xml')
  return None

