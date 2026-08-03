import random

def generate_feedback_box():
    box_width = 60

    # Select a random message
    message = random.choice(list_of_messages)

    print()  # noqa: T201
    print("\033[1;37m" + "#" + "-" * box_width + "#\033[0m")  # noqa: T201
    print("\033[1;37m" + "#" + " " * box_width + "#\033[0m")  # noqa: T201
    print("\033[1;37m" + "# {:^59} #\033[0m".format(message))  # noqa: T201
    print(  # noqa: T201
        "\033[1;37m"
        + "# {:^59} #\033[0m".format("https://github.com/BerriAI/litellm/issues/new")
    )
    print("\033[1;37m" + "#" + " " * box_width + "#\033[0m")  # noqa: T201
    print("\033[1;37m" + "#" + "-" * box_width + "#\033[0m")  # noqa: T201
    print()  # noqa: T201
    print(" Thank you for using LiteLLM! - Krrish & Ishaan")  # noqa: T201
    print()  # noqa: T201
    print()  # noqa: T201
    print()  # noqa: T201
    print(  # noqa: T201
        "\033[1;31mGive Feedback / Get Help: https://github.com/BerriAI/litellm/issues/new\033[0m"
    )
    print()  # noqa: T201
    print()  # noqa: T201

