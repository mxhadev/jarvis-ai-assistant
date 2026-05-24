from actions.tools import (
    open_website,
    open_vscode,
    get_time,
    youtube_search,
    google_search,
    play_youtube,
    type_text,
    press_key,
    take_screenshot,
    analyze_screen_tool
)
from memory.memory_manager import forget_memory
def execute_action(action_data):

    action = action_data.get("action")

    if action == "open_website":
        return open_website(
            action_data.get("target")
        )

    elif action == "open_vscode":
        return open_vscode()

    elif action == "get_time":
        return get_time()
    elif action == "youtube_search":
        return youtube_search(
         action_data.get("query")
    )

    elif action == "google_search":
        return google_search(
          action_data.get("query")
    )
    elif action == "analyze_screen":
        return analyze_screen_tool()
    elif action == "play_youtube":
        return play_youtube(
          action_data.get("query")
    )
    elif action == "forget_memory":
        return forget_memory(
          action_data.get("query")
    )
    elif action == "type_text":
        return type_text(
          action_data.get("text")
    )

    elif action == "press_key":
        return press_key(
          action_data.get("key")
    )

    elif action == "take_screenshot":
        return take_screenshot()
    else:
        return "Unknown action."