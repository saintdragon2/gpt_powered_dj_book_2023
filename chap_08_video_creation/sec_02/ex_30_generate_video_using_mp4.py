import pandas as pd
import moviepy.editor as mp
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.VideoClip import TextClip
import os
import time

def create_text_clip(text, fontsize, duration, position, start):
    text_clip=TextClip(text, fontsize=fontsize, color='white', font='Malgun-Gothic-Bold')
    text_clip=text_clip.set_position(position).set_duration(duration).set_start(start)
    return text_clip

def combine_videos_and_music(mp3_files, video_files, titles, artists, output_filename):
    # 영상 파일 합치기
    video_clips=[mp.VideoFileClip(video_file) for video_file in video_files]
    concat_video=mp.concatenate_videoclips(video_clips)

    # 음악 파일 합치기
    audio_clips=[mp.AudioFileClip(mp3_file) for mp3_file in mp3_files]
    concat_audio=mp.concatenate_audioclips(audio_clips)

    # 하나로 합친 동영상의 길이와 플레이리스트 길이 비교하기
    video_duration=concat_video.duration
    audio_duration=concat_audio.duration

    if video_duration > audio_duration:
        concat_video=concat_video.subclip(0, audio_duration)
    while video_duration < audio_duration:
        remainder=audio_duration - video_duration
        if remainder > video_duration:
            remainder=video_duration
        extra_video=concat_video.subclip(0, remainder)
        concat_video=mp.concatenate_videoclips([concat_video, extra_video])

        video_duration=concat_video.duration
        audio_duration=concat_audio.duration

    # 영상의 소리를 없애고 플레이리스트로 대체하기
    concat_video=concat_video.set_audio(concat_audio)
    
    # 곡 제목과 아티스트명 표기하기
    text_clips=[]
    start_time=0

    # 영상의 가로, 높이 크기에 따라 글자 크기 설정하기
    video_width, video_height=concat_video.size
    title_font_size=int(video_height * 0.05) 
    artist_font_size=int(title_font_size * 0.8)
    left_margin=title_font_size
    title_y=int(video_height * 0.7)
    artist_y=int(title_y + title_font_size * 1.2)

    for idx, audio_clip in enumerate(audio_clips):
        title_text=create_text_clip(titles[idx], title_font_size, audio_clip.duration, (left_margin, title_y), start_time)
        artist_text=create_text_clip(artists[idx], artist_font_size, audio_clip.duration, (left_margin, artist_y), start_time)
        
        text_clips.append([title_text, artist_text])

        start_time +=audio_clip.duration

    composite_clips=[concat_video] + [text for text_group in text_clips for text in text_group]
    final_video=CompositeVideoClip(composite_clips)
    
    # 결과 저장하기
    encoding_start_at=time.time()
    final_video.write_videofile(output_filename, audio_codec='aac')
    encoding_finish_at=time.time()

    print(encoding_start_at)
    print(encoding_finish_at)
    time_passed=encoding_finish_at - encoding_start_at
    print(f'{time_passed} sec')
    print(f'{time_passed // 60} min \t {time_passed % 60} sec')
    
    return output_filename

def generate_video_using_mp4(csv_file_path, video_files):
    df_playlist=pd.read_csv(csv_file_path, sep=';')
    mp3_files=df_playlist['mp3']
    titles=df_playlist['Title']
    artists=df_playlist['Artist']

    # CSV 파일명을 이용해 동영상 파일명 만들기
    dir, file_full_name=os.path.split(csv_file_path)    # 경로와 파일명 분리하기
    file_name, ext=os.path.splitext(file_full_name)    # 파일명과 확장자 분리하기
    video_file_path =f'./videos/{file_name}.mp4'

    return combine_videos_and_music(mp3_files, video_files, titles, artists, video_file_path)


if __name__  ==  '__main__':
    video_files=[
        './videos/dji/DJI_20230502091254_0073_D_1000_1080.MP4',
        './videos/dji/DJI_20230502091254_0073_D_1015_1080.MP4'
    ]

    csv_file_path='./playlist/2010년대 댄스음악.csv'

    video_file_path=generate_video_using_mp4(csv_file_path, video_files)
    print(video_file_path)
