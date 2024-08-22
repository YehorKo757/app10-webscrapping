import requests
import selectorlib


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


def send_email():
    print("Email was sent!")


def read():
    with open("data.txt", "r") as file:
        return file.read()


if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    print(extracted)
    content = read()
    if extracted.lower() != "no upcoming tours":
        if extracted not in content:
            store(extracted)
            send_email()
