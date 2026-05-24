import json
import os

PROFILE_PATH = "user_profile.json"


def load_profile():

    if not os.path.exists(PROFILE_PATH):

        return {
            "name": "",
            "favorite_apps": [],
            "favorite_websites": [],
            "habits": [],
            "preferences": [],
            "important_people": [],
            "goals": [],
            "projects": []
        }

    with open(PROFILE_PATH, "r") as file:

        return json.load(file)


def save_profile(profile):

    with open(PROFILE_PATH, "w") as file:

        json.dump(
            profile,
            file,
            indent=4
        )


def add_profile_item(category, value):

    profile = load_profile()

    if category not in profile:
        return

    if value not in profile[category]:

        profile[category].append(value)

    save_profile(profile)