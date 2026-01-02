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
            "base_language": data.language_code.split("-")[0],
            "is_generated": data.is_generated,
            "source": "youtube"
        }
        captions.append(captions_meta)
    return captions

def select_best_caption(captions):
    '''
    This function will get the caption metadata. It will select the best based on the quality first,
    language second and it will return with the caption metadata with confidence.
    '''

    language_priority = ["en", "hi", "mr", "ta", "te", "kn"]

    if not captions:
        return None
    
    def language_rank(base_language):
        if base_language in language_priority:
            return language_priority.index(base_language)
        return len(language_priority)

    sorted_captions = sorted(
        captions,
        key = lambda c: (
            c['is_generated'],
            language_rank(c['base_language'])
        )
    )

    best = sorted_captions[0]

    best['confidence'] = "low" if best['is_generated'] else "high"

    return best

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

    captions = discover_captions("gmwQeIS8sPY")

    print(f"captions are {captions}")
    print(f"Best one is {select_best_caption(captions)}")