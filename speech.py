# распознание речи по голосу опр человека
import speech_recognition as sr


# print(sr.__version__)
# выводим поключенные микрофоны по их индексам
# 1 способ (надежный)
# в этом способе индексы справа
# чтобы посмотреть список устройств звуковых и выбрать нужный индекс
# имено с этого устройства будет произведена запись
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

# 2 способ
# list_mic = sr.Microphone.list_microphone_names()
# for i in range(0, len(list_mic)):
#     print(i, list_mic[i])

def speech_r():
    # преобразование аудио в текст
    r = sr.Recognizer()
    # source микрофон с которого мы ожидаем, что скажет нам человек
    with sr.Microphone(device_index=1) as source:
        print('Скажите что-нибудь')
        audio = r.listen(source)
    # результат ответа на русском и обработка ошибок
    # recognize speech using Google Speech Recognition

    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        query = r.recognize_google(audio, language="ru-RU")
        print("Google Speech Recognition thinks you said " + query.lower())
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


speech_r()
# Использует Microsoft Bing Speech API
# r.recognize_bing()
# использует Google Cloud
# r.recognize_google_cloud()
# использует Houndify API от SoundHound
# r.recognize_houndify()
# использует IBM Speech to Text API
# r.recognize_ibm()
# использует PocketSphinx API
