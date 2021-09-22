import os
import time
import pyttsx3  # модуль для преобразования текста в речь
import speech_recognition as sr  # для преобразования нашей речи в текст альтернатива pyaudio (он работает реалтайм)
from fuzzywuzzy import fuzz  # для нечеткого сравнения
import datetime

# RHVoice для синтеза нескольких вариаций речи асистента https://github.com/RHVoice/RHVoice

# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

# написать код, который будет искать среди устройств, при нескольких
# вариантах предлагать на выбор записывающее устройство
INDEX_STREAM = 1

# словарь асистента
opts = {
    # вариации имени асистента
    "alias": ('альтрон', 'альтрн', 'vision', 'вижэн'),
    # речевые слова человека, которые нужно исключать из речевой команды
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси'),
    # все возможные команды нашего асистента
    "cmds": {
        "ctime": ('текущее время', 'сейчас времени', 'который час', 'времени'),
        "radio": ('включи музыку', 'воспроизведи радио', 'включи радио'),
        "stupid1": ('расскажи анекдот', 'рассмеши меня', 'ты знаешь анекдоты')
    }
}

speak_engine = pyttsx3.init()


def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


# будет запускаться каждый раз, после того, как речь переведет в текст
def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voice)
        # если обратится не по имени, он просто выведет Распознано
        if voice.startswith(opts["alias"]):
            # обращение к асистенту
            cmd = voice

            # удаляем имя само из команды, оставляя только команду
            for x in opts["alias"]:
                cmd = cmd.replace(x, "").strip()

            # удаляем отдельные слова из команды
            for x in opts["tbr"]:
                cmd = cmd.replace(x, "").strip()

            # определяем, что это за команда и выполняем
            print('команда ' + cmd)
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd["cmd"])

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")


# поиск нечетких(разных вариаций) команд, которые получил асистент
# внутри сравниваем полученные команды с командами из cmds команд асистента
def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    return RC


# преобразование команды в какое-то ее действие
# тоесть по сути чистая функция, как свитч кейс
def execute_cmd(cmd):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()

        speak("Сейчас " + str(now.hour) + ':' + str(now.minute))

    # воспроизвести радио
    # elif cmd == "radio":
    #     os.startfile(f"{os.getcwd()}/statics/audio/radio_record.m3u")

    elif cmd == "stupid1":
        # рассказать анекдот
        speak("Мой разработчик не научил меня анекдотам ... Ха-ха")

    else:
        print("Команда не распознана, повторите!")


def listen_command():
    # след 2 строки, только если установлен синтез речи для голоса
    # voices = speak_engine.getProperty('voices')
    # speak_engine.setProperty('voice', voices[4].id)

    # сначала асистент произносит приветственные фразы, только потом начинает слушать микрофон в фоне
    speak('Добрый день, повелитель!')
    speak('Альтрон, слушает!')

    r = sr.Recognizer()
    # source микрофон с которого мы ожидаем, что скажет нам человек
    with sr.Microphone(device_index=INDEX_STREAM) as source:
        r.adjust_for_ambient_noise(source)  # в течении 1 сек слушает фон, чтобы не путать шум с речью человека
        # print('Скажите что-нибудь')
        # audio = r.listen(source)
    stop_listening = r.listen_in_background(source, callback)
    while True:
        time.sleep(0.1)  # бесконечная петля
        # stop_listening()


listen_command()
# while True:
#     # time.sleep(0.1)  # бесконечная петля
#     listen_command()
#     stop_listening()
