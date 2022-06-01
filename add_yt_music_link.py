from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import datetime
import pandas as pd


def find_link_and_combine(PATH, max_iter = 100):
    print("=" * 10+ " INFO " + "="*10)
    print(f"this program will do {max_iter} iters to prevent dataset problem")
    print("you need to restart the program when it stops running")
    print("do not exit the program while it is running")
    print("happy waiting")
    print("="*26)
    options = Options()
    options.add_argument("--headless")
    options.add_argument('--log-level=3')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(options=options)

    # ytMusicURL = []

    cek = pd.read_csv(PATH)
    total_len = len(cek)
    if "ytMusic_URL" not in cek:
        yt_url = ["belum"] * total_len
        new_data_set = pd.DataFrame({
            "artists": cek["artists"],
            "title": cek["title"],
            "year_release": cek["year_release"],
            "ytMusic_URL": yt_url
        })
        new_data_set.to_csv(PATH)

    songs_data_set = pd.read_csv(PATH)
    total = len(songs_data_set)

    count, iter_count = 1, 0
    link_found, link_not_found = 0,0
    for q in songs_data_set.index:
        if iter_count == max_iter:
            break
        artis = songs_data_set["artists"][q]
        lagu = songs_data_set["title"][q]
        query = artis + " " + lagu
        if songs_data_set["ytMusic_URL"][q] == "belum":
            currentime = datetime.datetime.now()
            mixed = currentime.strftime('%H:%M:%S')
            text = f"[{mixed}]"
            print(f"{text} {query} ({count}/{total})")
            url = f"https://music.youtube.com/search?q={query}"
            driver.get(url)
            # time.sleep(2)

            # x = wait_element()
            # driver.get_screenshot_as_file("aaaaaaaaaaaaaaa.png")

            hitung = 0
            while True:
                if hitung > 500:
                    currentime = datetime.datetime.now()
                    mixed = currentime.strftime('%H:%M:%S')
                    textt = f"[{mixed}]"
                    print(f"{textt} link: {url}")
                    songs_data_set["ytMusic_URL"].mask((songs_data_set["artists"] == artis) & (songs_data_set["title"] == lagu), url, inplace=True)
                    songs_data_set.to_csv(PATH, index=False)
                    break
                try:
                    judul = driver.find_element(By.XPATH, '//*[@id="contents"]/ytmusic-responsive-list-item-renderer/div[2]/div[1]/yt-formatted-string/a')
                    # print(judul.text)

                    penyanyi = driver.find_element(By.XPATH, '//*[@id="contents"]/ytmusic-responsive-list-item-renderer/div[2]/div[3]/yt-formatted-string/a[1]')
                    # print(penyanyi.text)
                    # print(songs_data_set["title"][q].lower())

                    if (judul.text.lower() == lagu.lower()) and (penyanyi.text.lower() == artis.lower()):
                        # judul.click()
                        # url = driver.current_url
                        url = judul.get_attribute("href")
                        link_found += 1
                        # print(driver.current_url)
                    else:
                        # print("link not found")
                        url = "link not found"
                        link_not_found += 1
                    currentime = datetime.datetime.now()
                    mixed = currentime.strftime('%H:%M:%S')
                    textt = f"[{mixed}]"
                    print(f"{textt} link: {url}")
                    songs_data_set["ytMusic_URL"].mask((songs_data_set["artists"] == artis) & (songs_data_set["title"] == lagu), url, inplace=True)
                    songs_data_set.to_csv(PATH, index=False)
                    # ytMusicURL.append(url)
                    break
                except:
                    hitung += 1
            iter_count += 1
        # else:
        #     currentime = datetime.datetime.now()
        #     mixed = currentime.strftime('%H:%M:%S')
        #     text_else = f"[{mixed}]"
        #     print(f"{text_else} {query} (PASSED) ({count}/{total})")
        count += 1
    
    # new_data_set = pd.DataFrame({
    #     "artists": songs_data_set["artists"],
    #     "title": songs_data_set["title"],
    #     "year_release": songs_data_set["year_release"],
    #     "ytMusic_URL": ytMusicURL
    # })
    # new_data_set.to_csv(PATH)
    currentime = datetime.datetime.now()
    mixed = currentime.strftime('%H:%M:%S')
    fnf = f"[{mixed}]"
    print(f"{fnf} link found: {link_found}, link not found: {link_not_found}")
    print(f"{fnf} total: {link_found+link_not_found}")

    currentime = datetime.datetime.now()
    mixed = currentime.strftime('%H:%M:%S')
    sukses = f"[{mixed}]"
    print(f"{sukses} Program finished. please check {PATH}")
    driver.quit()

if __name__ == "__main__":
    find_link_and_combine("data/songsDataset.csv")