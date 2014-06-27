#!/usr/bin/env python
#=========================================================#
# [+] Title: Youtube Video's Caption Downloader           #
# [+] Script: ytcaption.py                                #
# [+] Blog: http://www.pythonforpentesting.com            #
# [+] Twitter: @OffensivePython                           #
#=========================================================#
import urllib2
import urlparse
import re
from optparse import OptionParser

def getVideoID(url):
    try:
        http = re.search("https?://", url).groups()
    except AttributeError:
        url = "http://"+url
    parsed = urlparse.urlparse(url)
    path = parsed.path
    query = parsed.query
    video_id = ""
    if path.upper() == "/WATCH":
        try:
            video_id = re.search("v=(.+)", query).group(1)
            if "&" in video_id:
                video_id = video_id[:video_id.index("&")]
        except AttributeError:
            pass
    elif "EMBED" in path.upper():
        try:
            video_id = re.search("/embed/(.+)", path).group(1)
        except AttributeError:
            pass

    if video_id:
        return video_id
    else:
        return None

def getTitle(video_id):
    url = "http://m.youtube.com/watch?v="+video_id
    try:
        html = urllib2.urlopen(url).read(4096)
        title = ""
        try:
            title = re.search("<title>(.+) - YouTube", html).group(1)
        except AttributeError:
            title = video_id
            pass
    except urllib2.HTTPError:
        return None
    return title

def sanitize(text):
    badchar = ('\\','/',':','*','?','"','<','>','|')
    ntext = text
    for b in badchar:
        ntext = ntext.replace(b, '')
    return ntext

def getSubtitle(video_id, title):
    url = "http://www.youtube.com/api/timedtext?format=srt&lang=en&v="+video_id
    try:
        srt = urllib2.urlopen(url).read()
        if srt:
            fname = sanitize(title)+".srt"
            try:
                f = open(fname, "w")
                f.write(srt)
                f.close()
                success = True
            except:
                pass
    except urllib2.HTTPError:
        return False

    return success

def download(url):
    video_id = getVideoID(url)
    if video_id:
        title = getTitle(video_id)
        if title:
            if getSubtitle(video_id, title):
                print("[+]%s: Done"%title)
            else:
                print("[+]%s: Video not found or doesn't have captions"%title)

def main():
    usage = """usage: %prog [options]\r\n
e.g: %prog -u http://www.youtube.com/watch?v=VIDEO_ID
            --file=links.txt"""
    parser = OptionParser(usage=usage)
    parser.add_option("-u", "--url",
                      dest="url", type="string",
                      help="YouTube video link", metavar="URL")
    parser.add_option("-f", "--file",
                      dest="fname", type="string",
                      help="File of Youtube videos links", metavar="FILE")
    options, args = parser.parse_args()
    if options.url:
        download(options.url)
    elif options.fname:
        f = open(options.fname, "r")
        for link in f.readlines():
            download(link)
    else:
        parser.print_help()
if __name__ == "__main__":
    print("#=========================================================#")
    print("# [+] Title: Youtube Video's Caption Downloader           #")
    print("# [+] URL: http://www.pythonforpentesting.com             #")
    print("# [+] Twitter: @OffensivePython                           #")
    print("#=========================================================#")
    main()
