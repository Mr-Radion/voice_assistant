import requests

URL_AUTH = 'https://developers.lingvolive.com/api/v1.1/authenticate'
URL_TRANSLATE = 'https://developers.lingvolive.com/api/v1/Minicard'
API_KEY = 'MjU5NGU1ZjMtODQ3ZS00OTFhLWEwZjctOTYzZTc3NDUwOWI0OjdjOThjZDFkY2Q4OTRkMmNhZWE1YjY1YWYzOGZlYjEx'

headers_auth = {'Authorization': 'Basic ' + API_KEY}

auth = requests.post(URL_AUTH, headers=headers_auth)


def english_to_russian():
    if auth.status_code == 200:
        token = auth.text
        while True:
            word = input('Введите слово для перевода: ')
            print(word)
            if word:
                headers_translate = {'Authorization': 'Bearer ' + token}
                params = {'text': word, 'srcLang': 1033, 'dstLang': 1049}
                r = requests.get(URL_TRANSLATE, headers=headers_translate, params=params)
                res = r.json()
                try:
                    print(res['Translation']['Translation'])
                except:
                    print('Не найден вариант для перевода')
    else:
        print('Error!')
