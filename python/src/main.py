import sys
from user import User
import my_utils as my_utils
import registrator
from pathlib import Path

def main():
    if len(sys.argv) < 3:
        print("Usage: python client_old.py <username> <action>")
        print("  actions: generate-keys | register | login | write | test | exit")
        sys.exit(1)
    username = sys.argv[1]
    action = sys.argv[2]
    user=None
    while True:
        if action == "generate-keys":
            priv_pem, pub_pem = my_utils.generate_rsa_keypair()
            my_utils.save_keys(Path(username),priv_pem, pub_pem)
            print("[+] RSA key pair generated and saved")
        elif action == "register":
            reg=registrator.registrator()
            reg.register_user(username)
        elif action == 'load':
            user=User(username)
            
        elif action == 'exit':
            break
        action = input("Next action:")

    return

if __name__ == "__main__":
    main()