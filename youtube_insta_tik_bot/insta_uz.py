import requests
from pprint import pprint 
url = "https://instagram-media-downloader.p.rapidapi.com/rapid/post_v2.php"

def insta_save(link):

    querystring = {"url":link}

    headers = {
        "X-RapidAPI-Key": "138577ad99msh285e033da25ed1bp12cefbjsne90ad86c1843",
        "X-RapidAPI-Host": "instagram-media-downloader.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    try:
        result = ("video",response.json()["items"][0]["video_versions"][0]["url"])
    except:
        result = ("rasm",response.json()["items"][0]["image_versions2"]["candidates"][0]["url"])
    
    return result