import re

def test_trace_to_file(stream_trace):
    file = tempfile.NamedTemporaryFile(mode='r')
    with detect.trace(file.name, mode='w'):
        dill.dumps(test_obj)
    file_trace = file.read()
    file.close()
    # Apparently, objects can change location in memory...
    reghex = re.compile(r'0x[0-9A-Za-z]+')
    file_trace, stream_trace = reghex.sub('0x', file_trace), reghex.sub('0x', stream_trace)
    # PyPy prints dictionary contents with repr(dict)...
    regdict = re.compile(r'(dict\.__repr__ of ).*')
    file_trace, stream_trace = regdict.sub(r'\1{}>', file_trace), regdict.sub(r'\1{}>', stream_trace)
    assert file_trace == stream_trace

