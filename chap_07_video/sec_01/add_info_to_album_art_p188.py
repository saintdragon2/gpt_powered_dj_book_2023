from PIL import Image, ImageDraw, ImageFont

def add_text_border(draw, text, position, font, fill, border_width, border_color):
    x, y=position
    for x_offset in range(-border_width, border_width + 1):
        for y_offset in range(-border_width, border_width + 1):
            draw.text((x + x_offset, y + y_offset), text, font=font, fill=border_color)
            draw.text(position, text, font=font, fill=fill)

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
    border_color=(0, 0, 0)
    border_width=2
    
    # 제목의 위치 계산하기
    title_width, title_height=draw.textlength(title, font=title_font), title_font.getsize(title)[1]
    while title_width > width * 0.9:
        title_font_size -= 1
        title_font=ImageFont.truetype("malgun.ttf", title_font_size)
        title_width, title_height=draw.textlength(title, font=title_font), title_font.getsize(title)[1]
    
    title_x=(width - title_width) / 2
    title_y=(height - title_height) * 0.4

    # 아티스트명의 위치 계산하기
    artist_width, artist_height=draw.textlength(artist, font=artist_font), title_font.getsize(title)[1]
    artist_x=(width - artist_width) / 2
    artist_y=(height - artist_height) * 0.55
    
    add_text_border(draw, title, (title_x, title_y), title_font, text_color, border_width, border_color)
    add_text_border(draw, artist, (artist_x, artist_y), artist_font, text_color, border_width, border_color)
 
    # 결과 이미지 저장하기
    img.save(f"{title}_{artist}_album_art.jpg")
    
# 사용 예시
create_album_art("./dreamlike_diffusion/New_York__New_York_Frank_Sinatra.jpg", "Laugh Now Cry Later(feat. Lil Durk)", "Drake")