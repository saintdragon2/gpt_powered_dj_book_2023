from dalle2_image_gen import generate_dalle_image
from dreamlike_diffusion_image_gen import generate_dreamlike_image
from add_info_to_album_art import create_album_art
import pandas as pd
import torch
import time


def generate_images_for_songs(csv_file):
    df_playlist=pd.read_csv(csv_file, sep=';')
   
    is_cuda_or_mps_available=torch.cuda.is_available() or torch.backends.mps.is_available()
   
    image_file_path=list()
    info_image_file_path=list()
   
    response_str='다음 곡의 이미지를 생성했습니다.'
   
    for i, row in df_playlist.iterrows():
        if row['mp3'] == 'Not found':
            image_file_path.append(None)
            info_image_file_path.append(None)
        else:
            if is_cuda_or_mps_available:
                image_file=generate_dreamlike_image(row['Title'], row['Artist'])
            else:
                try:
                    image_file=generate_dalle_image(row['Title'], row['Artist'])
                except:
                    print('Something went to wrong...')
                    image_file=None
                time.sleep(5)
            image_file_path.append(image_file)

            info_image_file=create_album_art(image_file, row['Title'], row['Artist'])
            info_image_file_path.append(info_image_file)
 
            response_str+=f'\n{row["Title"]}\t{row["Artist"]}\t{image_file}'
 
    df_playlist['image_file']=image_file_path
    df_playlist['info_image_file']=info_image_file_path

    df_playlist.to_csv(csv_file, sep=';', index=False)
    
    return response_str


if __name__ == '__main__':
    generate_images_for_songs('./playlist/2010s_hiphop.csv')