import subprocess
import random
import string

SKIP_USERS = ['root', 'seccdc'] # Will be changed depending on what is the name of seccdc user

def get_linux_users():
    with open("/etc/passwd", "r") as f:
        users = [line.split(":")[0] for line in f.readlines()]
    return users


def change_password(username, new_password):
    try:
        subprocess.run(['echo', f'{username}:{new_password}', '|', 'sudo', 'chpasswd'], check=True, shell=True)
        print("Password changed successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to change password:", e)


def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(characters, k=length))


passwords_file_text = ""
users = get_linux_users()
for user in users:
    if user not in SKIP_USERS:
        new_password = generate_password()
        change_password(user, new_password)
        passwords_file_text += f"{user} {new_password}\n"


print(passwords_file_text)