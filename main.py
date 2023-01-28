import sqlite3
import time

import requests
import selectorlib

from send_email import send_email

URL = "https://programmer100.pythonanywhere.com/tours/"
connection = sqlite3.connect("data.db")


def scraper(url):
    response = requests.get(url)
    response = response.text

    return response


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def store(extracted_data):
    values = extracted_data.split(',')
    values = [item.strip() for item in values]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", values)
    connection.commit()


def read_extracted_data(extracted_data):
    values = extracted_data.split(',')
    values = [item.strip() for item in values]
    band, city, date = values
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
    rows = cursor.fetchall()
    return rows


if __name__ == "__main__":
    while True:
        source = scraper(URL)
        extracted_vals = extract(source)

        if extracted_vals != "No upcoming tours":
            row = read_extracted_data(extracted_vals)
            if not row:
                store(extracted_vals)
                send_email(extracted_vals)
        time.sleep(2)
