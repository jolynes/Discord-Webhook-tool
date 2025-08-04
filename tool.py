import requests
import time
import os

def display_centered_banner():
    banner = f"""
    ____     _     _   ____  
    /    )   /|   /    /    )
---/____/---/-| -/----/___ /-
  /        /  | /    /    |  
_/________/___|/____/_____|__
"""
    try:
        cols = os.get_terminal_size().columns
    except:
        cols = 80
    
    print("\n" + "="*cols + "\n")
    for line in banner.split('\n'):
        print(line.center(cols))
    print("\n" + "="*cols + "\n")

def send_webhook_message(url, content):
    data = {"content": content}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")
        return False

def delete_webhook(url):
    try:
        response = requests.delete(url)
        response.raise_for_status()
        print("\nWebhook deleted successfully.")
    except requests.exceptions.RequestException as e:
        print(f"\nX Failed to delete webhook: {e}")

def main():
    display_centered_banner()
    
    webhook_url = input("1. Please enter your Discord Webhook URL: ").strip()
    initial_text = input("2. Please enter the text you want to send: ").strip()
    
    try:
        message_count = int(input("3. Please enter how many messages do you want to send: "))
    except ValueError:
        print("Invalid number. Please enter a valid integer.")
        return
    
    valid_prefixes = (
        'https://discord.com/api/webhooks/',
        'https://canary.discord.com/api/webhooks/',
        'https://discordapp.com/api/webhooks/'
    )
    
    if not any(webhook_url.startswith(prefix) for prefix in valid_prefixes):
        print("Invalid Discord webhook URL. It should start with one of the following:")
        print("  - https://discord.com/api/webhooks/")
        print("  - https://canary.discord.com/api/webhooks/")
        print("  - https://discordapp.com/api/webhooks/")
        return
    
    if message_count <= 0:
        print("Message count must be greater than 0.")
        return

    print(f"\nSending {message_count} messages...")
    
    success_count = 0
    for i in range(message_count):
        if send_webhook_message(webhook_url, initial_text):
            success_count += 1
            print(f"Sent message {i+1}")
        else:
            print(f"X Failed to send message {i+1}")
        if i < message_count - 1:
            time.sleep(1)
    
    print(f"\nDone! Sent {success_count}/{message_count} messages successfully.")

    while True:
        delete_choice = input("4. Do you want to delete the webhook? [y/n]: ").strip().lower()
        if delete_choice == 'y':
            delete_webhook(webhook_url)
            break
        elif delete_choice == 'n':
            print("Webhook was not deleted.")
            break
        else:
            print("Please enter 'y' or 'n'.")
    
if __name__ == "__main__":
    main()