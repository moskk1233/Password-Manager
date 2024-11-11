import os
import uuid
import pyperclip
from cryptography.fernet import Fernet
from logger import logger

__PASSWORDFILENAME = "passwords.txt"
__KEYFILENAME = "key.key"

def setup() -> None:
    """Set up the password manager by generating a key and creating the password file if they do not exist."""
    logger.info("Setting up")
    
    logger.info("Looking for essential files")
    if not os.path.isfile(__KEYFILENAME):
        logger.warning(f"Don't has file name {__KEYFILENAME}")
        with open(__KEYFILENAME, "wb") as f:
            f.write(Fernet.generate_key())
        logger.info(f"{__KEYFILENAME} created")
        
    if not os.path.isfile(__PASSWORDFILENAME):
        logger.warning(f"Don't has file name {__PASSWORDFILENAME}")
        with open(__PASSWORDFILENAME, "w") as f:
            f.write("")
        logger.info(f"{__PASSWORDFILENAME} created")
    logger.info("All file done")

def load_key() -> bytes:
    try:
        with open(__KEYFILENAME, "rb") as f:
            key = f.read()
    except FileNotFoundError:
        logger.error(f"Can't find file {__KEYFILENAME}")
        raise SystemExit(1)
    except Exception as e:
        logger.error(f"Error when try to read key file: {e}")
        raise SystemExit(1)
    return key

def add_password() -> None:
    try:
        platform = input("Platform / Web: ")
        password_id = str(uuid.uuid4())
        username = input("Username: ")
        password = input("Password: ")
        with open(__PASSWORDFILENAME, "a") as f:
            f.write(password_id + '|' + platform + '|' + username + '|' + fernet.encrypt(password.encode()).decode() + '\n')
    except Exception as e:
        logger.error(f"Error when try to add password: {e}")

def view_password() -> None:
    try:
        with open(__PASSWORDFILENAME, "r") as f:
            for line in f.readlines():
                uid, platform, username, _ = line.strip().split("|")
                print(f"ID: {uid}")
                print(f'Platform / Web: {platform}')
                print(f'Username: {username}')
                print(f'Password: ******')
                print("==========================================================")
    except Exception as e:
        logger.error(f"Error when try to view password: {e}")

def copy_password():
    id_password = str(input("ID: "))
    try:
        with open(__PASSWORDFILENAME, "r") as f:
            for line in f.readlines():
                uid, platform, username, password = line.strip().split("|")
                if uid == id_password:
                    print(f'Platform / Web: {platform}')
                    print(f'Username: {username}')
                    print(f'Password: {fernet.decrypt(password.encode()).decode()}')
                    pyperclip.copy(fernet.decrypt(password.encode()).decode())
                    print('Password copied to clipboard')
                    return
            logger.error("Cannot find ID")
    except Exception as e:
        logger.error(f"Error when try to view password: {e}")

if __name__ == "__main__":
    setup()

    try:
        key = load_key()
        fernet = Fernet(key)
        logger.info("Load key success")
    except Exception as e:
        logger.error(f"Error when try to load key: {e}")
        raise SystemExit(1)

    while True:
        try:
            mode = input(
                "Would you like to add a new password or view existing password ([v]iew, [a]dd, [c]opy), or [q]uit: "
            ).lower()

            if mode == 'add' or mode == 'a':
                add_password()
            elif mode == 'view' or mode == 'v':
                view_password()
            elif mode == 'copy' or mode == 'c':
                copy_password()
            elif mode == 'quit' or mode == 'q':
                break
            else:
                logger.error("Sorry but i don't understand")
        except KeyboardInterrupt:
            print("")
            logger.error("Nah, you only can exit with q")

