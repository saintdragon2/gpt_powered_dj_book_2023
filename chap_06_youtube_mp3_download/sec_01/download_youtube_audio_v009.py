import csv               # CSV 파일 처리를 위한 모듈
from youtube_search import YoutubeSearch   # Youtube 검색 모듈
import yt_dlp            # Youtube 다운로드 모듈

def download_song(title, artist):
    # 노래 제목과 아티스트 정보를 이용하여 검색할 쿼리 생성
    query = f"{title} {artist} audio"
    # YoutubeSearch 모듈로 쿼리에 대한 검색 결과를 리스트로 받아옴
    search_results = YoutubeSearch(query, max_results=1).to_dict()

    # 검색 결과가 존재하면
    if len(search_results) > 0:
        # 검색 결과에서 첫 번째 동영상의 URL 추출
        video_url = f"https://www.youtube.com{search_results[0]['url_suffix']}"

        # Youtube 다운로드 옵션 지정
        ydl_opts = {
            'format': 'bestaudio/best',   # 최상의 오디오 품질로 다운로드
            'postprocessors': [{          # 추출한 오디오 파일을 mp3 형식으로 변환
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320', # 비트율은 320로 지정
            }],
            'ffmpeg_location': './ffmpeg-6.0-full_build/bin',  
            'outtmpl': f"{title} – {artist}.%(ext)s", # 다운로드 된 파일의 이름 설정
            'quiet': True,  # 다운로드 중에 출력되는 로그를 숨김
        }

        # yt_dlp 라이브러리를 이용하여 동영상 다운로드 실행
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # 다운로드가 완료되면 메시지 출력
        print(f"Downloaded {title} by {artist}")
    else:
        # 검색 결과가 없으면 메시지 출력
        print(f"Could not find {title} by {artist}")

# billboard_no1.csv 파일을 읽어서 각 행을 처리하는 코드
with open('./playlist/billboard.csv', 'r', encoding='utf-8') as csvfile:
    # csv.DictReader를 이용하여 CSV 파일을 읽음
    reader = csv.DictReader(csvfile, delimiter=';')
    # 각 행에 대해 반복적으로 download_song 함수 호출
    for row in reader:
        # 노래 제목과 아티스트 정보 추출
        title = row['Title']
        artist = row['Artist']
        # download_song 함수 호출
        download_song(title, artist)
