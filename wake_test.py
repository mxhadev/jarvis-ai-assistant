from voice import (
    wait_for_wake_word,
    listen,
    speak
)

while True:

    wait_for_wake_word()

    command = listen()

    if command:

        speak(f"You said {command}")

    if "exit" in command:
        break