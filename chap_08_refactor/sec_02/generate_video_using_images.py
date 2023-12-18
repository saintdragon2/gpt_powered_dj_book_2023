import os
from moviepy.editor import *
import pandas as pd
from generate_image import generate_images_for_songs

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
    
    if 'info_image_file' not in df_playlist.columns:
        generate_images_for_songs(csv_file)
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

def merge_videos(video_paths, output_path):
    # 비디오 합치기
    clips=[VideoFileClip(v) for v in video_paths]
    final_clip=concatenate_videoclips(clips)
    
    # 동영상 저장하기
    final_clip.write_videofile(output_path)
    
    # 메모리 해제하기
    final_clip.close()
    
    for clip in clips:
        clip.close()
    
    return output_path

def generate_video_using_images(csv_file):
    videos=create_videos_from_playlist_csv(csv_file)
 
    # CSV 파일명을 이용해 동영상 파일명 만들기
    dir, file_full_name=os.path.split(csv_file) # 경로와 파일명 분리하기
    file_name, ext=os.path.splitext(file_full_name) # 파일명과 확장자 분리하기
    video_file_path=f'./videos/{file_name}.mp4'
 
    merge_videos(videos, video_file_path)
    return video_file_path

if __name__ == '__main__':
    video_file_path = generate_video_using_images('./playlist/2010s_hiphop.csv')
    print(video_file_path)
    