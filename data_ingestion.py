from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def parse_video_id(video_url:str)->str:
    parsed = urlparse(video_url)
    if parsed.hostname in ("www.youtube.com","youtube.com"):
        if parsed.path=="/watch":
            return parse_qs(parsed.query).get("v",[None])[0]
        elif parsed.path.startswith("/embed/"):
            return parsed.path.split("/")[2]
        elif parsed.path.startswith("/shorts/"):
            return parsed.path.split("/")[2]
    if parsed.hostname == "youtu.be":
        return parsed.path.lstrip("/")

    return None

def discover_captions(video_id:str):
    ytt_obj = YouTubeTranscriptApi()
    metadata_list = ytt_obj.list(video_id)
    captions = []
    for data in metadata_list:
        captions_meta = {
            "video_id":video_id,
            "language_code": data.language_code,
            "is_generated": data.is_generated,
            "source": "youtube"
        }
        captions.append(captions_meta)
    return captions

def select_best_caption(captions):
    preffered_lang = ['en','en-IN','en-US','hi']
    lang = ""
    for obj in captions:
        if obj.get('language_code') in preffered_lang:
            lang = obj.get('language_code')
            break
    if lang == "":
        return f"Preffered language not available"
    else:
        return lang

if __name__ == "__main__":
    urls = [
    "https://youtube.com/watch?v=abc123",
    "https://youtube.com/watch?v=abc123&t=10",
    "https://youtu.be/abc123",
    "https://youtube.com/shorts/abc123",
    "https://www.youtube.com/embed/abc123",
]
    # for u in urls:
    #     print(parse_video_id(u))

    print(select_best_caption([{'video_id': '-UQ6OZywZ2I', 'language_code': 'hi', 'is_generated': True, 'source': 'youtube'}]))