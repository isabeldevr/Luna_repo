from dotenv import load_dotenv
import os
import base64
import requests
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
refresh_token = os.getenv("REFRESH_TOKEN")

#print(client_id, client_secret)

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")  # Corrected encoding and decoding

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }

    result = requests.post(url, headers=headers, data=data)

    if result.status_code == 200:
        json_result = result.json()
        if "access_token" in json_result:
            token = json_result["access_token"]
            return token
        else:
            print("The 'access_token' key is not present in the JSON response.")
    else:
        print(f"Error: {result.status_code} - {result.text}")

    return None

token = get_token()
#print(token)

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)

    params = {
        "q": artist_name,
        "type": "artist",
        "limit": 1
    }

    result = requests.get(url, headers=headers, params=params)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None
    
    return json_result[0]

def get_song_by_artist(token, artist_id, country="US"):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = get_auth_header(token)
    params = {"market": country}  
    result = requests.get(url, headers=headers, params=params)
    json_result = json.loads(result.content)
    tracks = json_result.get("tracks", [])
    return tracks


token = get_token()
result = search_artist(token, "Charlie Puth")
artist_id = result["id"]
songs = get_song_by_artist(token, artist_id)


for idx, song in enumerate (songs):
    print(f"{idx+1}, {song['name']}")
