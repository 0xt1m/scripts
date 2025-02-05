#!/bin/bash

SKIP_USERS=("root" "seccdc")
PASSWORDS_FILE="passwords.txt"

get_linux_users() {
    awk -F: '{print $1}' /etc/passwd
}

generate_password() {
    tr -dc 'A-Za-z0-9_@#$%^&+=-~' < /dev/urandom | head -c 12
    echo
}

change_password() {
    local username=$1
    local new_password=$2
    echo "$username:$new_password" | sudo chpasswd
}

passwords_file_text=""
for user in $(get_linux_users); do
    if [[ ! " ${SKIP_USERS[@]} " =~ " ${user} " ]]; then
        new_password=$(generate_password)
        change_password $user $new_password
        passwords_file_text+="$user $new_password\n"
    fi
done

echo -e "$passwords_file_text" > "$PASSWORDS_FILE"
echo "Passwords have been saved to $PASSWORDS_FILE."