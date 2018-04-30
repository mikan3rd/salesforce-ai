import requests

import settings

KEY1 = settings.KEY1

endpoint = 'https://eastasia.api.cognitive.microsoft.com/vision/v1.0/ocr'

image_url = "https://bazubu.com/wp-content/uploads/2013/03/7dec493403292ee13268a2a283d92c151.png"
image_url2 = "https://upload.wikimedia.org/wikipedia/commons/5/57/Lorem_Ipsum_Helvetica.png"
image_url3 = "https://datumstudio.jp/wp-content/uploads/2018/01/pexels-photo-800721-1024x678.jpeg"


def get_text_by_ms(url):
    headers = {
        'Ocp-Apim-Subscription-Key': KEY1,
        'Content-Type': 'application/json',
    }
    params = {'visualFeatures': 'Categories,Description,Color'}
    data = {'url': url}
    response = requests.post(
        endpoint,
        headers=headers,
        params=params,
        json=data
    )
    data = response.json()
    # pprint(data)

    text = ''
    for region in data['regions']:
        for line in region['lines']:
            for word in line['words']:
                text += word.get('text', '')
                if data['language'] != 'ja':
                    text += ' '
        text += '\n'

    if len(text) == 0:
        text += '文字が検出できませんでした'

    print('text:', text)
    return text


if __name__ == "__main__":
    get_text_by_ms(image_url)
