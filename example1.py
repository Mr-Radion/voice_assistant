import random
import time
import pyaudio
import wave
import speech_recognition as sr
import os
import subprocess
import shlex
# import playsound

from gtts import gTTS


def listen_command():
    # speech_recognition для распознавания речи (аудио -> в текст)
    # альтернатива pocketsphinx
    # https://pypi.org/project/pocketsphinx/
    r = sr.Recognizer()
    # source микрофон с которого мы ожидаем, что скажет нам человек
    with sr.Microphone(device_index=1) as source:
        print('Скажите что-нибудь')
        audio = r.listen(source)
    try:
        our_speech = r.recognize_google(audio, language="ru-RU")
        print('Вы сказали ' + our_speech)
        return our_speech
    except sr.UnknownValueError:
        return 'ошибка1'
    except sr.RequestError as e:
        return 'ошибка2'
    return input('Скажите вашу команду ')


def do_this_command(message):
    message = message.lower()  # приводим команды в нижний регистр
    if 'привет' in message:
        say_message('Привет друг!')  # ответ, который должен произвести на команду - голосовой помощник
    elif 'пока' in message:
        say_message('Пока!')
        exit()  # для прерывания кода и выхода из цикла while
    else:
        say_message('Не распознана!')


# преобразование текста в аудио, далее сохраним файл, чтобы потом проиграть
# альтернатива pyttsx3
def say_message(message):
    # конвертация текстового сообщения в аудио файл, с помощью гугл сервиса gTTS
    voice = gTTS(message, lang='ru')
    # генерируем уникальны идентификатор
    file_voice_name = "_audio_" + str(time.time()) + "_" + str(random.randint(0, 100000)) + ".mp3"
    # file_voice_name = "sound.wav"
    # сохраняем файл
    voice.save("./statics/audio/" + file_voice_name)
    # можно внести поправку, чтобы удалять аудио, после воспроизведения, в функции воспроизведения
    # audio_playback(file_voice_name)
    print("Голосовой асистент: " + message)


# воспроизведение аудио
# вместо playsound использовать модуль из файла примера pya.py
# def audio_playback(file_name):
#     # time.sleep(15)
#     playsound.playsound("./statics/audio/" + file_name)

# версия 2, тоже не срабатывает вероятно из-за формата самой записи неподходящей в 64 битной версии?
# создаваемой с помощью gtts
# def audio_playback(file_name):
#     CHUNK = 1024
#
#     p = pyaudio.PyAudio()
#     wf = wave.open("./statics/audio/" + file_name, 'rb')
#
#     stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#                     channels=wf.getnchannels(),
#                     rate=wf.getframerate(),
#                     output=True)
#
#     data = wf.readframes(CHUNK)
#
#     while data != '':
#         stream.write(data)
#         data = wf.readframes(CHUNK)
#
#     stream.stop_stream()
#     stream.close()
#
#     p.terminate()

# версия 3
# модули os, subprocess, shlex они имено запускают приложения, в чем проблема, появляется проигрыватель сам
# хорошо подходит для запуска внешних программ
# https://pythonworld.ru/moduli/modul-os.html
# def audio_playback(file_name):
    # вариант 1. если в названии присутствуют пробелы, обернуть в другие кавычки это название
    # os.system(f"{os.getcwd()}/statics/audio/{file_name}")
    # вариант 2. чтобы не мучится с пробелами в названии, вместо system используем startfile и он хорош
    # os.startfile(f"{os.getcwd()}/statics/audio/{file_name}")
    # вариант 3. для запуска внешних приложений через консоль например
    # но тут запуск команд через консоль
    # cmd = 'ls -al'  # на линуксе
    # cmd = 'cmd -h'  # на винде
    # args = shlex.split(cmd)
    # p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # result = p.communicate()[0]
    # print(result)
    # вариант 4. то же но под другим соусом(с переводом тарабарщины на русский)
    # cmd = 'ping 8.8.8.8'
    # p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    # result = p.communicate()[0]
    # print(result.decode('cp866'))  # перевели на русские символы


# if __name__ == '__main__':


while True:  # бесконечно перезапускает эти функции друг за другом, пока не прервать
    # слушаем команду пользователя
    command = listen_command()
    do_this_command(command)  # обработчик команды пользователя
