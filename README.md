# site_analyzer

**site_analyzer** is a simple Python app designed to help you track new offers on [Kajakowo.net](https://kajakowo.net/pl/32-gielda-kajakowa) and never miss a great deal!

## 🚣‍♂️ What does it do?

- Automatically checks the Kajakowo marketplace for new kayak-related offers.
- Notifies you via email whenever new listings appear.
- Helps you stay ahead and catch special deals as soon as they are posted.

## ✉️ How does it work?

- The app scrapes the Kajakowo offers page at regular intervals.
- If new offers are found, it sends a summary email directly to your inbox.
- Email sending is powered by SendGrid for reliable delivery.

## ⚙️ Setup

1. Clone the repository.
2. Set your SendGrid API key and email addresses as environment variables:
   - `SENDGRID_API_KEY`
   - `EMAIL_SENDER`
   - `EMAIL_RECEIVER`
3. Run the app and let it watch for new deals!

## 💡 Why use it?

Whether you’re a kayak enthusiast or just looking for a bargain, **site_analyzer** makes sure you’re always up to date with the latest offers.

---

*Happy paddling and good luck hunting for deals!*
