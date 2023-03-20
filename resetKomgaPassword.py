import sqlite3
import sys
import bcrypt


def choose_user(x_users):
    print("Select user:")
    for counter, user in enumerate(x_users):
        print(f"{counter}: {user[1]}")
    x_choice = input("User: ")
    if x_choice.isdigit() and x_choice in [str(x) for x in range(len(x_users))]:
        return int(x_choice)
    else:
        print("Invalid choice!")
        return choose_user(x_users)


def new_password():
    pw = input("Input new password: ", )
    pw2 = input("Confirm new password: ")
    if pw == pw2:
        return bcrypt.hashpw(pw.encode('UTF-8'), bcrypt.gensalt())
    else:
        print("Passwords don't match!")
        return new_password()


if __name__ == "__main__":

    if len(sys.argv) != 2 \
            or sys.argv[1] == "-h" \
            or sys.argv[1] == "--help":
        print("Usage: resetKomgaPassword.py <path to database.sqlite>", flush=True)
        sys.exit(1)

    conn = sqlite3.connect(sys.argv[1])
    c = conn.cursor()
    c.execute("SELECT ID, EMAIL, PASSWORD FROM USER")
    users = c.fetchall()

    choice = choose_user(users)
    print("Resetting password for", users[choice][1])
    c.execute("UPDATE USER SET PASSWORD = ?, LAST_MODIFIED_DATE = CURRENT_TIMESTAMP WHERE ID = ?",
              ((new_password()), users[choice][0]))

    conn.commit()
    conn.close()
    sys.exit(0)
