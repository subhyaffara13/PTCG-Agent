
def test_del_attr_handling():
    # DataSource __del__ can be called
    # even if __init__ fails when the
    # Exception object is caught by the
    # caller as happens in refguide_check
    # is_deprecated() function

    ds = datasource.DataSource()
    # simulate failed __init__ by removing key attribute
    # produced within __init__ and expected by __del__
    del ds._istmpdest
    # should not raise an AttributeError if __del__
    # gracefully handles failed __init__:
    ds.__del__()

