import datetime
from googleapiclient.http import MediaFileUpload

def uploadYtvid(VIDEO_FILE_NAME='',
                title='Intro Video!',
                description=':) ',
                tags=[],
                modeAM = "A",
                googleAPI=None):
    
    now = datetime.datetime.now()
    upload_date_time = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, int(now.second)).isoformat() + '.000Z'

    request_body = {
        'snippet': {
            'categoryId': 23,
            'title': title,
            'description': description,
            'tags': tags
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False, 
        },
        'notifySubscribers': False
    }

    mediaFile = MediaFileUpload(VIDEO_FILE_NAME, chunksize=-1, resumable=True)

    response_upload = googleAPI.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=mediaFile
    ).execute()

    def thumbnail_upload():
        googleAPI.thumbnails().set(
            videoId=response_upload.get('id'),
            media_body=MediaFileUpload('thumbnail.png')
        ).execute()
    
    if modeAM == "A":
        thumbnail_upload()
    elif modeAM == "M":
        wanna_thum = input("[Q]     Do you wanna upload thumbnail.png?(y/N):").strip()
        if wanna_thum.lower() == "y":
            thumbnail_upload()
        else:
            print("[i]      No Custom thumbnail uploaded.")

    print("Upload Successful!")

if __name__ == "__main__":
    uploadYtvid(VIDEO_FILE_NAME='./intro_vid.mp4')
