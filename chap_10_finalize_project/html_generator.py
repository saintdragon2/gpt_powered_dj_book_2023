import os
import pandas as pd

def create_html(csv_file, youtube_title, youtube_description):
    # CSV 파일 읽기
    df=pd.read_csv(csv_file, sep=';')

    # HTML 시작하기
    html=f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{ youtube_title }</title>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
        </head>
        <body>
        <div class="container">
        <h1>{ youtube_title }</h1>
        <hr/>
        <p>{ youtube_description }</p>
        <hr/>
    """
    
    # 각 행에 HTML 코드 생성하기
    for i in range(0, len(df), 2):
        html +='<div class="row">\n'
        for j in range(i, min(i + 2, len(df))):
            row=df.iloc[j]
            html +=f"""
        <div class="col-md-6">
            <img src="{row['info_image_file']}" class="img-fluid">
            <audio controls>
                <source src="{row['mp3']}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
            <h2>{row['Title']}</h2>
            <p>{row['Artist']}</p>
            <p>{row['Released']}</p>
        </div>
            """
        html +='</div>\n'
    
    # HTML 종료하기
    html +="""
        </div>
        </body>
        </html>
    """

    # HTML 파일 저장하기
    html_file=os.path.basename(csv_file).replace('.csv', '.html')
    with open(html_file, 'w') as f:
        f.write(html)

    return f'\n{html_file}에 HTML 파일을 저장했습니다. '

if __name__  ==  '__main__':
    create_html('./playlist/beatles.csv')
