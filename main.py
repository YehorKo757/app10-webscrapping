import requests
import selectorlib
import os
import smtplib, ssl
import time

URL = "http://programmer100.pythonanywhere.com/tours/"


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
    with open("data.txt", "a") as file:
        file.write(extracted + "\n")


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


def read():
    with open("data.txt", "r") as file:
        return file.read()


if __name__ == "__main__":
    while True:
        try:
            scraped = scrape(URL)
            extracted = extract(scraped)
            print(extracted)
            content = read()
            if extracted.lower() != "no upcoming tours":
                if extracted not in content:
                    store(extracted)
                    message = f"Hey, check out this new event {extracted}"
                    send_email(message)
            time.sleep(2)
        except KeyboardInterrupt:
            break
