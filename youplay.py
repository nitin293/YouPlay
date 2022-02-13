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
Version: 0.0.4

'''
    print(ban)


class YTDownload:

    def downloadAudio(self, url, outfile):
        yt = YouTube(url)
        print("[+] Downloading Audio Content:", yt.title)
        ys = yt.streams.filter(only_audio=True).first()
        ys.download(outfile)

    def downloadVideo(self, url, outfile):
        yt = YouTube(url)
        print("[+] Downloading Video Content:", yt.title)
        ys = yt.streams.get_highest_resolution()
        ys.download(outfile)

    def extract_url_from_playlist(self, url):
        content = requests.get(url)
        text = content.content.decode()
        urls = set(re.findall(r'(?:{"url":")(/watch\?v=[a-zA-Z0-9_+-=/\\&%]+index=[0-9]+)', text))

        return urls

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
                 VIDEO=True,
                 OUTFILE=None
                 ):
        self.URL = URL
        self.PURL = PURL
        self.AUDIO = AUDIO
        self.VIDEO = VIDEO
        self.FILE = FILE
        self.OUTFILE = OUTFILE

    def launchandwait(self):
        downloader = YTDownload()

        if self.URL and self.AUDIO:
            downloader.downloadAudio(self.URL, self.OUTFILE)

        if self.URL and self.VIDEO:
            downloader.downloadVideo(self.URL, self.OUTFILE)

        if self.FILE:
            urls = downloader.extract_url_from_file(self.FILE)

            if self.AUDIO:
                for url in urls:
                    if url:
                        downloader.downloadAudio(url, self.OUTFILE)

            if self.VIDEO:
                for url in urls:
                    if url:
                        downloader.downloadVideo(url, self.OUTFILE)

        if self.PURL:
            urls = downloader.extract_url_from_playlist(self.PURL)

            if self.AUDIO:
                for url in urls:
                    url = "https://youtube.com" + url
                    downloader.downloadAudio(url, self.OUTFILE)

            if self.VIDEO:
                for url in urls:
                    url = "https://youtube.com" + url
                    downloader.downloadVideo(url, self.OUTFILE)

    # def verbose(self):
    #     print(f"URL: {self.URL}\n"
    #           f"PURL: {self.PURL}\n"
    #           f"FILE: {self.FILE}\n"
    #           f"AUDIO: {self.AUDIO}\n"
    #           f"VIDEO: {self.VIDEO}\n"
    #           f"OUTFILE: {self.OUTFILE}\n"
    #           )


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
        # choices=[True, False],
        default=False
    )

    parser.add_argument(
        "-v", "--video",
        type=bool,
        help="Download Video [higher resolution Only]",
        # choices=[True, False],
        default=False
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Output Directory [DEFAULT: ./]",
        default=False
    )

    args = parser.parse_args()

    if args.audio or args.video or args.file:
        AUDIO = args.audio
        VIDEO = args.video

    else:
        AUDIO = False
        VIDEO = True

    if args.output:
        OUTFILE = args.output

    else:
        OUTFILE = None

    if args.url or args.playlist or args.file:
        if args.url:
            URL = args.url
            PURL = None
            FILE = None

        elif args.playlist:
            URL = None
            PURL = args.playlist
            FILE = None

        else:
            URL = None
            PURL = None
            FILE = args.file

        print("Fetching Data...")
        launcher = Launch(URL=URL, PURL=PURL, FILE=FILE, AUDIO=AUDIO, VIDEO=VIDEO, OUTFILE=OUTFILE)

        try:
            # launcher.verbose()
            launcher.launchandwait()
            print("[+] Download Successful!")

        except KeyboardInterrupt:
            print("[!] KeyboardInterrupt Detected!")

        except requests.exceptions.MissingSchema:
            print("[!] Specify http:// or https:// before URL!")

        except requests.exceptions.ConnectionError:
            print("[!] Connection Error!")

        except:
            raise
            # print("[-] Download Failed!")

    else:
        filename = sys.argv[0]
        print(f"NO URL SPECIFIED\n\nHELP: {filename} --help")
        exit()
