from pytube import YouTube
import requests
import re
import argparse
import sys


def banner():
    ban = '''
██╗░░░██╗░█████╗░██╗░░░██╗██████╗░██╗░░░░░░█████╗░██╗░░░██╗
╚██╗░██╔╝██╔══██╗██║░░░██║██╔══██╗██║░░░░░██╔══██╗╚██╗░██╔╝
░╚████╔╝░██║░░██║██║░░░██║██████╔╝██║░░░░░███████║░╚████╔╝░
░░╚██╔╝░░██║░░██║██║░░░██║██╔═══╝░██║░░░░░██╔══██║░░╚██╔╝░░
░░░██║░░░╚█████╔╝╚██████╔╝██║░░░░░███████╗██║░░██║░░░██║░░░
░░░╚═╝░░░░╚════╝░░╚═════╝░╚═╝░░░░░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░

Author: Nitin Choudhury
Version: 0.0.1

'''
    print(ban)


class YTDownload:

    def downloadAudio(self, url):
        yt = YouTube(url)
        print("[+] Downloading Audio Content:", yt.title)
        ys = yt.streams.filter(only_audio=True).first()
        ys.download()

    def downloadVideo(self, url):
        yt = YouTube(url)
        print("[+] Downloading Video Content:", yt.title)
        ys = yt.streams.get_highest_resolution()
        ys.download()

    def extract_url_from_playlist(self, url):
        content = requests.get(url)
        text = content.content.decode()
        urls = set(re.findall(r'(?:{"url":")(/watch\?v=[a-zA-Z0-9_+-=/\\]+index=[0-9]+)', text))

        return list(urls)

    def extract_url_from_file(self, file):
        f = open(file, 'r')
        text = f.read()
        f.close()
        urls = re.split(r'\n+', text)

        return urls


class Launch:

    def __init__(self,
                 URL=None,
                 PURL=None,
                 FILE=None,
                 AUDIO=False,
                 VIDEO=True
                 ):
        self.URL = URL
        self.PURL = PURL
        self.AUDIO = AUDIO
        self.VIDEO = VIDEO
        self.FILE = FILE

    def launchandwait(self):
        downloader = YTDownload()

        if self.URL and self.AUDIO:
            downloader.downloadAudio(self.URL)

        if self.URL and self.VIDEO:
            downloader.downloadVideo(self.URL)

        if self.FILE:
            urls = downloader.extract_url_from_file(self.FILE)

            if self.AUDIO:
                for url in urls:
                    if url:
                        downloader.downloadAudio(url)

            if self.VIDEO:
                for url in urls:
                    if url:
                        downloader.downloadVideo(url)

        if self.PURL:
            urls = downloader.extract_url_from_playlist(self.PURL)

            if self.AUDIO:
                for url in urls:
                    downloader.downloadAudio(url)

            if self.VIDEO:
                for url in urls:
                    downloader.downloadVideo(url)


if __name__ == '__main__':
    banner()
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-u", "--url",
        type=str,
        help="Youtube Video URL",
        default=None
    )

    parser.add_argument(
        "-p", "--playlist",
        type=str,
        help="Youtube Playlist URL",
        default=None
    )

    parser.add_argument(
        "-f", "--file",
        type=str,
        help="File containing URLs",
        default=None
    )

    parser.add_argument(
        "-a", "--audio",
        type=bool,
        help="Download Audio Only",
        default=False
    )

    parser.add_argument(
        "-v", "--video",
        type=bool,
        help="Download Video [higher resolution Only]",
        default=False
    )

    args = parser.parse_args()

    if args.audio or args.video or args.file:
        AUDIO = args.audio
        VIDEO = args.video

    else:
        AUDIO = False
        VIDEO = True

    if args.url or args.playlist or args.file:
        if args.url:
            URL = args.url
            PURL = None
            FILE = None

        elif args.playlist:
            URL = None
            PURL = args.playlist
            File = None

        else:
            URL = None
            PURL = None
            FILE = args.file

        print("Fetching Data...")
        launcher = Launch(URL, PURL, AUDIO, VIDEO)

        try:
            launcher.launchandwait()
            print("[+] Download Successful!")
        except:
            print("[-] Download Failed!")

    else:
        filename = sys.argv[0]
        print(f"NO URL SPECIFIED\n\nHELP: {filename} --help")
        exit()