import psutil
import requests
import time
import json
import os
from colorama import Fore, init

def set_console_title(title):
    if os.name == 'nt':  
        os.system(f'title {title}')
    else:  
        print(f'\033]0;{title}\007', end='', flush=True)

set_console_title('Warning Skibidi')

init(autoreset=True)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Banner LoL
def print_banner():
    print(Fore.BLUE + """       
░██╗░░░░░░░██╗░█████╗░██████╗░███╗░░██╗██╗███╗░░██╗░██████╗░  ████████╗░█████╗░░█████╗░██╗░░░░░ |
░██║░░██╗░░██║██╔══██╗██╔══██╗████╗░██║██║████╗░██║██╔════╝░  ╚══██╔══╝██╔══██╗██╔══██╗██║░░░░░ |
░╚██╗████╗██╔╝███████║██████╔╝██╔██╗██║██║██╔██╗██║██║░░██╗░  ░░░██║░░░██║░░██║██║░░██║██║░░░░░ |
░░████╔═████║░██╔══██║██╔══██╗██║╚████║██║██║╚████║██║░░╚██╗  ░░░██║░░░██║░░██║██║░░██║██║░░░░░ |
░░╚██╔╝░╚██╔╝░██║░░██║██║░░██║██║░╚███║██║██║░╚███║╚██████╔╝  ░░░██║░░░╚█████╔╝╚█████╔╝███████╗ |
░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═╝╚═╝░░╚══╝░╚═════╝░  ░░░╚═╝░░░░╚════╝░░╚════╝░╚══════╝ |
                     Version : 0.0.3 -- https://discord.gg/ugphone-official                     |
-------------------------------------------------------------------------------------------------
    """)

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'warningconfig.json')
    with open(config_path, 'r') as file:
        config = json.load(file)
    return config

def check_memory_usage(memory_threshold_gb):
    threshold = memory_threshold_gb * 1024 * 1024 * 1024  
    used_memory = psutil.virtual_memory().used
    
    if used_memory > threshold:
        return True, used_memory
    return False, used_memory

def send_warning_to_discord(webhook_url, used_memory, device_name, memory_threshold_gb):
    used_memory_gb = used_memory / (1024 * 1024 * 1024)

    embed = {
        "title": f"⚠️ Memory Usage Alert on {device_name} ⚠️",
        "description": f"Memory usage is at **{used_memory_gb:.2f} GB**, exceeding the **{memory_threshold_gb} GB** limit.",
        "color": 15158332,  
        "fields": [
            {
                "name": "Threshold Exceeded",
                "value": f"Memory usage has exceeded the threshold of {memory_threshold_gb} GB."
            }
        ],
        "thumbnail": {  
            "url": "https://play-lh.googleusercontent.com/ziyYqRZxCcw_ffXMzt3RCiQmf5dg8geErhBtiPAbAAzxHV2oKPP6JHTaysRuCQ2Prw"  
        },
        "footer": {
            "text": "Powered By UGPHONE | https://discord.gg/ugphone-official"
        }
    }

    data = {
        "content": f"🚨 **High Memory Usage Detected on {device_name}!** 🚨",
        "embeds": [embed]
    }

    result = requests.post(webhook_url, json=data)

    if result.status_code == 204:
        print(f"{Fore.RED}Alert sent to Webhook successfully for {device_name}!")
    else:
        print(f"{Fore.RED}Failed to send alert for {device_name}. Status code: {result.status_code}, Response: {result.text}")

def log_memory_under_limit(device_name, used_memory):
    used_memory_gb = used_memory / (1024 * 1024 * 1024)
    print(f"{Fore.GREEN}Memory usage is under limits on {device_name} ({used_memory_gb:.2f} GB used).")

# Main function lol
def warning_tool():
    config = load_config()  
    webhook_url = config['webhook_url']
    device_name = config['device_name']
    memory_threshold_gb = config['memory_threshold_gb']
    check_interval_minutes = config['check_interval_minutes']

    while True:
        alert_triggered, used_memory = check_memory_usage(memory_threshold_gb)
        if alert_triggered:
            send_warning_to_discord(webhook_url, used_memory, device_name, memory_threshold_gb)
        else:
            log_memory_under_limit(device_name, used_memory)
        
        time.sleep(check_interval_minutes * 60)

if __name__ == "__main__": 
    try:
        clear_console()
        print_banner()
        warning_tool()  
    except KeyboardInterrupt:
        clear_console()
        print_banner()
        print(f"{Fore.LIGHTBLACK_EX}\nTool was exited.")
        exit(0)
