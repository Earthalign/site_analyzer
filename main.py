from bs4 import BeautifulSoup

import requests
import json
import schedule
import time
import os


def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def get_offers(url):
    """Scrape offers from Kajakowo.net"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    offers = []
    for product in soup.select(".product-title a"):
        title = product.text.strip()
        link = product["href"]
        if not link.startswith("http"):
            link = "https://kajakowo.net" + link
        offers.append((title, link))
    return offers

def send_email(sender, api_key, receiver, new_offers):
    html = "<h3>New offers:</h3><ul>"
    for title, link in new_offers:
        html += f"<li><a href='{link}'>{title}</a></li>"
    html += "</ul>"

    data = {
        "personalizations": [
            {"to": [{"email": receiver}]}
        ],
        "from": {"email": sender},
        "subject": "Hey! There is 🚣 New offers on Kajakowo.net",
        "content": [{"type": "text/html", "value": html}]
    }

    response = requests.post(
        "https://api.sendgrid.com/v3/mail/send",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json=data
    )

    if response.status_code == 202:
        print("📧 Email sent successfully.")
    else:
        print(f"❌ SendGrid error: {response.status_code} {response.text}")

def check_for_updates():
    config = load_config()
    url = config["url"]
    api_key = os.getenv("SENDGRID_API_KEY", config.get("sendgrid_api_key", ""))
    sender = config["email_sender"]
    receiver = config["email_receiver"]

    print("🔍 Checking for new offers...")
    try:
        new_data = get_offers(url)

        if os.path.exists("offers.json"):
            with open("offers.json", "r") as f:
                old_data = json.load(f)
        else:
            old_data = []

        old_titles = {title for title, _ in old_data}
        new_offers = [offer for offer in new_data if offer[0] not in old_titles]

        if new_offers:
            print(f"✨ Found {len(new_offers)} new offer(s). Sending email...")
            send_email(sender, api_key, receiver, new_offers)
        else:
            print("😴 No new offers found.")

        with open("offers.json", "w") as f:
            json.dump(new_data, f)

    except Exception as e:
        print("❌ Error:", e)

def main():
    config = load_config()
    interval = config.get("check_interval_minutes", 10)
    schedule.every(interval).minutes.do(check_for_updates)

    print(f"🚀 Monitor started. Checking every {interval} minutes...")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
