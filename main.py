import requests
import selectorlib
import os
import smtplib, ssl
import time
import sqlite3

URL = "http://programmer100.pythonanywhere.com/tours/"

connection = sqlite3.connect("data.db")

def scrape(url):
    """
    Scrape the page source from the URL
    """
    response = requests.get(url)
    text = response.text
    return text


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "yehor.kosiachkin@gmail.com"
    password = os.getenv("PASSWORD")
    receiver = "yehor.kosiachkin@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)
    print("Email was sent!")


def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
    rows = cursor.fetchall()
    return rows

if __name__ == "__main__":
    while True:
        try:
            scraped = scrape(URL)
            extracted = extract(scraped)
            print(extracted)
            if extracted.lower() != "no upcoming tours":
                row = read(extracted)
                if not row:
                    store(extracted)
                    message = f"Hey, check out this new event {extracted}"
                    send_email(message)
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM events")
            db = cursor.fetchall()
            print(db)
            time.sleep(2)
        except KeyboardInterrupt:
            break
