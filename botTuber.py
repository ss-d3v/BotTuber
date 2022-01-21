from scrape_videos import scrapeVideos
from make_compilation import makeCompilation
from upload_ytvid import uploadYtvid
import schedule
import time
import datetime
import os
import shutil
import googleapiclient.errors
from googleapiclient.discovery import build #pip install google-api-python-client
from google_auth_oauthlib.flow import InstalledAppFlow #pip install google-auth-oauthlib
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import config
import json
import sys


print("""
▒█▀▀█ █▀▀█ ▀▀█▀▀ ▀▀█▀▀ █░░█ █▀▀▄ █▀▀ █▀▀█ 
▒█▀▀▄ █░░█ ░░█░░ ░▒█░░ █░░█ █▀▀▄ █▀▀ █▄▄▀ 
▒█▄▄█ ▀▀▀▀ ░░▀░░ ░▒█░░ ░▀▀▀ ▀▀▀░ ▀▀▀ ▀░▀▀
🄵🅄🄻🄻 🅈🄾🅄🅃🅄🄱🄴 🄲🄷🄰🄽🄽🄴🄻 🄰🅄🅃🄾🄼🄰🅃🄸🄾🄽 🅂🅄🄸🅃🄴

YouTube Channel - https://youtube.com/c/pwnos
GitHub - https://github.com/sam5epi0l/BotTuber
LinkedIn - https://linkedin.com/in/sam-sepi0l/
Twitter - https://twitter.com/sam5epi0l
Quora - https://pwnos.quora.com/
Patreon - https://www.patreon.com/pwnOS
""")

if sys.argv[-1].upper() == "-A":
  mode = "A"
elif sys.argv[-1].upper() == "-I":
  mode = input("[Q] Automated or Manual A/M:").upper()
elif sys.argv[-1].upper() == "-M":
  mode = "M"
else:
  print("""
  Code to run a fully automated youtube that can scrape content, edit a compilation, and upload to youtube daily. \

  Quick Start
  git clone https://github.com/sam5epi0l/BotTuber.git
  cd BotTuber
  # add instagram credentials in config.py
  # add YouTube API v3 credentials to googleAPI.json (check instructions)
  pip3 install -r requirements.txt
  python3 botTuber.py

  USAGE: python3 botTuber.py [OPTIONS]
  
  OPTIONS -
  python3 botTuber.py -i Interactive Mode
  python3 botTuber.py -a Full Automation
  python3 botTuber.py -m Manual Mode
  python3 botTuber.py -h Help Menu
  """)
  exit()

os.system("touch description.txt") #make description file
num_to_month = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "June",
    7: "July",
    8: "Aug",
    9: "Sept",
    10: "Oct",
    11: "Nov",
    12: "Dec"
} 
now = datetime.datetime.now()

# USER VARIABLES FILL THESE OUT (fill out username and password in config.py)

IG_USERNAME = config.IG_USERNAME
IG_PASSWORD = config.IG_PASSWORD
print("[i] ", IG_USERNAME)
print("[i] ", IG_PASSWORD)

# Commit - Automating Title with HashTags
if mode == "M":
    title = input("[Q] Type video title in 100 C or leave Blank to Use Default Title:").strip()
    description = input("[Q] Type video description headers or leave blank to use Default Headers:").strip()
    tags = input("[Q] Add some tags to default tag list or use default tags:").strip()
    if title == "":
        title = "TRY NOT TO LAUGH | BEST Dank video #memes #" + str(now.day)
elif mode == "A":
    title = "TRY NOT TO LAUGH | BEST Dank video #memes #" + str(now.day)
    description = ""
    tags = ""

videoDirectory = "./DankMemes_" + num_to_month[now.month].upper() + "_" + str(now.year) + "_V" + str(now.day) + "/"
outputFile = "./" + num_to_month[now.month].upper() + "_" + str(now.year) + "_v" + str(now.day) + ".mp4"

INTRO_VID = '' # SET AS '' IF YOU DONT HAVE ONE
OUTRO_VID = ''
TOTAL_VID_LENGTH = 13*60
MAX_CLIP_LENGTH = 19
MIN_CLIP_LENGTH = 5
DAILY_SCHEDULED_TIME = "20:00"
TOKEN_NAME = "token.json" # Don't change

# Setup Google 
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
client_secrets_file = "googleAPI.json"

def routine(title, description, tags):

    # Handle GoogleAPI oauthStuff
    print("[+] Handling GoogleAPI")
    creds = None
    # The file token1.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_NAME):
        creds = Credentials.from_authorized_user_file(TOKEN_NAME, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, SCOPES)
            creds = flow.run_console()
        # Save the credentials for the next run
        with open(TOKEN_NAME, 'w') as token:
            token.write(creds.to_json())

    googleAPI = build('youtube', 'v3', credentials=creds)

    now = datetime.datetime.now()
    print("[+] ", now.year, now.month, now.day, now.hour, now.minute, now.second)
    
    print("[+] ", outputFile)

    if not os.path.exists(videoDirectory):
        os.makedirs(videoDirectory)
    
    # Step 1: Scrape Videos
    print("[+] Scraping Videos...")
    scrapeVideos(username = IG_USERNAME,
                 password = IG_PASSWORD,
                 output_folder = videoDirectory,
                 modeAM = mode,
                  days=1)
    print("[+] Scraped Videos!")
    
    # intro into description
    description += """Enjoy some of the funniest videos on the internet! 
Why spend hours searching for funny videos that make you laugh when you can get some of the best memes here!

In this video, I show you the best Dank Video Memes on the internet😁😂😂.
Links To Sources & Credit to owners⬇️:

"""
    
    with open("description.txt", 'a') as dfile:
        dfile.write(description)

    # Step 2: Make Compilation

    if mode == "M":
        makeCompilation_or_not = input("[Q] Use existing compilation(Check name)(Y/n)")
        if makeCompilation_or_not == "n":
            print(f"[+] using existing File {outputFile}")
        else:
            print("[+] Making Compilation...")
            makeCompilation(path = videoDirectory,
                            introName = INTRO_VID,
                            outroName = OUTRO_VID,
                            totalVidLength = TOTAL_VID_LENGTH,
                            maxClipLength = MAX_CLIP_LENGTH,
                            minClipLength = MIN_CLIP_LENGTH,
                            outputFile = outputFile,
                            videoDirectory = videoDirectory,
                            description_meta= "")
            print("[+] Made Compilation!")
    else:
        print("[+] Making Compilation...")
        makeCompilation(path = videoDirectory,
                        introName = INTRO_VID,
                        outroName = OUTRO_VID,
                        totalVidLength = TOTAL_VID_LENGTH,
                        maxClipLength = MAX_CLIP_LENGTH,
                        minClipLength = MIN_CLIP_LENGTH,
                        outputFile = outputFile,
                        videoDirectory = videoDirectory,
                        description_meta= "")
        print("[+] Made Compilation!")

    # added video metaData(profile, video_url, Caption) within make_compilation script
    #description += make_compilation.description_meta

    description += """
    Welcome to my Channel, where I search for the best trending videos, or videos people have forgotten about, and put them all in one video. I upload 2-3 times a week to keep video quality high. I always ask for permission to share videos that I find!
If you enjoyed this video, watch my other videos as well


Click here to subscribe today:
►►►Follow me!
new video every day :)

#️⃣clips featured are used with permission from original creators

"""

    #disclaimer
    description += "\n----------------------------------------------------------------------------------------------------------------"

    # tags
    description += """\n
In this video you will watch Extremely Funny memes, dankest, funny af, offensive memes, vine videos, meme compilation, dank meme compilation, Funny videos, Memes, Unexpected videos, Reddit Memes, Perfectly Cut Screams Memes, Watch People Die Inside Memes, videos I found on reddit, Try not to laugh videos, Totally Random, Cursed Memes, Cute and Funny Animals, Cute and Funny Dogs, Cute and Funny Cats,  Funny Vines, Anime Memes, Cartoon Memes, Fails Memes, SpongeBob Memes, Spiderman Memes, Super Mario Memes, Dwayne "The Rock" Johnson Memes, Gaming Memes, Among Us "Sus" Memes, Disney Memes, Nintendo Memes, Wii Sports Memes, Mickey Mouse Memes, Star Wars Memes, Adventure Time Memes, Twitch Streamer Memes, Family Guy Memes, GTA Memes, Bowling Memes, Soccer Football Memes, Fortnite Memes, Music Memes, Avengers Memes, Michael Jackson Memes, Pokemon Memes, Windows Error Memes, Thanos Memes, Zoom Memes, Winnie The Pooh Memes, McDonald's Memes, Monkey Memes, Twitter Memes, Will Smith Memes, School Memes, Halloween Memes, Phineas and Ferb Memes, Mom Memes, Holy Memes, Amazon Echo Memes, Gorillaz Memes

Memes that are approved by school
Memes that will finally bring you happiness
You laugh, you 💀
Memes that are teacher approved
Memes that will finally bring you happines
memes that 😂
UNUSUAL MEMES COMPILATION
The Best Of The Internet
"""
    description += "\n\nCopyright Disclaimer, Under Section 107 of the Copyright Act 1976, allowance is made for 'fair use' for purposes such as criticism, comment, news reporting, teaching, scholarship, and research. Fair use is a use permitted by copyright statute that might otherwise be infringing. Non-profit, educational or personal use tips the balance in favor of fair use.\n\n"

    # Hashtags
    description += "#memes #dankmemes #compilation #funny #funnyvideos \n\n"
    description += "#memes #dankmemes #compilation #funny #funnyvideos #shorts #TikTok #randomvideos "

    with open("description.txt", 'a+') as dfile:
        dfile.write(description)
        description = dfile.read()

    print("[+]", description)

    tags += "Extremely Funny memes, dankest, funny af, offensive memes, vine videos, meme compilation, dank meme compilation, Funny videos, Memes, Unexpected videos, Reddit Memes"

    # Step 3: Upload to Youtube
    
    def upload_to_youtube():
        print("[+] Uploading to Youtube...")
        uploadYtvid(VIDEO_FILE_NAME=outputFile,
                    title=title,
                    description=description,
                    googleAPI=googleAPI)
        print("[+] Uploaded To Youtube!")
    
    if mode =="A":
        upload_to_youtube()
        print(f"[+] tags used: {tags}")
    elif mode =="M":
        proceed_to_upload = input("[Q] Upload to YouTube Y/n:")
        if proceed_to_upload != "n":
            upload_to_youtube()
            print(f"[+] tags used: {tags}")
        else:
            print("[+] Video not uploaded to YouTube")
    
    # Step 4: Cleanup
    def cleanup():
      print("[-] Removing temp files!")
      # Delete all files made:
      #   Folder videoDirectory
      shutil.rmtree(videoDirectory, ignore_errors=True)
      #   File outputFile
      try:
          os.remove(outputFile)
      except OSError as e:  ## if failed, report it back to the user ##
          print ("[E] Error: %s - %s." % (e.filename, e.strerror))
      print("Removed temp files!")
    
    if mode == "A":
      cleanup()
    elif mode == "M":
      keep_files = input("[Q] Do you wanna keep temp files?(Y/n)").strip()
      if keep_files == "n":
        cleanup()
      else:
        print("[-] files are not deleted")

def attemptRoutine():
    while(1):
        try:
            routine(title, description, tags)
            break
        except OSError as err:
            print("[e] Routine Failed on " + "OS error: {0}".format(err))
            time.sleep(60*60)

#attemptRoutine()
schedule.every().day.at(DAILY_SCHEDULED_TIME).do(attemptRoutine)

attemptRoutine()
while True:
    schedule.run_pending()  
    time.sleep(60) # wait one min
