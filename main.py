from bs4 import BeautifulSoup
import requests
import json
import os

SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY"]
EMAIL_SENDER = os.environ["EMAIL_SENDER"]
EMAIL_RECEIVER = os.environ["EMAIL_RECEIVER"]
URL = "https://kajakowo.net/pl/32-gielda-kajakowa"

def get_offers(url: str) -> list[tuple[str, str]]:
    """Scrape offers from Kajakowo.net"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    offers: list[tuple[str, str]] = []
    for product in soup.select(".product-title a"):
        title = product.text.strip()
        link = product["href"]
        if not link.startswith("http"):
            link = "https://kajakowo.net" + link
        offers.append((title, link))
    return offers

def send_email(sender: str, api_key: str, receiver: str, new_offers: list[tuple[str, str]]) -> None:
    html = f"<h3>New offers in <a href='{URL}'>{URL}</a></h3><ul>"
    for title, link in new_offers:
        html += f"<li><a href='{link}'>{title}</a></li>"
    html += "</ul>"

    data = {
        "personalizations": [
            {"to": [{"email": receiver}]}
        ],
        "from": {"email": sender},
        "subject": "Hey! 🚣 New offers on Kajakowo.net",
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

def check_for_updates() -> None:
    print("🔍 Checking for new offers...")
    try:
        new_data = get_offers(URL)

        if os.path.exists("offers.json"):
            with open("offers.json", "r") as f:
                old_data: list[tuple[str, str]] = json.load(f)
        else:
            old_data: list[tuple[str, str]] = []

        old_titles = {title for title, _ in old_data}
        new_offers = [offer for offer in new_data if offer[0] not in old_titles]

        if new_offers:
            print(f"✨ Found {len(new_offers)} new offer(s). Sending email...")
            send_email(EMAIL_SENDER, SENDGRID_API_KEY, EMAIL_RECEIVER, new_offers)
        else:
            print("😴 No new offers found.")

        with open("offers.json", "w") as f:
            json.dump(new_data, f)

    except requests.RequestException as e:
        print(f"❌ Network error: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON error: {e}")
    except KeyError as e:
        print(f"❌ Missing environment variable: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    check_for_updates()
