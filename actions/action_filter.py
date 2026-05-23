def is_action_request(text):

    text = text.lower().strip()

    # Explicit time requests
    time_phrases = [
        "what's the time",
        "what is the time now",
        "current time",
        "tell me the time",
        "time now"
    ]

    for phrase in time_phrases:
        if phrase in text:
            return True

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