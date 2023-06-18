import requests
import os
import json
from urllib.parse import urlparse

def download_file(url, output_dir, md5):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        file_extension = os.path.splitext(urlparse(url).path)[-1]
        file_name = md5 + file_extension
        file_path = os.path.join(output_dir, file_name)

        if os.path.exists(file_path):
            print(f"Skipping download of {url}. File '{file_name}' already exists".lower())
        else:
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)

            print(f"Downloaded: {file_name} to {file_path}".lower())
    except requests.exceptions.HTTPError as e:
        print(f"Skipping download of {url}. Error: {e}".lower())
    except requests.exceptions.RequestException as e:
        print(f"Skipping download of {url}. Error: {e}".lower())

input_directory = "./input"
json_file_path = os.path.join(input_directory, "jd-akamai-origin.json")

output_directory = "./output"
public_directory = os.path.join(output_directory, "public")

if not os.path.exists(public_directory):
    os.makedirs(public_directory)

directories = [
    "TestBundle",
    "com-videos",
    "dance-machine",
    "home",
    "jdnext",
    "map",
    "playlists",
    "portrait-borders",
    "quests",
    "skin",
    "streamed-videos",
    "wdf-bosses",
    "wdf"
]

valid_extensions = (".jpg", ".png", ".webm", ".zip", ".bundle", ".mp4", ".ckd")

with open(json_file_path) as file:
    data = json.load(file)
    for item in data:
        url = item.get("url")
        md5 = item.get("md5")
        if (
            url
            and md5
            and url.startswith("https://")
            and "private" not in url
            and any(directory in url for directory in directories)
        ):
            file_extension = os.path.splitext(urlparse(url).path)[-1]
            if file_extension in valid_extensions:
                url_parts = urlparse(url).path.split("/")
                nested_directory = public_directory
                for part in url_parts[2:-1]:
                    nested_directory = os.path.join(nested_directory, part)
                    if not os.path.exists(nested_directory):
                        os.makedirs(nested_directory)

                download_file(url, nested_directory, md5)
            else:
                print(f"Skipping download of {url}. Invalid file extension: {file_extension}")

















