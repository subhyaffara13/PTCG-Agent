
def _convert_to_highs_enum(option, option_str, choices):
    # If option is in the choices we can look it up, if not use
    # the default value taken from function signature and warn:
    try:
        return choices[option.lower()]
    except AttributeError:
        return choices[option]
    except KeyError:
        sig = inspect.signature(_linprog_highs)
        default_str = sig.parameters[option_str].default
        warn(f"Option {option_str} is {option}, but only values in "
             f"{set(choices.keys())} are allowed. Using default: "
             f"{default_str}.",
             OptimizeWarning, stacklevel=3)
        return choices[default_str]

