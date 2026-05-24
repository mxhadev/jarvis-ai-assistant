import json
import os
from datetime import datetime

HABIT_PATH = "habits.json"


def load_habits():

    if not os.path.exists(HABIT_PATH):

        return {}

    with open(HABIT_PATH, "r") as file:

        return json.load(file)


def save_habits(habits):

    with open(HABIT_PATH, "w") as file:

        json.dump(
            habits,
            file,
            indent=4
        )


def track_action(action_name):

    habits = load_habits()

    current_hour = datetime.now().hour

    if action_name not in habits:

        habits[action_name] = {
            "count": 0,
            "hours": []
        }

    habits[action_name]["count"] += 1

    habits[action_name]["hours"].append(current_hour)

    save_habits(habits)