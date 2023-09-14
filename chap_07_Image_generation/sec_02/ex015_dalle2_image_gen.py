import openai
import os

openai.api_key='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'

PROMPT="Ferrari is cruising through the big city at night."

response=openai.Image.create(
    prompt=PROMPT,
    n=1,             # 몇 개의 이미지를 생성할지
    size="512x512",  # 해상도(256256, 512512, 102401024 등 선택 가능)
)

print(response["data"][0]["url"])
