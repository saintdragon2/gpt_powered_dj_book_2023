# 필요한 라이브러리 임포트하기
from diffusers import StableDiffusionPipeline
import torch

# 사용할 이미지 생성 모델의 ID 설정하기
model_id="dreamlike-art/dreamlike-diffusion-1.0"

# 사전 훈련된 모델을 로드해 파이프라인을 생성하고 데이터 타입을 float16으로 설정하기
pipe=StableDiffusionPipeline.from_pretrained(model_id)

# 모델을 GPU로 이동하기
pipe=pipe.to("cuda")

# 이미지를 생성하는 프롬프트 설정하기
prompt="dreamlikeart, a grungy woman with rainbow hair, travelling between dimensions, dynamic pose, happy, soft eyes and narrow chin, extreme bokeh, dainty figure, long hair straight down, torn kawaii shirt and baggy jeans, In style of by Jordan Grimmer and greg rutkowski, crisp lines and color, complex background, particles, lines, wind, concept art, sharp focus, vivid colors"

# 프롬프트를 기반으로 모델이 이미지 생성하기
image=pipe(prompt).images[0]

# 생성한 이미지를 "result.jpg" 파일로 저장하기
image.save("./result.jpg")
