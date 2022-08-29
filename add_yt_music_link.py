from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import datetime
import pandas as pd
from send_telegram_message import send_message


def find_link_and_combine(PATH ="data/songsDataset.csv", max_iter = 100):
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

                    penyanyi = driver.find_element(By.XPATH, '//*[@id="contents"]/ytmusic-responsive-list-item-renderer/div[2]/div[3]/yt-formatted-string/a[1]')

                    if (judul.text.lower() == lagu.lower()) and (penyanyi.text.lower() == artis.lower()):

                        url = judul.get_attribute("href")
                        link_found += 1
                    else:
                        url = "link not found"
                        link_not_found += 1
                    currentime = datetime.datetime.now()
                    mixed = currentime.strftime('%H:%M:%S')
                    textt = f"[{mixed}]"
                    print(f"{textt} link: {url}")
                    songs_data_set["ytMusic_URL"].mask((songs_data_set["artists"] == artis) & (songs_data_set["title"] == lagu), url, inplace=True)
                    songs_data_set.to_csv(PATH, index=False)
                    break
                except:
                    hitung += 1
            iter_count += 1
        count += 1
    
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
    send_message(f"{mixed} - data updated successfully!")

if __name__ == "__main__":
    find_link_and_combine("data/songsDataset.csv")