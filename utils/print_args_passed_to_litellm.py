
def print_args_passed_to_litellm(original_function, args, kwargs):
    if not _is_debugging_on():
        return
    try:
        # we've already printed this for acompletion, don't print for completion
        if (
            "acompletion" in kwargs
            and kwargs["acompletion"] is True
            and original_function.__name__ == "completion"
        ):
            return
        elif (
            "aembedding" in kwargs
            and kwargs["aembedding"] is True
            and original_function.__name__ == "embedding"
        ):
            return
        elif (
            "aimg_generation" in kwargs
            and kwargs["aimg_generation"] is True
            and original_function.__name__ == "img_generation"
        ):
            return

        args_str = ", ".join(map(repr, args))
        kwargs_str = ", ".join(f"{key}={repr(value)}" for key, value in kwargs.items())
        print_verbose(
            "\n",
        )  # new line before
        print_verbose(
            "\033[92mRequest to litellm:\033[0m",
        )
        if args and kwargs:
            print_verbose(
                f"\033[92mlitellm.{original_function.__name__}({args_str}, {kwargs_str})\033[0m"
            )
        elif args:
            print_verbose(
                f"\033[92mlitellm.{original_function.__name__}({args_str})\033[0m"
            )
        elif kwargs:
            print_verbose(
                f"\033[92mlitellm.{original_function.__name__}({kwargs_str})\033[0m"
            )
        else:
            print_verbose(f"\033[92mlitellm.{original_function.__name__}()\033[0m")
        print_verbose("\n")  # new line after
    except Exception:
        # This should always be non blocking
        pass

