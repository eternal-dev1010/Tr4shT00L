# pkg install python python-pip tsu libexpat openssl -y && pip install requests psutil colorama && pkg update
# cd /sdcard/download && python cookiechecker.py
import os
import requests
from colorama import Fore, init

def set_console_title(title):
    if os.name == 'nt':  
        os.system(f'title {title}')
    else:  
        print(f'\033]0;{title}\007', end='', flush=True)

# Set console title
set_console_title('Cookie Checker')

init(autoreset=True)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def press_enter_to_continue():
    input(f"{Fore.LIGHTBLUE_EX}\nPress Enter to continue...")
    clear_console()

def print_banner():
    print(Fore.LIGHTBLACK_EX + """
░█████╗░░█████╗░░█████╗░██╗░░██╗██╗███████╗  ░█████╗░██╗░░██╗███████╗░█████╗░██╗░░██╗███████╗██████╗░ |
██╔══██╗██╔══██╗██╔══██╗██║░██╔╝██║██╔════╝  ██╔══██╗██║░░██║██╔════╝██╔══██╗██║░██╔╝██╔════╝██╔══██╗ |
██║░░╚═╝██║░░██║██║░░██║█████═╝░██║█████╗░░  ██║░░╚═╝███████║█████╗░░██║░░╚═╝█████═╝░█████╗░░██████╔╝ |
██║░░██╗██║░░██║██║░░██║██╔═██╗░██║██╔══╝░░  ██║░░██╗██╔══██║██╔══╝░░██║░░██╗██╔═██╗░██╔══╝░░██╔══██╗ |
╚█████╔╝╚█████╔╝╚█████╔╝██║░╚██╗██║███████╗  ╚█████╔╝██║░░██║███████╗╚█████╔╝██║░╚██╗███████╗██║░░██║ |
░╚════╝░░╚════╝░░╚════╝░╚═╝░░╚═╝╚═╝╚══════╝  ░╚════╝░╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝ |
                     Version : 0.0.2 -- https://discord.gg/ugphone-official                           |
-------------------------------------------------------------------------------------------------------
    """)

def check_cookie_validity(cookie):
    url = "https://users.roblox.com/v1/users/authenticated"
    headers = {
        "Cookie": f".ROBLOSECURITY={cookie}",
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print(f"{Fore.GREEN}Cookie is alive!")
        user_data = response.json()
        print(f"Logged in as: {user_data['name']} (User ID: {user_data['id']})")
        return True
    elif response.status_code == 401:
        print(f"{Fore.RED}Cookie is dead or invalid!")
        return False
    else:
        print(f"{Fore.YELLOW}Unexpected response. Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def check_cookies_from_file(file_path):
    folder_name = "Cookies Checked"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    live_file_path = os.path.join(folder_name, 'live.txt')
    dead_file_path = os.path.join(folder_name, 'dead.txt')
    
    if not os.path.exists(file_path):
        print(f"{Fore.YELLOW}File {file_path} doesn't exist. Creating one...")
        with open(file_path, 'w') as file:
            file.write("") 
        print(f"{Fore.GREEN}Created {file_path}. Add cookies in it with 'username:password:cookie' format and try again!")
        return
    
    with open(file_path, 'r') as file:
        credentials = file.readlines()

    open(live_file_path, 'w').close()  # Clear live.txt
    open(dead_file_path, 'w').close()  # Clear dead.txt
    
    total_cookies = len(credentials)
    live_cookies = 0
    dead_cookies = 0
    
    for idx, cred in enumerate(credentials, 1):
        cred = cred.strip()
        if cred.count(":") >= 2:  
            parts = cred.split(":")
            username = parts[0]
            password = parts[1]
            cookie = ":".join(parts[2:])  
            
            print(f"Checking cookie {idx} for {username}...")
            
            if check_cookie_validity(cookie):  
                live_cookies += 1
                with open(live_file_path, 'a') as live_file:
                    live_file.write(f"{username}:{password}:{cookie}\n")
            else:  
                dead_cookies += 1
                with open(dead_file_path, 'a') as dead_file:
                    dead_file.write(f"{username}:{password}:{cookie}\n")
        else:
            print(f"{Fore.RED}Invalid format in line {idx}. Expected format 'username:password:cookie'.")
    
    print(f"--------------------------------------------------")
    print(f"\n{Fore.CYAN}Total Cookies: {total_cookies}")
    print(f"{Fore.GREEN}Live Cookies: {live_cookies}")
    print(f"{Fore.RED}Dead Cookies: {dead_cookies}")

def main_menu():
    clear_console()
    print_banner()
    while True:
        print(Fore.LIGHTBLUE_EX + "\nRoblox Cookie Checker Menu :")
        print("1. Start Check Cookie Process (username:password:cookie)")
        print("2. Exit")
        
        choice = input("Select an option : ")
        
        if choice == "1":
            check_cookies_from_file('cookies.txt')
            press_enter_to_continue()
            print_banner() 
            
        elif choice == "2":
            clear_console()
            print_banner()  
            print(f"{Fore.LIGHTBLACK_EX}Tool was exited.")
            break
        else:
            print(f"{Fore.RED}Invalid option | Please try again !")
            press_enter_to_continue()
            clear_console()
            print_banner()

if __name__ == "__main__":
    try:
        main_menu()  
    except KeyboardInterrupt:
        clear_console()
        print_banner()
        print(f"{Fore.LIGHTBLACK_EX}\nTool was exited.")
        exit(0)
