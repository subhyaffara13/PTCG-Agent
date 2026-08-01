
def test_pretty_unicode_str():
    assert pretty( 'xxx' ) == 'xxx'
    assert pretty( 'xxx' ) == 'xxx'
    assert pretty( 'xxx\'xxx' ) == 'xxx\'xxx'
    assert pretty( 'xxx"xxx' ) == 'xxx\"xxx'
    assert pretty( 'xxx\"xxx' ) == 'xxx\"xxx'
    assert pretty( "xxx'xxx" ) == 'xxx\'xxx'
    assert pretty( "xxx\'xxx" ) == 'xxx\'xxx'
    assert pretty( "xxx\"xxx" ) == 'xxx\"xxx'
    assert pretty( "xxx\"xxx\'xxx" ) == 'xxx"xxx\'xxx'
    assert pretty( "xxx\nxxx" ) == 'xxx\nxxx'

