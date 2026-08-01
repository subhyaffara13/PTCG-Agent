
def _datetime_metadata_str(dtype):
    # TODO: this duplicates the C metastr_to_unicode functionality
    unit, count = np.datetime_data(dtype)
    if unit == 'generic':
        return ''
    elif count == 1:
        return f'[{unit}]'
    else:
        return f'[{count}{unit}]'

