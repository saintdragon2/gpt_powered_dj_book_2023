import moviepy.editor as mp

def combine_video_and_music(mp3_files, video_files):
    # 영상 파일 합치기
    video_clips=[mp.VideoFileClip(video_file) for video_file in video_files]
    concat_video=mp.concatenate_videoclips(video_clips)

    # 음악 파일 합치기
    audio_clips=[mp.AudioFileClip(video_file) for video_file in video_files]
    concat_audio=mp.concatenate_videoclips(audio_clips)

    # 하나로 합친 동영상의 길이와 플레이리스트 길이 비교하기
    video_duration=concat_video.duration
    audio_duration=concat_audio.duration

    if video_duration > audio_duration: 
        concat_video=concat_video.subclip(0, audio_duration)
    elif video_duration < audio_duration:
        remainder = audio_duration - video_duration
        extra_video=concat_video.subclip(0, remainder)
        concat_video=mp.concatenate_videoclips([concat_video, extra_video])

    # 영상의 소리를 없애고 플레이리스트로 대체하기
    concat_video=concat_video.set_audio(concat_audio)

    # 결과 저장하기
    output_filename="conbined_video.mp4"
    concat_video.write_videofile(output_filename)

    return output_filename



