from voice import listen, speak

while True:

    user = listen()

    if user:

        speak(f"You said {user}")

    if "exit" in user:
        break