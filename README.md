# 🔄 Latest Nesco Balance Scraper (Selenium + Telegram Bot)

This project automatically checks customer balance from nesco website using **Python + Selenium**, then sends the result to a **Telegram chat** every day at **10:30 AM (Asia/Dhaka)** via **GitHub Actions**.

---

## 🚀 Features

- 🕵️ **Headless Selenium** — runs Chrome invisibly in the cloud.
- ⏰ **Automated Daily Schedule** — runs daily at 10:30 AM (Asia/Dhaka).
- 📩 **Telegram Alerts** — sends success or error messages directly to your Telegram.
- 🔐 **Secrets-based Config** — no credentials stored in code.
- ☁️ **Fully Hosted** — executes daily on GitHub Actions, no external server needed.
- 💾 **Lightweight & Reliable** — ideal for small automation tasks.

---

## 🧩 How It Works

1. The workflow opens the target nesco webpage.
2. It fills the customer number field:
   ```html
   <input type="text" id="cust_no" name="cust_no" />
   ```
3. It clicks the “রিচার্জ হিস্ট্রি” button:
   ```html
   <input type="submit" id="recharge_hist_button" />
   ```
4. Once the result section (`#con_info_div`) appears, the script extracts the target input value using this XPath:
   ```xpath
   //*[@id="con_info_div"]/div/div/div/form/div[6]/div[2]/input
   ```
5. The scraped value (e.g., `836.087`) is sent to your Telegram bot chat.
6. The job runs automatically every day at the scheduled time or can be triggered manually.

---

## 🗂️ Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── balance.yml       # GitHub Actions workflow file
├── balance_prod.py           # Main Selenium + Telegram script
├── requirements.txt          # Python dependencies
└── README.md
```

---

## ⚙️ Setup Guide

### 1️⃣ Fork or clone this repository

```bash
git clone https://github.com/hhs98/nesco-remaining-balance.git
cd nesco-remaining-balance
```

---

### 2️⃣ Add GitHub Secrets

Go to your repository → **Settings → Secrets and variables → Actions → New repository secret**  
Add these:

| Secret Name          | Description                                                                     |
| -------------------- | ------------------------------------------------------------------------------- |
| `TELEGRAM_BOT_TOKEN` | Token from [@BotFather](https://t.me/BotFather)                                 |
| `TELEGRAM_CHAT_ID`   | Your Telegram chat ID (use [@userinfobot](https://t.me/userinfobot) to find it) |
| `TARGET_URL`         | The recharge page URL                                                           |
| `CUST_NUMBER`        | Your customer number                                                            |

---

### 3️⃣ Configure the schedule (optional)

In `.github/workflows/balance.yml`, the default schedule is:

```yaml
on:
  schedule:
    # Runs daily at 10:30 Asia/Dhaka = 04:30 UTC
    - cron: "30 4 * * *"
  workflow_dispatch: {} # allows manual run
```

You can change the time using [crontab.guru](https://crontab.guru).

---

### 4️⃣ Manual Run

To test it immediately:

- Go to the **Actions** tab in your repo.
- Select **Daily Recharge Scrape**.
- Click **Run workflow**.

---

## 📤 Telegram Output Example

**Successful message:**

```
অবশিষ্ট ব্যালেন্স (টাকা)
Customer: 12345678
Value: 836.087
```

**Error message:**

```
❌ Error for customer 12345678: Timeout waiting for con_info_div
```

---

## 🧰 Dependencies

| Package         | Purpose                                      |
| --------------- | -------------------------------------------- |
| `selenium`      | Automates the browser actions                |
| `requests`      | Sends messages to Telegram                   |
| `python-dotenv` | Loads environment variables (for local runs) |

Install locally (optional testing):

```bash
pip install -r requirements.txt
```

---

## ⚙️ Workflow Overview

The GitHub Action (`balance.yml`) performs these steps:

1. **Checkout** the repo.
2. **Set up Python** 3.11.
3. **Install Chrome** using the official `browser-actions/setup-chrome`.
4. **Install dependencies** from `requirements.txt`.
5. **Run `balance_prod.py`** with your secret environment variables.
6. **Send the result** to Telegram automatically.

---

## 🧾 License

This project is licensed under the **MIT License** — free to use, modify, and share.

---

## ❤️ Credits

Built with 💻, ☕, and a bit of ❤️ by **angrywolf)**.  
Keeping your daily balance checks automated like a pro 🚀
