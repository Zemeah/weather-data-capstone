# Capstone Project - Weather Web Scraping

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import time

# Load webpage

url = "https://www.timeanddate.com/weather/"

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

driver.get(url)

time.sleep(5)

# ----------------------------------------
# Scrape weather data
# ----------------------------------------

rows = driver.find_elements(
    By.XPATH,
    "//table[contains(@class,'zebra')]//tr"
)

weather_data = []

for row in rows[1:]:  # Skip header row

    cells = row.find_elements(By.TAG_NAME, "td")

    for i in range(0, len(cells), 4):

        try:
            city = cells[i].text.strip()
            local_time = cells[i + 1].text.strip()
            temperature = cells[i + 3].text.strip()

            if city:
                weather_data.append(
                    {
                        "City": city,
                        "Local Time": local_time,
                        "Temperature": temperature
                    }
                )

        except IndexError:
            continue

driver.quit()

# ----------------------------------------
# Create DataFrame
# ----------------------------------------

df = pd.DataFrame(weather_data)

print("Before cleaning:")
print(weather_data[:5])

# ----------------------------------------
# Data Cleaning
# ----------------------------------------

df["City"] = df["City"].str.replace("*", "", regex=False)

df["Temperature"] = (
    df["Temperature"]
    .str.replace("°F", "", regex=False)
    .str.replace("F", "", regex=False)
    .str.strip()
)

df["Temperature"] = pd.to_numeric(df["Temperature"])

df = df.drop_duplicates()
df = df.dropna()

# Sort alphabetically

df = df.sort_values(by="City").reset_index(drop=True)

print("After cleaning:")
print(df.shape)

print(df.head())

# ----------------------------------------
# Save CSV
# ----------------------------------------

df.to_csv("cleaned_weather.csv", index=False)