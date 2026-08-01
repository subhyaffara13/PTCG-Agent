
def print_saved_residuals(f, *args, **kwargs):
  for aval, src in saved_residuals(f, *args, **kwargs):
    print(f'{aval.str_short(short_dtypes=True)} {src}')

