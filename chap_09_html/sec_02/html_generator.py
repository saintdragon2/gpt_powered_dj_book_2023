import os
import pandas as pd

def create_html(csv_file, youtube_title, youtube_description):
    df = pd.read_csv(csv_file, sep=';')

    html=f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{youtube_title}</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    </head>

    <body>
    <div class="container">
    <h1>{youtube_title}</h1>
    <hr/>
    <p>{youtube_description}</p>
    <hr/>
    """

    for i in range(0, len(df), 2):
        html += '<div class="row">\n'
        for j in range(i, min(i + 2, len(df))):
            row=df.iloc[j]
            html += f"""
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
        html += "</div>\n"


    html += """
    </div>
    </body>

    </html>
    """

    # HTML 파일 저장하기
    html_file = os.path.basename(csv_file).replace('.csv', '.html')
    with open(html_file, 'w', encoding='UTF-8') as f:
        f.write(html)

    return f'\n{html_file}에 HTML 파일을 저장했습니다.'

if __name__ == '__main__':
    create_html(
        './playlist/eric_clapton.csv',
        'Eric Clapton Best',
        'Eric Clapton의 명곡들을 추천해드립니다. Layla, Tears in Heaven, Wonderful Tonight 등 Eric Clapton의 기타와 노래를 감상해보세요.'
    )