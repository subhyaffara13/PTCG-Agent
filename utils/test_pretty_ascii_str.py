
def test_pretty_ascii_str():
    assert pretty( 'xxx' ) == 'xxx'
    assert pretty( "xxx" ) == 'xxx'
    assert pretty( 'xxx\'xxx' ) == 'xxx\'xxx'
    assert pretty( 'xxx"xxx' ) == 'xxx\"xxx'
    assert pretty( 'xxx\"xxx' ) == 'xxx\"xxx'
    assert pretty( "xxx'xxx" ) == 'xxx\'xxx'
    assert pretty( "xxx\'xxx" ) == 'xxx\'xxx'
    assert pretty( "xxx\"xxx" ) == 'xxx\"xxx'
    assert pretty( "xxx\"xxx\'xxx" ) == 'xxx"xxx\'xxx'
    assert pretty( "xxx\nxxx" ) == 'xxx\nxxx'

