def is_action_request(text):

    text = text.lower()

    action_starters = [

        "open",
        "play",
        "search",
        "launch",
        "start",
        "run",
        "close",
        "tell",
        "show",
        "forget",
        "delete",
        "remove"

    ]

    words = text.split()

    if not words:
        return False

    return words[0] in action_starters