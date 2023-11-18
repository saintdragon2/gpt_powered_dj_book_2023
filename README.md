# Do it! 챗GPT & 파이썬으로 AI 직원 만들기
- GPT로 나만의 플레이리스트 제작 프로그램 만들기

## 책 구매처
- [교보문고](https://product.kyobobook.co.kr/detail/S000210892321)
- [yes24](https://www.yes24.com/Product/Goods/123278667)
- [알라딘](https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=327940197)

## 공지
### 이 책에서 사용한 패키지 버전

이 책은 2023년은 11월 10일에 출판되었었습니다. 책이 출판되기 직전인 11월 6일에 openai의 DEVDAY행사와 함께 API 버전 1.1.1으로 업데이트 되면서 API 사용 코드가 예고 없이 일부 수정되었습니다. 

이 책의 코드 그대로 사용하고 싶으신 분들은 openai 패키지를 설치 할 때 버전 정보를 0.28.1로 설치하시면 됩니다. 

```terminal
> pip install openai==0.28.1
```
혹은 이 저장소에 `requirements.txt`로 정리해둔 패키지 버전 정보를 이용하여 사용하시면 책에서 사용한 환경과 동일하게 진행하실 수 있습니다. 
```terminal
> pip install -r requirements.txt
```


아래는 1.1.1 이후 버전에서 Chat completion을 하는 예제입니다. 최신 버전을 사용하고 싶으신 분들은 아래 공식 문서의 가이드를 참고하여 진행하시면 됩니다. 
```python
# openai==1.1.1
from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]
)

print(completion.choices[0].message)

```

## 책에 관한 문의사항
책을 읽으시면서 혹은 코드를 보면서 궁금하거나 의견을 나누고 싶으신 분들은 이 깃허브 저장소에 의견을 올려주시거나 아래 공간을 이용하시면 됩니다. 
- 저자 홈페이지: https://sungyonglee.com 
- https://cafe.naver.com/doitstudyroom 



![책](readme_imgs\i9791163035237.jpg)