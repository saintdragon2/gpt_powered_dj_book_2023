import csv # CSV 파일 처리를 위한 모듈
from youtube_search import YoutubeSearch # 유튜브 검색 모듈
import yt_dlp # 유튜브 내려받기 모듈

def download_song(title, artist):
    # 노래 제목과 아티스트 정보를 이용해 검색할 쿼리 생성하기
    query=f"{title} {artist} audio"
    # YoutubeSearch 모듈로 쿼리에 대한 검색 결과를 리스트로 받아오기
    search_results=YoutubeSearch(query, max_results=1).to_dict()
    
    # 검색 결과가 있으면
    if len(search_results) > 0:
        # 검색 결과에서 첫 번째 동영상의 URL 추출하기
        video_url=f"https://www.youtube.com{search_results[0]['url_suffix']}"
        # 유튜브 내려받기 옵션 지정하기
        ydl_opts={
            'format': 'bestaudio/best', # 최상의 오디오 품질로 내려받기
            'postprocessors': [{ # 추출한 오디오 파일을 MP3 형식으로 변환하기
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320', # 비트율은 320으로 지정하기
            }],
            'ffmpeg_location': './ffmpeg-6.0-full_build/bin', 
            'outtmpl': f"{title} – {artist}.%(ext)s", # 내려받은 파일의 이름 설정하기
            'quiet': True, # 내려받는 도중에 출력되는 로그 숨기기
        }
        # yt_dlp 라이브러리를 이용해 동영상 내려받기
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        # 내려받기가 끝나면 메시지 출력하기
        print(f"Downloaded {title} by {artist}")
    else:
        # 검색 결과가 없으면 메시지 출력하기
        print(f"Could not find {title} by {artist}")

# billboard_no1.csv 파일을 읽어서 각 행을 처리하는 코드
with open('./playlist/billboard.csv', 'r', encoding='utf-8') as csvfile:
    # csv.DictReader를 이용해 CSV 파일 읽기
    reader=csv.DictReader(csvfile, delimiter=';')
    # 각 행마다 반복해서 download_song 함수 호출하기
    for row in reader:
        # 노래 제목과 아티스트 정보 추출하기
        title=row['Title']
        artist=row['Artist']
        # download_song 함수 호출하기
        download_song(title, artist)