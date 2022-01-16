from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.resize import resize
import os
from os.path import isfile, join
import random
import shutil 
from collections import defaultdict
import json

VideoFileClip.resize = resize

def extractAcc(filepath):
    try:
        s = filepath.split("/")[-1].split("-")
        acc = "-".join(s[1:(2+(len(s) - 4))])
        return acc
    except:
        return ""


# makeCompilation takes videos in a folder and creates a compilation with max length totalVidLength
def makeCompilation(path = "./",
                    introName = '',
                    outroName = '',
                    totalVidLength = 10,
                    maxClipLength = 20,
                    minClipLength = 5,
                    outputFile = "output.mp4",
                    video_source_meta = {},
                    videoDirectory = "",
                    description_meta = "",
                    modeAM = "A"):

    downVideos = []
    seenLengths = defaultdict(list)
    #totalLength = 0
    duration = 0
    videos = []

    # Add intro video if included
    if introName != '':
        introVid = VideoFileClip("./" + introName)
        videos.append(introVid)
        duration += introVid.duration


    for fileName in os.listdir(path):
        filePath = join(path, fileName)

        if isfile(filePath) and fileName.endswith(".mp4"):

            if os.stat(filePath).st_size < 5000:
                continue

            # Destination path
            print(filePath)
            clip = VideoFileClip(filePath)
            clip = clip.resize(width=1920)
            clip = clip.resize(height=1080)
            duration = clip.duration
            print(fileName + " " + str(duration) + " Added")

            # add_video in min&max range or ignore errors
            def add_video(duration):
                downVideos.append(clip)
                seenLengths[duration].append(fileName)
                duration += clip.duration


            print(duration, seenLengths, downVideos)

            if modeAM == "A":
                add_video(duration)
            elif modeAM == "M":
                if duration <= maxClipLength and duration >= minClipLength:
                    add_video(duration)
                else:
                    ignore_error = input("Do you want to ignore Errors in min max Total Video Length?(Y/n)").strip()
                    if ignore_error != "n":
                        pass
                    else:
                        add_video(duration)

            #Add automated description

            for k in range(len(os.listdir(path))):
                
                fileNameJ = fileName.split(".mp4")
                fileNameJSON = ''.join(fileNameJ) + ".json"

                acc = extractAcc(clip.filename)

                # Fix error in TimeStamps
                duration_in_min = str(duration).split(".")
                #duration_in_min.pop()
                video_source_meta[f"TimeStamps{k}"] = "00:" + str(duration_in_min[0]) + " : @" + acc + "\n"

                video_source_meta[f"profile{k}"] = "Instagram profile:" + "  instagram.com/" + acc +'\n'
                    
                #extract url & other information about video
                
                f = open(f"{videoDirectory}{fileNameJSON}", "r")
                json_d = json.loads(f.read())
                f.close()

                video_source_meta[f"vido_url{k}"] = "Video URL:" + "instagram.com/tv/" + json_d["shortcode"] + '\n'
                video_source_meta[f"Caption{k}"] = json_d["edge_media_to_caption"]["edges"][0]["node"]["text"] + '\n'

                description_meta = video_source_meta[f"TimeStamps{k}"] + video_source_meta[f"profile{k}"] + video_source_meta[f"vido_url{k}"] + video_source_meta[f"Caption{k}"] + '\n\n'

    print(description_meta)
    print("Total Length: " + str(duration))

    # Create videos
    for clip in downVideos:
        #duration += clip.duration 
        videos.append(clip)

        if duration >= totalVidLength:
            # Just make one video
            break
    
    # Add outro vid
    if outroName != '':
        outroVid = VideoFileClip("./" + outroName)
        videos.append(outroVid)
    
    # Used Moviepy lib
    finalClip = concatenate_videoclips(videos, method="compose")

    audio_path = "/tmp/temoaudiofile.m4a"

    # Create compilation
    finalClip.write_videofile(outputFile, threads=8, temp_audiofile=audio_path, remove_temp=True, codec="libx264", audio_codec="aac")
    
    return description_meta
    
if __name__ == "__main__":
    makeCompilation(path = "/home/kali/Documents/YOUTUBE/AutomatedChannel/Videos/Memes/",
                    introName = "intro_vid.mp4",
                    outroName = '',
                    totalVidLength = 10*60,
                    maxClipLength = 20,
                    outputFile = "outputseq.mp4",
                    video_source_meta = {},
                    videoDirectory = "",
                    description_meta = "",
                    modeAM = "A")
