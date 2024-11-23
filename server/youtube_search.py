import yt_dlp

def youtube_video_search(query: str, max_results: int = 3) -> list:
    """
    Retrieves a list of YouTube video details matching the search query.
    
    Args:
        query (str): The search term to look up on YouTube.
        max_results (int): Maximum number of video results to retrieve.
        
    Returns:
        list: A list of dictionaries with video details (URL, title, views).
        
    Raises:
        yt_dlp.utils.DownloadError: If there's an error accessing YouTube.
        Exception: For other unexpected errors.
    """
    try:
        ydl_opts = {
            'quiet': True,
            'default_search': 'ytsearch',
            'noplaylist': True,
            'extract_flat': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Search on YouTube for the specified number of results
            results = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)
            video_details = []

            # Loop through each entry to extract details
            for video in results['entries']:
                video_url = f"https://www.youtube.com/watch?v={video['id']}"
                video_title = video.get('title', 'Unknown Title')
                video_view_count = video.get('view_count', 'Unknown Views')
                
                video_details.append({
                    'url': video_url,
                    'title': video_title,
                    'views': video_view_count
                })

            return video_details
            
    except yt_dlp.utils.DownloadError as e:
        print(f"Error accessing YouTube: {str(e)}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return []

def youtube_video_main(search_term):
    video_details = youtube_video_search(search_term)
    # for video in video_details:
    #     print(f"Title: {video['title']}")
    #     print(f"URL: {video['url']}")
    #     print(f"Views: {video['views']}")
    #     print("-" * 50)
    
    return video_details  # Return the list of video details

# Example usage:
if __name__ == "__main__":
    videos = youtube_video_main('python')
    # Now `videos` contains the returned list of video details
    # print("Returned Video Details:")
    print(videos)
