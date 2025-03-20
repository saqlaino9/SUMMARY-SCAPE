import sys
import re
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url):
    """Extract YouTube video ID from URL (supports both standard and short URLs)."""
    match = re.search(r"(?:v=|be/)([a-zA-Z0-9_-]+)", url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube URL format")

def extract_metadata(url):
    """Fetch video title and channel name from YouTube page."""
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    # Extract video title
    link_title = soup.find("title")
    title = link_title.text if link_title else "Unknown Title"

    # Extract channel name
    link_channel = soup.find("link", itemprop="name")
    channel = link_channel["content"] if link_channel else "Unknown Channel"

    return title, channel

def download_thumbnail(video_id, save_path="thumbnail.jpg"):
    """Download YouTube video thumbnail and save it as a file."""
    try:
        image_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        response = requests.get(image_url, timeout=10)

        # Check if the request was successful
        if response.status_code == 200:
            with open(save_path, "wb") as handler:
                handler.write(response.content)
            print(f"Thumbnail saved as {save_path}")
        else:
            print(f"Failed to download thumbnail. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading thumbnail: {e}")

def show_thumbnail(save_path="thumbnail.jpg"):
    """Display the downloaded thumbnail using Streamlit."""
    st.image(save_path, use_container_width=True) 

def get_transcript(video_id):
    """Fetch transcript (subtitles) for the video."""
    try:
        transcript_raw = YouTubeTranscriptApi.get_transcript(video_id, languages=["en", "hi", "ur", "te", "ar"])
        transcript_str_lst = [i["text"] for i in transcript_raw]
        transcript_full = " ".join(transcript_str_lst)
        return transcript_full
    except Exception as e:
        return f"Error fetching transcript: {e}"

if __name__ == "__main__":
    try:
        # Debugging: Print received arguments
        print("Arguments passed:", sys.argv)

        # Check for valid number of arguments
        if len(sys.argv) != 2:
            print("Usage: python scrape_youtube.py https://www.youtube.com/watch?v=-tBKkfahCFQ")
            sys.exit(1)

        # Get YouTube URL from command-line argument
        youtube_url = sys.argv[1]

        # Process video
        video_id = extract_video_id(youtube_url)
        title, channel = extract_metadata(youtube_url)
        transcript = get_transcript(video_id)
        download_thumbnail(video_id)

        # Print results
        print(f"Title: {title}")
        print(f"Channel: {channel}")
        print("=" * 30)
        print(transcript)

    except Exception as e:
        print("Error:", e)
        sys.exit(1)


