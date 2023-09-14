import openai
from pathlib import Path
from base64 import b64decode

def generate_dalle_image(prompt, image_file_name):
    # OpenAI API 키 설정하기
    openai.api_key='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'

    # 이미지를 저장할 디렉터리 설정하고 해당 디렉터리 생성하기
    DATA_DIR=Path.cwd() / 'dalle2_results'
    DATA_DIR.mkdir(exist_ok=True)

    # 디렉터리 경로 출력하기
    print(DATA_DIR)

    # OpenAI API 사용해 이미지 생성 요청하기
    response=openai.Image.create(
        prompt=prompt,
        n=1,             # 생성할 이미지의 개수 지정하기
        size="512x512",  # 이미지 해상도 지정하기 (예) 256256, 512512 등
        response_format='b64_json'  # 응답 형식을 Base64로 인코딩된 JSON 파일로 지정하기
    )

    # 생성된 이미지의 파일명 설정하기
    file_name=DATA_DIR / f"{image_file_name}.png"

    # 응답에서 Base64로 인코딩된 이미지 데이터 추출하기
    b64_data=response['data'][0]['b64_json']

    # Base64 이미지 데이터를 디코딩해 바이너리 형식으로 변환하기
    image_data=b64decode(b64_data)

    # 이미지를 저장할 파일 경로 지정하기
    image_file=DATA_DIR / f'{file_name}'

    # 디스크에 이미지 파일 저장하기
    with open(image_file, mode='wb') as png:
        png.write(image_data)

    return image_file

generate_dalle_image('A man is dancing in the night in the middle of Gangnam, Seoul', 'dancing_man')
