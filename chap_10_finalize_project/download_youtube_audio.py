import csv               # CSV 파일 처리를 위한 모듈
from youtube_search import YoutubeSearch   # Youtube 검색 모듈
import yt_dlp            # Youtube 다운로드 모듈
import re
import os

# 비디오 제목이 노래 제목과 아티스트와 관련이 있는지 확인하는 함수
def is_relevant_video_title(video_title, song_title, song_artist):
    # 문자열을 소문자로 변환하기
    video_title=video_title.lower()
    song_title=song_title.lower()
    song_artist=song_artist.lower()

    # 노래 제목과 아티스트의 단어 나누기
    title_words=song_title.split()
    artist_words=song_artist.split()

    # 비디오 제목에 노래 제목과 아티스트의 단어가 얼마나 포함되어 있는지 확인하기
    title_matches=sum([word in video_title for word in title_words])
    artist_matches=sum([word in video_title for word in artist_words])

    # 일치하는 단어의 비율이 일정 수준 이상이면 관련성이 있다고 판단하기
    return title_matches >= len(title_words) * 0.5 and artist_matches >= len(artist_words) * 0.5

# 파일명에서 부적절한 문자를 제거하고 공백 문자를 대체하는 함수
def sanitize_filename(filename):
    return re.sub('[\\\\/:*?"<>|].', '', filename).replace(' ', '_')

def download_song(title, artist):
    # 노래 제목과 아티스트 정보를 이용하여 검색할 쿼리 생성
    query = f"{title} {artist} audio"
    # YoutubeSearch 모듈로 쿼리에 대한 검색 결과를 리스트로 받아옴
    search_results = YoutubeSearch(query, max_results=5).to_dict()

    # 파일명 정리하기
    file_name = sanitize_filename(f'{title}__{artist}')

    # 검색 결과에서 관련성이 있는 동영상 찾기
    for searched in search_results:
        video = searched
        video_url = f"https://www.youtube.com{searched['url_suffix']}"

        # Youtube 다운로드 옵션 지정
        if is_relevant_video_title(video['title'], title, artist):
            ydl_opts = {
                'format': 'bestaudio/best',   # 최상의 오디오 품질로 다운로드
                'postprocessors': [{          # 추출한 오디오 파일을 mp3 형식으로 변환
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320', # 비트율은 320로 지정
                }],
                'ffmpeg_location': './ffmpeg-6.0-full_build/bin',  
                'outtmpl': f"./mp3/{file_name}.%(ext)s",
                'quiet': True,  # 다운로드 중에 출력되는 로그를 숨김
            }

            # yt_dlp 라이브러리를 이용하여 동영상 내려 받기
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

            # 파일 경로 반환하기
            return f"./mp3/{file_name}.mp3"
    # 관련성 있는 동영상이 없으면 None 반환하기
    return None

# CSV 파일에 있는 노래들을 내려받는 함수
def download_songs_in_csv(csv_file):
    result_dict=dict()

    # CSV 파일 열기
    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        # 세미콜론으로 구분된 CSV 파일 읽기
        reader = csv.DictReader(csvfile, delimiter=';')

        if 'mp3' not in reader.fieldnames:
            # 필드명 가져오기
            fieldnames = reader.fieldnames + ['mp3']
        else:
            fieldnames = reader.fieldnames

        # 결과를 저장할 새 CSV 파일 생성하기
        temp_ouptut_file=csv_file.replace('.csv', '__temp.csv')
        with open(temp_ouptut_file, 'w', encoding='utf-8', newline='') as output_csvfile:
            # 작성자 객체 생성하고 필드명 사용하기
            writer = csv.DictWriter(output_csvfile, fieldnames=fieldnames, delimiter=';')
            # 헤더 작성하기
            writer.writeheader()

            # CSV 파일의 각 행에서 반복하기
            for row in reader:
                # 제목과 아티스트 가져오기
                title = row['Title']
                artist = row['Artist']
                # 노래를 내려받고 파일 경로 가져오기
                filepath = download_song(title, artist)

                # 파일 경로가 있으면 파일 경로를 저장하고 그렇지 않으면 "Not found" 저장하기
                if filepath:
                    row['mp3'] = filepath
                    result_dict[f'{title} - {artist}'] = filepath
                else:
                    row['mp3'] = "Not found"
                    result_dict[f'{title} - {artist}'] = 'Not found'

                # 새로운 CSV 파일에 행 작성하기
                writer.writerow(row)
                
    # 원본 input_file 삭제하고 temp_output_file의 이름을 input_file로 바꾸기
    os.remove(csv_file)
    os.rename(temp_ouptut_file, csv_file)
    
    return result_dict

if __name__ == '__main__':
    # 입력 파일의 경로 설정하기
    file_path='./playlist/korean_80s_rock.csv'
    # CSV 파일에 있는 노래 내려받기
    result=download_songs_in_csv(file_path)
    for k, r in result.items():
        print(k, r)
