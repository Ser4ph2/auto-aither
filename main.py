#!/usr/bin/python3

try:
    from time import sleep
    import os
    import requests
except ImportError:
    print("[!] Missing library, please run: pip install -r requirements.txt")
    sleep(2)
    exit(1)

def dispBanner():
    print("*"*16)
    print("AUTO-AITHER v0.1")
    print("*"*16)

def newAnnounceURL():
    print("\n\n[?] Enter PID (see github FAQ if unsure): ", end="")
    pid = input()
    url = "https://aither.cc/announce/" + pid
    with open("announce.txt", "w") as f:
        f.write(url)
    return url

def loadAnnounceURL():
    try:
        with open("announce.txt", "r") as f:
            url = f.read()
        return url
    except Exception as e:
        print("Exception: " + str(e))
        return None

def makeTorrent(path):
    # determine which piece size to use for torrent: 0.5mb if file < 1gb, 4mb if file < 50gb and 16mb if file > 50gb
    size = os.path.getsize(path)
    if size <= 500000:
        pieceSize = "22"
    elif size > 500000 and size < 53687091200:
        pieceSize = "24"
    else:
        pieceSize = "25" 

    print("\n\n[1] Enter announce URL and save for future use")
    print("[2] Use saved announce URL")
    print("[3] Use placeholder announce URL (you will need to download the .torrent file after to use in your torrent client)")
    while True:
        choice = input("> ")
        if choice in ["1", "2", "3"]:
            break
        else:
            print("[!] Invalid option\n")

    if choice == "1":
        announceURL = newAnnounceURL()
    elif choice == "2":
        announceURL = loadAnnounceURL()
    else:
        announceURL = "placeholder"

    print("\n")
    print("-"*50)
    os.system("mktorrent -l {} -p -v -a {} {}".format(pieceSize, announceURL, path))
    print("-"*50)

    return path.split("/")[-1] + ".torrent"

def takeScreenshots(path):
    print("[?] Is the path ({}) a [1]file or a [2]folder?".format(path))
    while True:
        choice = input("> ")
        if choice in ["1", "2"]:
            break
        else:
            print("[!] Invalid option\n")
    
    if choice == "2":
        folderContents = os.listdir(path)
        for each in folderContents:
            print("[{}] {}".format(str(folderContents.index(each)+1), each))
        print("\n[?] Select file to use for screenshots")
        while True:
            try:
                choice = input("> ")
                if int(choice) >= 1 and int(choice) < len(folderContents) + 1 :
                    break
                else:
                    print("[!] Invalid option\n")
            except:
                print("[!] Invalid option\n")
        
        filePath = path + "/" + folderContents[int(choice)-1]
    else:
        filePath = path

    timeStamps = [300, 600, 900, 1200, 1500, 1800]
    os.system("mkdir screenshots")
    while True:
        for each in timeStamps:
            os.system("ffmpeg -ss {} -i {} -q:v 2 -vframes 1 screenshots/{}.jpg".format(each, filePath, str(timeStamps.index(each)+1)))
        print("\n[?] Are these screenshots okay? (./screenshots) [Y/n]: ", end="")
        tmp = input()
        if tmp.upper() != "N" and tmp.upper != "NO":
            break
        else:
            timeStamps = [x + 200 for x in timeStamps]
    
    return filePath

def uploadScreenshots():
    os.chdir("screenshots")
    for each in os.listdir():
        os.system("curl -F'file=@{}' https://0x0.st >> imagelinks.txt".format(each))
    os.chdir("..")

def getMediainfo(filePath):
    print("\n[*] Getting mediainfo...")
    os.system("mediainfo {} > mediainfo.txt".format(filePath))
    print("[*] Done! If you need to remove any personal information from mediainfo.txt, do so now. Press enter to continue.")
    input()

    mediainfo = ""
    with open("mediainfo.txt", "r") as f:
        mediainfo += f.read()
    return mediainfo

def getInfo():
    print("\n\n")
    print("[?] Enter name of movie/show with year/season: ", end="")
    title = input()

    print("\n[1] Movie")
    print("[2] TV")
    print("[?] Choose category: ",end="")
    category = int(input())

    print("[?] Enter resolution: ", end="")
    res = input()

    print("[?] Enter source: ", end="")
    source = input()

    print("\n[1] Encode")
    print("[2] Remux")
    print("[3] WEB-DL")
    print("[4] WEBRip")
    print("[5] Other")
    while True:
        print("[?] Choose type: ", end="")
        tmp = input()
        if tmp in ["1", "2", "3", "4", "5"]:
            if tmp == "1":
                torrentType = "Encode"
            elif tmp == "2":
                torrentType = "Remux"
            elif tmp == "3":
                torrentType = "Web-DL"
            elif tmp == "4":
                torrentType = "WEBRip"
            else:
                torrentType = "Other"
            break
        else:
            print("[!] Invalid option.")

    print("[?] Enter video codec: ", end="")
    video = input()

    print("[?] Enter audio codec: ", end="")
    audio = input()

    print("[?] Enter TMDB: ", end="")
    tmdb = input()

    print("[?] 10bit colour depth? [y/N]: ", end="")
    tmp = input()
    if tmp.upper() != "Y" and tmp.upper != "YES":
        bits10 = ""
    else:
        bits10 = "10bit"
    
    print("[?] Anonymous upload? [y/N]: ", end="")
    tmp = input()
    if tmp.upper() != "Y" and tmp.upper != "YES":
        anon = 0
    else:
        anon = 1
    
    print("[?] Stream optimised? [y/N]: ", end="")
    tmp = input()
    if tmp.upper() != "Y" and tmp.upper != "YES":
        stream = 0
    else:
        stream = 1

    print("[?] Standard definition? [y/N]: ", end="")
    tmp = input()
    if tmp.upper() != "Y" and tmp.upper != "YES":
        sd = 0
    else:
        sd = 1

    print("[?] Internal release? [y/N]: ", end="")
    tmp = input()
    if tmp.upper() != "Y" and tmp.upper != "YES":
        internal = 0
    else:
        internal = 1

    print("[?] Enter crew/ripper: ", end="")
    crew = input()

    if bits10 == "10bit":
        metadata = [title, res, bits10, source, audio, video]
    else:
        metadata = [title, res, source, audio, video]
    return metadata, category, tmdb, anon, stream, sd, internal, crew, torrentType

def getDescription():
    description = ""
    images = []
    with open("screenshots/imagelinks.txt", "r") as f:
        for line in f.readlines():
            images.append(line)
    
    for each in images:
        description += "[img]{}[/img]\n".format(each)
    return description

def newApiKey():
    print("\n\n[?] Enter API key (see github FAQ if unsure): ", end="")
    key = input()
    with open("apikey.txt", "w") as f:
        f.write(key)
    return key

def loadApiKey():
    try:
        with open("apikey.txt", "r") as f:
            key = f.read()
        return key
    except Exception as e:
        print("Exception: " + str(e))
        return None

def upload(torrentPath, finalTitle, description, mediainfo, category, torrentType, tmdb, imdb, tvdb, mal, igdb, anon, stream, sd, internal, metadata):
    print("\n\n[1] Enter API key and save for future use")
    print("[2] Use saved API key")
    print("[3] Enter API key and don't save")
    while True:
        choice = input("> ")
        if choice in ["1", "2", "3"]:
            break
        else:
            print("[!] Invalid option\n")

    if choice == "1":
        apiKey = newApiKey()
    elif choice == "2":
        apiKey = loadApiKey()
    else:
        apiKey = input("Enter API key: ")

    url = "https://aither.cc/api/torrents/upload?api_token={}".format(apiKey)
    print(url)
    files = {"torrent": open(torrentPath,"rb")}
    values = {"name": finalTitle,
            "description": description,
            "mediainfo": mediainfo,
            "category_id": category,
            "type": torrentType,
            "resolution": metadata[1],
            "tmdb": tmdb,
            "imdb": imdb,
            "tvdb": tvdb,
            "mal": mal,
            "igdb": igdb,
            "anonymous": anon,
            "stream": stream,
            "sd": sd,
            "internal": internal,
            "user_id": 3}
    r = requests.post(url, files=files, data=values)
    return r.status_code

def createTorrentUpload():
    print("\n[?] Enter path of file/folder: ", end="")
    path = input()
    if os.path.exists(path) != True:
        print("[!] File does not exist.\n\n")
        main()

    torrentPath = makeTorrent(path)
    filePath = takeScreenshots(path)
    uploadScreenshots()
    mediainfo = getMediainfo(filePath)
    metadata, category, tmdb, anon, stream, sd, internal, crew, torrentType = getInfo()
    imdb = 0
    tvdb = 0
    mal = 0
    igdb = 0


    finalTitle = " ".join(metadata)
    finalTitle += "-{}".format(crew)
    description = getDescription()

    result = upload(torrentPath, finalTitle, description, mediainfo, category, torrentType, tmdb, imdb, tvdb, mal, igdb, anon, stream, sd, internal, metadata)
    if result == 200:
        print("Upload successfully!")
    else:
        print("Error " + str(result))
    main()


def createTorrent():
    print("\n[?] Enter path of file(s): ", end="")
    path = input()
    if os.path.exists(path):
        torrentPath = makeTorrent(path)
        print("[*] Torrent created: " + torrentPath + "\n\n")
        main()
    else:
        print("[!] File does not exist.\n\n")
        main()

def uploadTorrent():
    pass

def main():
    dispBanner()
    print("[1] Create new .torrent file and upload")
    print("[2] Create new .torrent file")
    print("[3] Upload existing .torrent file")
    print("[4] Exit")
    while True:
        choice = input("> ")
        if choice in ["1", "2", "3", "4"]:
            break
        else:
            print("[!] Invalid option\n")
    
    # python needs switch statements lmao
    if choice == "1":
        createTorrentUpload()
    elif choice == "2":
        createTorrent()
    elif choice == "3":
        uploadTorrent()
    else:
        exit()
try:
    main()
except KeyboardInterrupt:
    print("\nExiting.")
    exit()