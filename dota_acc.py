import requests
from bs4 import BeautifulSoup
from pyfiglet import Figlet


# dotabuff url
url = "https://www.dotabuff.com/players/"
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 "
}
account_id=""


# program title using pyfiglet
def title(text):
    preview_text = Figlet(font="slant")
    print(preview_text.renderText(text))

# separate blocks
def separation(number):
    print("-" * number)


# getting account id, adding id to url, request to url with id
def get_data(url, headers):
    global account_id
    account_id = input("Please enter Dota 2 AccountID: ").strip()
    print("\n")
    url += account_id
    req = requests.get(url, headers=headers)
    return req.text


# parsing data
def parse_data(req):
    try:
        soup = BeautifulSoup(req, "lxml")
        main_role = soup.find("div", class_="r-none-mobile").text.strip()
        main_role_coresup = soup.find("div", class_="row-12 with-sidebar player-summary").find("div",
                                                                                               class_="label").text.strip()[
                            4:]
        main_role += " " + main_role_coresup
        main_hero = soup.find("img", class_="image-hero image-icon").get("title").strip()
        main_hero_matches = soup.find("div", class_="content-inner").find("div", class_="r-fluid r-10 r-line-graph").find(
            "div", class_="r-body").text.strip()
        main_hero_winrate = soup.find("div", class_="content-inner").find("div",
                                                                          class_="r-fluid r-10 r-line-graph").findNextSibling().find(
            "div", class_="r-body").text.strip()
        return main_role, main_hero, main_hero_matches, main_hero_winrate
    except:
        print("No account data found")
        preview_text = Figlet(font="bubble")
        print(preview_text.renderText("ERROR"))
        req = requests.get(url+account_id, headers=headers)
        print(f"Response status: {req.status_code}")
        return 404

# printing result on screen
def display(info):
    separation(30)
    print(f"Main role: {info[0]}")
    separation(30)
    print(f"Main hero: {info[1]}\nMatches: {info[2]} Winrate: {info[3]}")
    separation(30)

# main function
def main():
    title("XIII")
    html_data = get_data(url, headers=headers)
    result = parse_data(html_data)
    if result != 404:
        display(result)


if __name__ == '__main__':
    main()
