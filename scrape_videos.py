import datetime
import dateutil.relativedelta
from instalooter.looters import InstaLooter, ProfileLooter
import instaloader
from instalooter.cli.login import login

# scrape_videos.py scrapes all the videos from pages we are following
def scrapeVideos(username = "",
                 password = "",
                 output_folder = "",
                 modeAM = "",
                 days = 1):
        
    print("Starting Scraping")

    L = instaloader.Instaloader()

    # Login or load session for loader
    L.login(username, password)  
    profile = instaloader.Profile.from_username(L.context, username)
    following = profile.get_followees()
    print(following)

    today = datetime.date.today()
    timeframe = (today, today - dateutil.relativedelta.relativedelta(days=days))

    for profile in following:
        acc = profile.username
        # Scrap videos from this account or not

        def scrape_videos_fn():
            looter = ProfileLooter(acc, videos_only=True, dump_json=True, template="{id}-{username}-{width}-{height}")
            if not looter.logged_in():
                looter.login(username, password)
            print("[+]Scraping From Account: " + acc)

            try:
                # videos downloaded
                numDowloaded = looter.download(output_folder, media_count=30, timeframe=timeframe)
                print("[+]Downloaded " + str(numDowloaded) + " videos successfully")
                print("")

            except Exception as e:
                # error Occcured 
                print("[+]Skipped acc " + acc + "because of")
                print(e)

        if modeAM == "M":
            scrap_or_Skip_video = input(f"[Q]Do you want to scrape from {acc}'s profile?(Y/n/q):").strip().lower()
            if scrap_or_Skip_video == "n":
                print("[+]Skiped Scraping")
                continue
            if scrap_or_Skip_video == "q":
                print("[+]Exit Scrapping Loop")
                break
            else:
                scrape_videos_fn()
        elif modeAM == "A":
            scrape_videos_fn()


if __name__ == "__main__":
    scrapeVideos(username = "chewymemes_v3",
                 password = "",
                 modeAM = "A",
                 output_folder = "./Memes_December_4")
