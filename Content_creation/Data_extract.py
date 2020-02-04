from bs4 import BeautifulSoup, SoupStrainer
import requests
import os
import urllib
import sys


def get_links_tostories(number_of_stories_needed):
    n = 1
    List = []
    while (
        n <= number_of_stories_needed
    ):  # Number of short stories max 1000 on project guttenberg

        url = f"http://www.gutenberg.org/ebooks/search/?query=Short+Stories&start_index={n}"
        page = requests.get(url)
        data = page.text
        soup = BeautifulSoup(data,features="html.parser")
        for link in soup.find_all("a"):
            url = link.get("href")
            try:
                no = int(url.rsplit("/", 1)[1])
                List.append(no)
            except Exception:
                pass

        n += 25
    return List


def short_story_downloader_urls(List_with_bookids):
    url = f"http://www.gutenberg.org/files/"
    url_download = []
    for Id in List_with_bookids:

        url2 = url + str(Id) + "/"
        page = requests.get(url2)
        data = page.text
        soup = BeautifulSoup(data,features="html.parser")
        zips = []
        for link in soup.find_all("a"):

            if link.get("href").endswith(".txt"):
                zips.append(link.get("href"))
        if len(zips) == 0:
            pass
            # print("The ID {} has no txt".format(Id))
        else:
            url3 = url2 + zips[0]
            # print(url3)
            url_download.append(url3)
    return url_download


def Download_short_stories_text(number_of_stories_needed):
    DOWNLOADS_DIR = "books"
    List = get_links_tostories(int(number_of_stories_needed))
    for url in short_story_downloader_urls(List):

        name = url.split("/")[-1]
        name2 = name.split(sep="txt")[0]
        name3 = name2 + "txt"
        try:
            original_umask = os.umask(0)
            os.makedirs(DOWNLOADS_DIR, mode=0o777, exist_ok=True)
        finally:
            os.umask(original_umask)
        filename = os.path.join(DOWNLOADS_DIR, name3)
        if not os.path.isfile(filename):
            urllib.request.urlretrieve(f"{url}", f"{filename}")
    return "All the short stories have been downloaded"


if __name__ == "__main__":
    # print(sys.argv[1])
    Download_short_stories_text(sys.argv[1])
