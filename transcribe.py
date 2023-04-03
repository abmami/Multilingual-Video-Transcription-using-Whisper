from pytube import YouTube, Playlist
import os
import argparse
import json
import re
import whisper

def extract_video_id(url):
    pattern = r'(?:https?:\/\/)?(?:www\.)?youtu(?:\.be|be\.com)\/(?:.*v(?:\/|=)|(?:.*\/)?)([\w\-]+)'
    match = re.match(pattern, url)
    if match:
        return match.group(1)
    return None


def load_urls(filename):
    with open(filename, 'r') as f:
        urls = json.load(f)
    return urls


def download(url, resolution, videos_path):
    resolution = str(resolution) + "p"
    file_name = extract_video_id(url)
    if file_name:
        file_name = file_name + ".mp4"
        file_path = os.path.join(videos_path, file_name)
        print("Downloading", url)
        yt = YouTube(url)
        yt.streams.filter(res = resolution, progressive= True).first().download(videos_path, file_name)
        print("Downloaded to", file_path)
        return {
            "filename": file_name,
            "title": yt.title
        }


def transcribe(model, video_path, save):
    print("Transcribing", video_path)
    result = model.transcribe(video_path)    
    text = [item["text"] for item in result["segments"]]
    text = "".join(text)
    if not save:
        os.remove(video_path)
    return text

if __name__ == "__main__":

    # paths
    input_path = "data/urls.json"
    videos_path = "data/videos"
    output_path = "data/output.json"

    # model 
    # multilingual models: "tiny", "base" 74M params, "small" 244M params, "medium", "large"
    # More on https://github.com/openai/whisper#available-models-and-languages
    model_name = "small"
    model = whisper.load_model(model_name)

    # args
    parser = argparse.ArgumentParser()
    parser.add_argument("--url",type=str, required=False, help="Single url method", default=None)
    parser.add_argument("--playlist",type=str, required=False, help="Playlist url method", default=None)
    parser.add_argument("--res", type=int, required=False, help="The resolution of the video(s) to download", default=360)
    parser.add_argument('--no-save', action='store_false', dest="save", help='Add this to remove the video(s) from the local storage after transcription.')
    parser.add_argument('--local', action='store_true', dest="local", help='Add this to use local files instead of downloading from youtube.')
    #parser.add_argument('--verbose', action='store_true', dest="verbose", help='Print performance details.')

    args = parser.parse_args()

    # load, download, and transcribe
    if args.url:
        print("Option: from single url")
        urls = [args.url]
    elif args.playlist:
        print("Option: from playlist")
        urls = Playlist(args.playlist).video_urls
    elif args.local:
        # local files in videos_path
        print("Option: from local files")
        urls = os.listdir(videos_path)
    else:
        print("Option: from urls.json")
        urls = load_urls(input_path)

    data = {}
    for url in urls:
        if args.local:
            video = {"filename": url, "title": url}
        else:
            video = download(url, args.res, videos_path)
        video_path = os.path.join(videos_path, video["filename"])
        transcript = transcribe(model, video_path, args.save)
        data[url] = {"title":video["title"], "transcription":transcript}

    # save output to json
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)




