import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By

def access_site(driver, website):
    driver.get(website)
    title = str(driver.title)
    return title


def scrape_odds(driver):
    rivalry_odds = []
    bet_content = driver.find_elements(By.XPATH, "//div[contains(@class, 'betline m-auto')]//div[@class='betline-competitors betline-matchup']")

    for row in bet_content:
        match_detail = row.text.replace("\n", ",").split(',')
        del match_detail[2]
        rivalry_odds.append(match_detail)

    return rivalry_odds


def store_odds(team_odds):
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 10)
    pd.set_option('display.width', 500)

    df_rivalry_odds = pd.DataFrame(team_odds, columns=['home', 'odds', 'away', 'odds'])
    print(df_rivalry_odds)


def main():
    driver = webdriver.Chrome()
    website = "https://www.rivalry.com/sports/popular/basketball-betting"
    access_site(driver, website)
    rivalry_odds = scrape_odds(driver)
    store_odds(rivalry_odds)
    driver.close()

if __name__ == '__main__':
    main()