import json
import os
import getpass

user_images = {}

def load_user_data():
    try:
        with open('user_data.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_user_data(data):
    with open('user_data.json', 'w') as file:
        json.dump(data, file, indent=4)

def load_user_images(username):
    data = load_user_data()
    return data.get(username, {}).get('images', [])

def save_user_images(username, images):
    data = load_user_data()
    if username not in data:
        print(f"Error: User '{username}' not found. Cannot save images.")
        return
    data[username]['images'] = images
    save_user_data(data)

def upload_image(username):
    while True:
        image_path = input("Enter image file location (or 'back' to return): ").strip()
        if image_path.lower() == 'back':
            return
        if not os.path.exists(image_path):
            print("File does not exist. Try again.")
            continue
        if not image_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            print("Only image files (.jpg, .jpeg, .png, .gif) are allowed.")
            continue
        user_images[username].append(image_path)
        save_user_images(username, user_images[username])
        print(f"Image '{image_path}' uploaded successfully!")

def delete_image(username):
    if not user_images[username]:
        print("No images to delete.")
        return

    for idx, img in enumerate(user_images[username], 1):
        print(f"{idx}. {img}")

    while True:
        choice = input("Enter image number to delete (or 'back'): ").strip()
        if choice.lower() == 'back':
            return
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(user_images[username]):
                confirm = input(f"Confirm deletion of '{user_images[username][index]}'? (yes/no): ")
                if confirm.lower() == 'yes':
                    removed = user_images[username].pop(index)
                    save_user_images(username, user_images[username])
                    print(f"Deleted: {removed}")
                else:
                    print("Cancelled.")
                return
        print("Invalid input. Try again.")

def view_images(username):
    if not user_images[username]:
        print("No images uploaded.")
        return
    for idx, img in enumerate(user_images[username], 1):
        print(f"{idx}. {img}")

    while True:
        action = input("Options: [delete], [back]: ").lower()
        if action == 'delete':
            delete_image(username)
        elif action == 'back':
            return
        else:
            print("Invalid choice.")

def display_help():
    print("""
Help:
1. Upload Image: Upload image file path (JPEG, PNG, etc.).
2. View Images: View and optionally delete uploaded images.
3. Delete Image: Delete a previously uploaded image.
4. Logout: Log out current user.
5. Exit: Close the program.
""")

def display_main_menu():
    print(r"""
--------------------------------
|         Image Manager        |
|------------------------------|
| 1. Upload Image              |
| 2. View Images               |
| 3. Delete Image              |
| 4. Help                      |
| 5. Logout                    |
| 6. Exit                      |
--------------------------------
""")

def login():
    user_data = load_user_data()
    print("Welcome! Type your username to login or type 'new' to create an account.")
    username = input("Username: ").strip()

    if username.lower() == 'new':
        create_account()
        return

    if username not in user_data:
        print("Username not found. Try again.")
        login()
        return

    password = getpass.getpass("Password: ")
    if password != user_data[username]['password']:
        print("Incorrect password.")
        login()
        return

    print(f"Welcome, {username}!")
    main_menu(username)

def create_account():
    user_data = load_user_data()
    print("Creating new account. Enter 'back' anytime to cancel.")
    while True:
        username = input("Choose username: ").strip()
        if username.lower() == 'back':
            login()
            return
        if username in user_data:
            print("Username exists. Choose another.")
            continue
        password = getpass.getpass("Choose password: ")
        confirm = getpass.getpass("Confirm password: ")
        if password != confirm:
            print("Passwords do not match.")
            continue
        user_data[username] = {'password': password, 'images': []}
        save_user_data(user_data)
        print("Account created!")
        login()
        return

def main_menu(username):
    user_images[username] = load_user_images(username)
    while True:
        display_main_menu()
        choice = input("Enter choice (1-6): ").strip()
        if choice == "1":
            upload_image(username)
        elif choice == "2":
            view_images(username)
        elif choice == "3":
            delete_image(username)
        elif choice == "4":
            display_help()
        elif choice == "5":
            print("Logging out...")
            login()
            return
        elif choice == "6":
            print("Exiting...")
            save_user_images(username, user_images[username])
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    login()
