from pathlib import Path

import click
from yt_dlp import YoutubeDL


@click.command()
@click.option(
    "-u",
    "--url",
    prompt="Video URL",
    help="URL to the video you want to download"
)
@click.option(
    "-p",
    "--path",
    prompt="Download directory path",
    help="Path to which the downloaded video or audio is saved"
)
@click.option(
    "-cp",
    "--create-path",
    is_flag=True,
    default=False,
    help="If the specified download directory does not exist, create it."
)
@click.option(
    "-a",
    "--audio",
    is_flag=True,
    default=False,
    help="Whether to download only audio"
)
def main(url: str, path: str, create_path: bool, audio: bool) -> None:
    validate_url(url)

    path = Path(path).resolve()

    validate_path(path, create_path)

    if audio:
        options = get_audio_options(path)
    else:
        options = get_video_options(path)

    download(options, url)

def validate_url(url: str) -> None:
    start = "https://www.youtube.com/watch?v="
    if not url.startswith(start):
        raise ValueError(f"URL is invalid, because it does not start with \"{start}\": {url}")

def validate_path(path: Path, create_path: bool) -> None:
    if not path.exists() and not create_path:
        raise FileNotFoundError(f"Directory does not exist: {path}")

    if path.exists() and not path.is_dir():
        raise NotADirectoryError(f"Not a directory: {path}")

def get_audio_options(output_dir: Path) -> dict:
    return {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": str(output_dir / "%(title)s.%(ext)s")
    }

def get_video_options(output_dir: Path) -> dict:
    return {
        "format": "bestvideo*+bestaudio/best",
        "outtmpl": str(output_dir / "%(title)s.%(ext)s")
    }

def download(options: dict, url: str):
    with YoutubeDL(options) as ydl:
        return ydl.download([url])


if __name__ == "__main__":
    main()
