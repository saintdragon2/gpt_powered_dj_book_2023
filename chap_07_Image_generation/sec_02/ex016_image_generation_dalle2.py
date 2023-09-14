import openai
import json
from pathlib import Path

openai.api_key='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'

PROMPT="Ferrari is cruising through the big city at night."
DATA_DIR=Path.cwd() / 'dalle2_results'    # ① 폴더 추가
DATA_DIR.mkdir(exist_ok=True)
print(DATA_DIR)

response=openai.Image.create(
    prompt=PROMPT,
    n=1,             # 몇 개의 이미지를 생성할지
    size="512x512",  # 해상도(256256, 512512, 102401024 등 선택 가능)
    response_format='b64_json' # ② Base64 형태로 받기
)

# ③ 파일명 생성하기
file_name=DATA_DIR / f"{PROMPT[:5]}-{response['created']}.json"

# ④ JSON 파일로 저장하기
with open(file_name, mode='w', encoding='UTF-8') as file:
    json.dump(response, file)
