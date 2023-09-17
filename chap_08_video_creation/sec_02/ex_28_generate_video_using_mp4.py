import moviepy.editor as mp
import pandas as pd

def combine_videos_and_music(mp3_files, video_files):
    # 영상 파일 합치기
    video_clips=[mp.VideoFileClip(video_file) for video_file in video_files]
    concat_video=mp.concatenate_videoclips(video_clips)

    # 음악 파일 합치기
    audio_clips=[mp.AudioFileClip(mp3_file) for mp3_file in mp3_files]
    concat_audio=mp.concatenate_audioclips(audio_clips)

    # 하나로 합친 동영상의 길이와 플레이리스트의 길이 비교하기
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

    # 결과 저장하기
    output_filename="./combined_video3.mp4"
    concat_video.write_videofile(output_filename)
    
    return output_filename

if __name__  ==  '__main__':
    video_files=[
        './videos/dji/DJI_20230502091254_0073_D_1000_1080.MP4',
        './videos/dji/DJI_20230502091254_0073_D_1015_1080.MP4'
    ]

    df_playlist=pd.read_csv('./playlist/2010년대 댄스음악.csv', sep=';')
    mp3_files=df_playlist['mp3']
    # titles=df_playlist['Title']
    # artists=df_playlist['Artist']
    combine_videos_and_music(mp3_files, video_files)
