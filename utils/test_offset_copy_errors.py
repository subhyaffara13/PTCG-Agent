
def test_offset_copy_errors():
    with pytest.raises(ValueError,
                       match="'fontsize' is not a valid value for units. "
                             "Supported values are 'dots', 'points', 'inches'"):
        mtransforms.offset_copy(None, units='fontsize')

    with pytest.raises(ValueError,
                       match='For units of inches or points a fig kwarg is needed'):
        mtransforms.offset_copy(None, units='inches')

