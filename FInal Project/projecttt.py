class TrackYourProfessor:
    def __init__(self):
        self.users = {}
        self.professors = {}

    def register_user(self, name, email, password, role):
        if email in self.users:
            print("Email already exists! Please choose a different email.")
            return
        self.users[email] = {"name": name, "password": password, "role": role}
        self.save_user_data()
        print("User registered successfully!")

    def login(self, email, password):
        if email in self.users:
            if self.users[email]["password"] == password:
                print(f"Welcome back, {self.users[email]['name']}!")
                return True
            else:
                print("Incorrect password!")
                return False
        else:
            print("User not found!")
            return False

    def save_user_data(self):
        with open("user_data.txt", "w") as file:
            for email, data in self.users.items():
                file.write(f"{email},{data['name']},{data['password']},{data['role']}\n")

    def load_user_data(self):
        try:
            with open("user_data.txt", "r") as file:
                for line in file:
                    email, name, password, role = line.strip().split(',')
                    self.users[email] = {"name": name, "password": password, "role": role}
        except FileNotFoundError:
            print("No existing user data found. Starting with an empty user database.")


def main():
    tracker = TrackYourProfessor()
    tracker.load_user_data()

    print("Welcome to Track Your Professor")

    while True:
        print("\nMain Menu:")
        print("1. Login")
        print("2. Register Now")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            # Login
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            tracker.login(email, password)

        elif choice == '2':
            # Register
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            role = input("Enter your role (Student/Professor/Teaching Assistant): ")
            tracker.register_user(name, email, password, role)

        elif choice == '3':
            print("Exiting Track Your Professor. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()
