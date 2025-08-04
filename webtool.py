import requests
import time
import os

# ANSI color codes
BLUE = "\033[94m"
RESET = "\033[0m"

def display_centered_banner():
    banner = f"""{BLUE}
    ____     _     _   ____  
    /    )   /|   /    /    )
---/____/---/-| -/----/___ /-
  /        /  | /    /    |  
_/________/___|/____/_____|__
{RESET}"""
    try:
        cols = os.get_terminal_size().columns
    except:
        cols = 80
    
    print("\n" + "="*cols + "\n")
    for line in banner.split('\n'):
        print(line.center(cols))
    print("\n" + "="*cols + "\n")

def send_webhook_message(url, content):
    data = {
        "content": content
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"{BLUE}Error sending message: {e}{RESET}")
        return False

def main():
    display_centered_banner()
    
    webhook_url = input(f"{BLUE}1. Please enter your Discord Webhook URL: {RESET}").strip()
    initial_text = input(f"{BLUE}2. Please enter the text you want to send: {RESET}").strip()
    
    try:
        message_count = int(input(f"{BLUE}3. Please enter how many messages do you want to send: {RESET}"))
    except ValueError:
        print(f"{BLUE}Invalid number. Please enter a valid integer.{RESET}")
        return
    
    # Validate URL
    valid_prefixes = (
        'https://discord.com/api/webhooks/',
        'https://canary.discord.com/api/webhooks/',
        'https://discordapp.com/api/webhooks/'
    )
    
    if not any(webhook_url.startswith(prefix) for prefix in valid_prefixes):
        print(f"{BLUE}Invalid Discord webhook URL. It should start with:{RESET}")
        print(f"{BLUE}'https://discord.com/api/webhooks/' or 'https://discordapp.com/api/webhooks/'{RESET}")
        return
    
    if message_count <= 0:
        print(f"{BLUE}Message count must be greater than 0.{RESET}")
        return
    
    print(f"{BLUE}\nSending {message_count} messages...{RESET}")
    
    success_count = 0
    for i in range(message_count):
        if send_webhook_message(webhook_url, initial_text):
            success_count += 1
            print(f"{BLUE}✓ Sent message {i+1}{RESET}")
        else:
            print(f"{BLUE}✗ Failed to send message {i+1}{RESET}")
        
        if i < message_count - 1:
            time.sleep(1)
    
    print(f"{BLUE}\nDone! Sent {success_count}/{message_count} messages successfully.{RESET}")

if __name__ == "__main__":
    main()