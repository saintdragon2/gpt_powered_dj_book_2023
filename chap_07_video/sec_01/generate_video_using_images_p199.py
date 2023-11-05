import os
from moviepy.editor import *
import pandas as pd

def create_video(mp3_path, img_path):
    # 오디오 파일과 이미지 파일 열기
    audio_clip=AudioFileClip(mp3_path)
    image_clip=ImageClip(img_path)
    
    # 이미지를 오디오 길이에 맞게 반복하기
    image_clip=image_clip.set_duration(audio_clip.duration).loop()
    
    # 동영상 생성하기
    video_clip=CompositeVideoClip([image_clip], size=image_clip.size)
    video_clip=video_clip.set_audio(audio_clip)
    
    # 이미지 파일명을 이용해 동영상 파일명 만들기
    dir, img_file_full_name=os.path.split(img_path) # 경로와 파일명 분리하기
    file_name, ext=os.path.splitext(img_file_full_name) # 파일명과 확장자 분리하기
 
    print(dir)

    print(img_file_full_name)
    print(file_name)
    
    # 동영상 저장하기
    video_path=f"./videos/{file_name}.mp4"
    video_clip.write_videofile(video_path, fps=24)
    
    return os.path.abspath(video_path)

def create_videos_from_playlist_csv(csv_file):
    df_playlist=pd.read_csv(csv_file, sep=';')
    videos=list()
    
    for i, row in df_playlist.iterrows():
        if row['mp3'] != 'Not found':
            video=create_video(
                row['mp3'],
                row['info_image_file']
            )
        videos.append(video)
    
    return videos

if __name__ == '__main__':
    videos=create_videos_from_playlist_csv('./playlist/2010s_hiphop.csv')
    for v in videos:
        print(v)