import requests
import selectorlib

URL = "https://programmer100.pythonanywhere.com/tours/"


def scraper(url):
    response = requests.get(url)
    response = response.text

    return response


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email():
    print("Email was sent!")


def store(extracted_data):
    with open("data.txt", 'a') as file:
        file.write(extracted_data + "\n")


def read_extracted_data():
    with open("data.txt", 'r') as file:
        return file.read()


if __name__ == "__main__":
    source = scraper(URL)
    extracted_vals = extract(source)

    content = read_extracted_data()
    if extracted_vals != "No upcoming tours":
        if extracted_vals not in content:
            store(extracted_vals)
            send_email()
