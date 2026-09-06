DATA_FILE = "study_log.txt"

def main():
    # Load existing sessions from the data file, if it exists.
    sessions = load_sessions()

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_session(sessions)
        elif choice == "2":
            view_sessions(sessions)
        elif choice == "3":
            subject = input("Enter subject to search for: ")
            search_by_subject(sessions, subject)
        elif choice == "4":
            study_statistics(sessions)
        elif choice == "5":
            save_sessions(sessions)
            print("Exiting the Smart Study Planner. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")




def add_session(sessions):
    # Prompt the user for session details and add a new session to the list.
    subject = input("Enter subject name: ")
    topic = input("Enter topic covered: ")
    date = input("Enter date/day (e.g. 2026-09-01 or Monday): ")

    # Keep asking until the user gives a valid, positive number for duration
    while True:
        duration_input = input("Enter duration of session (in minutes): ")
        try:
            duration = float(duration_input)
            if duration > 0:
                break
            else:
                print("Duration must be a positive number. Please try again.")
        except ValueError:
            print("That's not a valid number. Please try again.")

    session = {
        "subject": subject,
        "topic": topic,
        "date": date,
        "duration": duration,
    }
    sessions.append(session)
    print(f"\nSession added: {subject} ({classify_session(duration)}, {duration} min)\n")

def classify_session(duration):
    # Classify the session based on its duration.
    if duration < 30:
        return "Short"
    elif 30 <= duration <= 60:
        return "Medium"
    else:
        return "Long"

def view_sessions(sessions):
    # Display all logged study sessions in a tabular format, including their classification.
    if not sessions:
        print("\nNo study sessions have been logged yet.\n")
        return

    print("\n" + "-" * 70)
    print(f"{'Subject':<15}{'Topic':<20}{'Date':<12}{'Duration':<10}{'Type':<10}")
    print("-" * 70)

    for session in sessions:
        classification = classify_session(session["duration"])
        print(
            f"{session['subject']:<15}"
            f"{session['topic']:<20}"
            f"{session['date']:<12}"
            f"{session['duration']:<10.0f}"
            f"{classification:<10}"
        )

    print("-" * 70 + "\n")


def search_by_subject(sessions, subject):
    # Search for and display all sessions for a given subject, case-insensitively.
    matches = [s for s in sessions if s["subject"].lower() == subject.lower()]

    if not matches:
        print(f"\nNo sessions found for subject '{subject}'.\n")
        return

    print("\n" + "-" * 70)
    print(f"{'Subject':<15}{'Topic':<20}{'Date':<12}{'Duration':<10}{'Type':<10}")
    print("-" * 70)

    total_time = 0
    for session in matches:
        classification = classify_session(session["duration"])
        print(
            f"{session['subject']:<15}"
            f"{session['topic']:<20}"
            f"{session['date']:<12}"
            f"{session['duration']:<10.0f}"
            f"{classification:<10}"
        )
        total_time += session["duration"]

    print("-" * 70)
    print(f"Total time spent on {subject}: {total_time:.0f} minutes\n")


def study_statistics(sessions):
    # Display overall statistics about the logged study sessions, including total time, time per subject, weakest area, and longest session.
    if not sessions:
        print("\nNo study sessions have been logged yet, so no statistics to show.\n")
        return

    # Build a dictionary mapping subject -> total minutes studied
    subject_totals = {}
    for session in sessions:
        subject = session["subject"]
        subject_totals[subject] = subject_totals.get(subject, 0) + session["duration"]

    total_minutes = sum(subject_totals.values())

    # Subject with the least total study time = the weakest area
    weakest_subject = min(subject_totals, key=subject_totals.get)

    # The single longest session recorded, by duration
    longest_session = max(sessions, key=lambda s: s["duration"])

    print("\n----- STUDY STATISTICS -----")
    print(f"Total time studied overall: {total_minutes / 60:.2f} hours\n")

    print("Time studied per subject:")
    for subject, minutes in subject_totals.items():
        print(f"  {subject:<15}: {minutes / 60:.2f} hours")

    print(f"\nWeakest area (least total study time): {weakest_subject}")

    print(
        "\nLongest session recorded: "
        f"{longest_session['subject']} - {longest_session['topic']} "
        f"({longest_session['duration']:.0f} minutes on {longest_session['date']})"
    )
    print("-----------------------------\n")


def save_sessions(sessions, filename=DATA_FILE):
    # Save the current list of sessions to the data file, overwriting any previous contents.
    with open(filename, "w") as file:
        for session in sessions:
            line = f"{session['subject']}|{session['topic']}|{session['date']}|{session['duration']}\n"
            file.write(line)
    print(f"Sessions saved to {filename}.")


def load_sessions(filename=DATA_FILE):
    # Load the list of sessions from the data file, if it exists. If not, return an empty list.
    sessions = []
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                subject, topic, date, duration = line.split("|")
                sessions.append(
                    {
                        "subject": subject,
                        "topic": topic,
                        "date": date,
                        "duration": float(duration),
                    }
                )
    except FileNotFoundError:
        # No saved data yet - that's fine, just start with an empty list
        pass

    return sessions


def display_menu():
    # Display the main menu options to the user.
    print("\n===== SMART STUDY PLANNER =====")
    print("1. Add a study session")
    print("2. View all sessions")
    print("3. Search sessions by subject")
    print("4. View statistics")
    print("5. Save and exit")
    print("================================")

if __name__ == "__main__":
    main()
