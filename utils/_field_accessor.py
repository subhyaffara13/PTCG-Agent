
def _field_accessor(name: str, field: str, docstring: str | None = None):
    def f(self):
        values = self._local_timestamps()

        if field in self._bool_ops:
            result: np.ndarray

            if field.endswith(("start", "end")):
                freq = self.freq
                month_kw = 12
                if freq:
                    kwds = freq.kwds
                    month_kw = kwds.get("startingMonth", kwds.get("month", month_kw))

                if freq is not None:
                    freq_name = freq.name
                else:
                    freq_name = None
                result = fields.get_start_end_field(
                    values, field, freq_name, month_kw, reso=self._creso
                )
            else:
                result = fields.get_date_field(values, field, reso=self._creso)

            # these return a boolean by-definition
            return result

        result = fields.get_date_field(values, field, reso=self._creso)
        result = self._maybe_mask_results(result, fill_value=None, convert="float64")

        return result

    f.__name__ = name
    f.__doc__ = docstring
    return property(f)


def _field_accessor(name: str, docstring: str | None = None):
    def f(self):
        base = self.dtype._dtype_code
        result = get_period_field_arr(name, self.asi8, base)
        return result

    f.__name__ = name
    f.__doc__ = docstring
    return property(f)


def _field_accessor(name: str, alias: str, docstring: str):
    def f(self) -> np.ndarray:
        values = self.asi8
        if alias == "days":
            result = get_timedelta_days(values, reso=self._creso)
        else:
            # error: Incompatible types in assignment (
            # expression has type "ndarray[Any, dtype[signedinteger[_32Bit]]]",
            # variable has type "ndarray[Any, dtype[signedinteger[_64Bit]]]
            result = get_timedelta_field(values, alias, reso=self._creso)  # type: ignore[assignment]
        if self._hasna:
            result = self._maybe_mask_results(
                result, fill_value=None, convert="float64"
            )

        return result

    f.__name__ = name
    f.__doc__ = f"\n{docstring}\n"
    return property(f)

