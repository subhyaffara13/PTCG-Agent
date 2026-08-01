
def sys_executable_encodable():
    try:
        sys.executable.encode('UTF-8')
    except UnicodeEncodeError:
        pytest.skip("sys.executable is not encodable to UTF-8")

