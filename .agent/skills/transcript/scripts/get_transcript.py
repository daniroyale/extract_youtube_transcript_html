#!/usr/bin/env python3
"""
YouTube Transcript Extractor Script

This script extracts transcripts from YouTube videos using the youtube-transcript-api library.
It supports both YouTube URLs and video IDs, with options for language selection and output file.
"""

import argparse
import sys
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,

    YouTubeRequestFailed
)


def extract_video_id(url_or_id):
    """
    Extract video ID from a YouTube URL or return the ID if already provided.
    
    Args:
        url_or_id (str): YouTube URL or video ID
        
    Returns:
        str: The video ID
        
    Raises:
        ValueError: If the URL format is invalid
    """
    # If it's already a video ID (11 characters, alphanumeric with - and _)
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url_or_id):
        return url_or_id
    
    # Try to extract from various YouTube URL formats
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/v\/([a-zA-Z0-9_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    
    raise ValueError(f"Could not extract video ID from: {url_or_id}")


def get_transcript(video_id, language='en'):
    """
    Fetch the transcript for a YouTube video.
    
    Args:
        video_id (str): YouTube video ID
        language (str): Language code (default: 'en')
        
    Returns:
        str: The full transcript text
        
    Raises:
        Various exceptions from youtube_transcript_api
    """
    try:
        # Create an instance and fetch the transcript
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id, languages=[language])
        
        # Combine all text segments from snippets
        full_text = ' '.join([snippet.text for snippet in transcript.snippets])
        
        return full_text
    
    except TranscriptsDisabled:
        raise Exception(f"Transcripts are disabled for video: {video_id}")
    except NoTranscriptFound:
        raise Exception(f"No transcript found for language '{language}' in video: {video_id}")
    except VideoUnavailable:
        raise Exception(f"Video unavailable: {video_id}")

    except YouTubeRequestFailed as e:
        raise Exception(f"YouTube request failed: {str(e)}")


def main():
    """Main function to handle command-line interface."""
    parser = argparse.ArgumentParser(
        description='Extract transcripts from YouTube videos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  %(prog)s "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o transcript.txt
  %(prog)s "dQw4w9WgXcQ" --lang es -o transcript_es.txt
        """
    )
    
    parser.add_argument(
        'url',
        help='YouTube URL or video ID'
    )
    
    parser.add_argument(
        '--lang',
        default='en',
        help='Language code for the transcript (default: en)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output file path. If not specified, prints to stdout'
    )
    
    args = parser.parse_args()
    
    try:
        # Extract video ID from URL or use as-is if already an ID
        video_id = extract_video_id(args.url)
        
        # Fetch the transcript
        transcript = get_transcript(video_id, args.lang)
        
        # Output the transcript
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(transcript)
            print(f"Transcript saved to: {args.output}", file=sys.stderr)
        else:
            print(transcript)
        
        return 0
    
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error fetching transcript: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
