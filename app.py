from flask import Flask, render_template
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

stocks = [ "AAPL", "MSFT", "NVDA", "GOOGL", "META", "ORCL", "INTC", "CRM", "RGTI", "ADBE", "AMD",
    "TSLA", "ASML", "TXN", "AVGO", "QCOM", "INTU", "ADSK", "MU", "WDAY", "NOW",
    "JNJ", "PFE", "MRK", "ABT", "LLY", "BMY", "AMGN", "GILD", "REGN", "CVS",
    "XOM", "CVX", "COP", "SLB", "PSX", "EOG", "VLO", "BKR", "MPC", "HES",
    "JPM", "BAC", "WFC", "C", "GS", "MS", "AXP", "BK", "TFC", "USB", "CCEP", "KO",
    "CAT", "MMM", "GE", "DE", "EMR", "HON", "BA", "LMT", "NOC", "RTX"
]

def get_stock_data(ticker):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(ChromeDriverManager().install())  # Elimina options si no es necesario


    try:
        url = f"https://www.cnbc.com/quotes/{ticker}"
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".QuoteStrip-lastPrice")))

        price = driver.find_element(By.CSS_SELECTOR, ".QuoteStrip-lastPrice").text.strip()

        try:
            change_element = driver.find_element(By.CSS_SELECTOR, ".QuoteStrip-changeUp")
        except:
            change_element = driver.find_element(By.CSS_SELECTOR, ".QuoteStrip-changeDown")
        change_parts = change_element.text.strip().split()
        change_price, change_percent = change_parts if len(change_parts) == 2 else (change_parts[0], "N/A")

        try:
            volume = driver.find_element(By.CSS_SELECTOR, ".QuoteStrip-volume").text.strip()
        except:
            volume = "N/A"

        try:
            week_range_text = driver.find_element(By.CSS_SELECTOR, ".QuoteStrip-fiftyTwoWeekRange").text.strip()
        except:
            week_range_text = "N/A"

        try:
            pe_ratio = driver.find_element(By.CSS_SELECTOR, "#MainContentContainer li:nth-child(2) > span.Summary-value").text.strip()
        except:
            pe_ratio = "N/A"

        return {
            "ticker": ticker,
            "price": price,
            "change_price": change_price,
            "change_percent": change_percent,
            "volume": volume,
            "week_range": week_range_text,
            "pe_ratio": pe_ratio
        }

    except:
        return {"ticker": ticker, "error": True}
    finally:
        driver.quit()

@app.route("/")
def home():
    stock_data = [get_stock_data(t) for t in stocks[:10]]  # Solo 10 para que cargue rápido
    return render_template("index.html", stocks=stock_data)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
