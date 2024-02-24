class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

class Professor(User):
    def __init__(self, username, timetable=None):
        super().__init__(username, "Professor")
        self.timetable = timetable if timetable else {}

    def update_timetable(self, new_timetable):
        self.timetable = new_timetable


class MeetingScheduler:
    def __init__(self):
        self.students = {}
        self.professors = {}
        self.pending_meetings = {}
        self.time_table_meetings = {}
        self.registered_users = set()
        self.load_registered_users()

    def register_user(self, username, role):
        if username in self.registered_users:
            print("Username already exists.")
            return
        self.registered_users.add(username)
        if role.lower() == 'student':
            self.add_student(username)
        elif role.lower() == 'professor':
            self.add_professor(username)
        else:
            print("Invalid role.")
            return
        with open("registered_users.txt", "a") as f:
            f.write(f"{username},{role.lower()}\n")
        print("User registered successfully.")

    def load_registered_users(self):
        try:
            with open("registered_users.txt", "r") as f:
                for line in f:
                    username, role = line.strip().split(",")
                    self.registered_users.add(username)
                    if role == 'student':
                        self.add_student(username)
                    elif role == 'professor':
                        self.add_professor(username)
        except FileNotFoundError:
            print("No registered users found.")

    def add_student(self, username):
        self.students[username] = []

    def add_professor(self, username):
        self.professors[username] = Professor(username)

    def login(self):
        username = input("Enter your username: ")
        role = input("Are you a student or a professor? ").lower()
        if username in self.registered_users:
            if role == 'student':
                return User(username, role)
            elif role == 'professor':
                return User(username, role)
            else:
                print("Invalid role.")
                return None
        else:
            print("Username not found. Please register first.")
            return None

    def select_professor(self):
        print("Available Professors:")
        for professor in self.professors.values():
            print(professor.username)
        professor_username = input("Enter the username of the professor you want to meet: ")
        if professor_username in self.professors:
            return self.professors[professor_username]
        else:
            print("Professor not found.")
            return None

    def request_meeting(self, student, professor, option):
        if professor.username in self.professors:
          option = int(option) 
          if len(self.time_table_meetings) >= option > 0:
            self.pending_meetings.setdefault(professor.username, []).append((student.username, self.time_table_meetings[option]))
            print("Meeting request sent to professor.")
          else:
            print("Invalid option. Please select from the available options.")
        else:
          print("Professor not found.")

    def view_timetable(self, professor):
        if isinstance(professor, Professor):
            print(f"Timetable for Professor {professor.username}:")
            # day_object = {}
            count_number =1
            for day, schedule in professor.timetable.items():
                print(f"{count_number}. {day}: {schedule}")
                self.time_table_meetings[count_number] = {day:schedule}
                count_number += 1
        else:
            print("Invalid professor object.")

    def view_requests(self, professor):
        if professor.username in self.professors:
            pending_meetings = self.pending_meetings.get(professor.username, [])
            if pending_meetings:
                print("Pending Meeting Requests:")
                for student, time in pending_meetings:
                    print(f"Student: {student}, Time: {time}")
            else:
                print("No pending meeting requests.")
        else:
            print("Professor not found.")

    def approve_meeting(self, professor):
        self.view_requests(professor)
        student_username = input("Enter the username of the student you want to approve the meeting for: ")
        if professor.username in self.professors:
            if student_username in [meeting[0] for meeting in self.pending_meetings.get(professor.username, [])]:
                professor_instance = self.professors[professor.username]
                new_timetable = professor_instance.timetable.copy()
                new_timetable.update(self.pending_meetings[professor.username])
                professor_instance.update_timetable(new_timetable)
                del self.pending_meetings[professor.username]
                print("Meeting approved.")
            else:
                print("No pending meeting request from this student.")
        else:
            print("Professor not found.")

    def add_timetable(self, professor):
        if professor.username in self.professors:
            new_timetable = {}
            for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                schedule = input(f"Enter schedule for {day} (or leave blank if not available): ")
                if schedule.strip():
                    new_timetable[day] = schedule
            self.professors[professor.username].update_timetable(new_timetable)
            print("Timetable updated successfully.")
        else:
            print("Professor not found.")

    def get_professor_timetable(self, professor_username):
        if professor_username in self.professors:
            return self.professors[professor_username].timetable
        else:
            print("Professor not found.")
            return None

scheduler = MeetingScheduler()

while True:
    print("1. Login")
    print("2. Register")
    print("3. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        user = None
        while user is None:
            user = scheduler.login()

        if user.role == "student":
            professor = scheduler.select_professor()
            if professor:
                professor_timetable = scheduler.get_professor_timetable(professor.username)
                if professor_timetable:
                    scheduler.view_timetable(professor)
                option = input("Enter the option for the meeting: ")
                scheduler.request_meeting(user, professor, option)
        elif user.role == "professor":
            while True:
                print("1. View Meeting Requests")
                print("2. View Timetable")
                print("3. Approve Meeting")
                print("4. Update Timetable")
                print("5. Logout")
                choice = input("Enter your choice: ")
                if choice == "1":
                    scheduler.view_requests(user)
                elif choice == "2":
                    scheduler.view_timetable(scheduler.professors[user.username])  # Pass professor object
                elif choice == "3":
                    scheduler.approve_meeting(user)
                elif choice == "4":
                    scheduler.add_timetable(scheduler.professors[user.username])  # Pass professor object
                elif choice == "5":
                    break
                else:
                    print("Invalid choice. Please try again.")

    elif choice == "2":
        username = input("Enter your username: ")
        role = input("Are you a student or a professor? ").lower()
        scheduler.register_user(username, role)
    elif choice == "3":
        break
    else:
        print("Invalid choice. Please try again.")