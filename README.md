# Multilingual Video Transcription using Whisper

A Python command-line tool for downloading and/or transcribing videos using OpenAI's Whisper open-source model. It supports YouTube video URLs, playlists, videos already downloaded locally, or YouTube URLs from a JSON file. It can download videos in different resolutions, and the resulting transcriptions are saved in a JSON file.

## Setup 

1. Clone the repository:
```bash 
git clone https://github.com/abmami/Multilingual-Video-Transcription-using-Whisper.git
cd Multilingual-Video-Transcription-using-Whisper
```
2. Create and activate a virtual environment:
```bash 
python3 -m venv venv
source venv/bin/activate  # On Linux
venv\Scripts\activate.bat  # On Windows
```
3. Install the required Python packages:
```bash 
pip install -r requirements.txt

```
4. Install FFmpeg:
    - On Ubuntu: 
    ```bash 
    sudo apt-get install ffmpeg
    ```
    - On Windows: 
      - Download the latest static build of FFmpeg from the official website: https://ffmpeg.org/download.html#build-windows
      - Extract the downloaded ZIP file to a folder on your system.
      - Add the path to the bin folder of the extracted FFmpeg to your system's PATH environment variable

## Usage

- Transcribe videos from the urls JSON file in data folder using the following command:
```bash 
python transcribe.py
```
- Transcribe videos that have already been downloaded locally and stored in the folder data/videos using the following command:
```bash 
python transcribe.py --locally
```
- Transcribe a Youtube playlist using the following command:
```bash 
python transcribe.py --playlist YT_PLAYLIST_URL
```

- Transcribe a single Youtube Video using the following command:
```bash 
python transcribe.py --url YT_VIDEO_URL
```


### Additional Options

- `--res`: The resolution of the video(s) to download (default: 360).
- `--no-save`: Add this to delete the video(s) after transcription.

### Configuration

The tool uses the following paths:

- `input_path`: The path to the input file (default: `data/urls.json`).
- `videos_path`: The path to the folder where the videos are saved (default: `data/videos`).
- `output_path`: The path to the output file (default: `data/output.json`).

The tool also uses the Whisper's small model. The size of the small model is ~461M. You can change it in the code to use the base or another model.

- `model_name`: The name of the Whisper model to use (default: `small`).
