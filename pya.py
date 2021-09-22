import pyaudio
import wave
import sys

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5  # сколько секунд записываем
WAVE_OUTPUT_FILENAME = "./statics/audio/output.wav"  # в какой файл записываем
INDEX_STREAM = 1  # индекс входного устройства, которое мы будем использовать

p = pyaudio.PyAudio()

# выводим список устройств для дальнейшей выборочной индексации в качестве записывающего устройства
# for i in range(p.get_device_count()):
#     print(i, p.get_device_info_by_index(i)['name'])

"""PyAudio example: Record a few seconds of audio and save to a WAVE file."""
# Запись аудио
# http://people.csail.mit.edu/hubert/pyaudio/docs/

# открываем поток и указываем параметры записи
# stream = p.open(format=FORMAT,
#                 channels=CHANNELS,
#                 rate=RATE,
#                 input_device_index=INDEX_STREAM,
#                 input=True,
#                 frames_per_buffer=CHUNK)
#
# print("* recording")
#
# frames = []
#
# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     frames.append(data)
#
# print("* done recording")
#
# stream.stop_stream()  # останавливаем поток
# stream.close()  # закрываем
# p.terminate()  # прекращаем работу с устройством
#
# wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
# wf.setnchannels(CHANNELS)
# wf.setsampwidth(p.get_sample_size(FORMAT))
# wf.setframerate(RATE)
# wf.writeframes(b''.join(frames))
# wf.close()

# Воспроизведение аудио

# if len(sys.argv) < 2:
#     print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
#     sys.exit(-1)

# wf = wave.open(sys.argv[1], 'rb')
# 2
wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

data = wf.readframes(CHUNK)

while data != '':
    stream.write(data)
    data = wf.readframes(CHUNK)

stream.stop_stream()
stream.close()

p.terminate()
