import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv



load_dotenv()  

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "PUT_YOUR_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "PUT_YOUR_CHAT_ID_HERE")
TARGET_URL = os.getenv("TARGET_URL")
CUST_NUMBER = os.getenv("CUST_NUMBER")

#Precise XPath inside #con_info_div
VALUE_XPATH = '//*[@id="con_info_div"]/div/div/div/form/div[6]/div[2]/input'


def make_driver_headless():
    opts = webdriver.ChromeOptions()
    # Headless & server-friendly flags
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,900")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    
    # If Actions provides CHROME_BIN, use it
    chrome_bin = os.getenv("CHROME_BIN")
    if chrome_bin:
        opts.binary_location = chrome_bin

    driver = webdriver.Chrome(options=opts)
    return driver


def send_telegram_message(text: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID or "PUT_YOUR_" in TELEGRAM_BOT_TOKEN:
        print("Telegram credentials missing. Message not sent.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        r = requests.post(url, data=payload, timeout=15)
        r.raise_for_status()
        print("Telegram: message sent.")
    except requests.RequestException as e:
        print("Telegram send failed:", e)


def main():
    driver = make_driver_headless()
    wait = WebDriverWait(driver, 25)

    try:
        driver.get(TARGET_URL)

        # Fill customer number
        cust_input = wait.until(EC.presence_of_element_located((By.ID, "cust_no")))
        cust_input.clear()
        cust_input.send_keys(CUST_NUMBER)

        # Click submit
        submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "recharge_hist_button")))
        submit_btn.click()

        # Wait for results container
        wait.until(EC.visibility_of_element_located((By.ID, "con_info_div")))

        # Extract the specific disabled input value with the full XPath
        value_input = wait.until(EC.presence_of_element_located((By.XPATH, VALUE_XPATH)))
        raw_value = value_input.get_attribute("value") or ""
        value = raw_value.strip()

        print("Scraped value:", value)

        # Send to Telegram
        msg = (
            f"<b>অবশিষ্ট ব্যালেন্স (টাকা)</b>\n"
            f"Customer: <code>{CUST_NUMBER}</code>\n"
            f"Value: <b>{value}</b>"
        )
        send_telegram_message(msg)

    except Exception as e:
        err = f"❌ Error for customer {CUST_NUMBER}: {e}"
        print(err)
        send_telegram_message(err)
    finally:
        time.sleep(1)
        driver.quit()


if __name__ == "__main__":
    main()
