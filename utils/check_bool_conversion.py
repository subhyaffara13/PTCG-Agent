
def check_bool_conversion(arr: Array):
  if arr.size == 0:
    raise ValueError("The truth value of an empty array is ambiguous. Use"
                     " `array.size > 0` to check that an array is not empty.")
  if arr.size > 1:
    raise ValueError("The truth value of an array with more than one element"
                     " is ambiguous. Use a.any() or a.all()")

