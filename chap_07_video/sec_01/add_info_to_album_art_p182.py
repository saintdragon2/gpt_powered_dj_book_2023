from PIL import Image, ImageDraw, ImageFont

def create_album_art(image_path, title, artist):
    # 이미지 열기
    img=Image.open(image_path)
 
    # 이미지 크기 구하기
    width, height=img.size
    
    # 드로잉 객체 생성하기
    draw=ImageDraw.Draw(img)
    
    # 텍스트의 크기 설정하기
    title_font_size=int(height * 0.07)
    artist_font_size=int(height * 0.05)
 
    # 글꼴 설정하기
    title_font=ImageFont.truetype("malgun.ttf", title_font_size)
    artist_font=ImageFont.truetype("malgun.ttf", artist_font_size)
 
    # 텍스트 색상 설정하기(흰색)
    text_color=(255, 255, 255)
    
    # 제목의 위치 계산하기
    title_width, title_height=draw.textsize(title, font=title_font)
    title_x=(width - title_width) / 2
    title_y=(height - title_height) * 0.4

    # 아티스트명의 위치 계산하기
    artist_width, artist_height=draw.textsize(artist, font=artist_font)
    artist_x=(width - artist_width) / 2
    artist_y=(height - artist_height) * 0.55
    
    # 텍스트 그리기
    draw.text((title_x, title_y), title, font=title_font, fill=text_color)
    draw.text((artist_x, artist_y), artist, font=artist_font, fill=text_color)
 
    # 결과 이미지 저장하기
    img.save(f"{title}_{artist}_album_art.jpg")
    
# 사용 예시
create_album_art("./dreamlike_diffusion/New_York__New_York_Frank_Sinatra.jpg", "곡 제목", "아티스트명")