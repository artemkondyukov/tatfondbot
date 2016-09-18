import speech_recognition as sr
import subprocess
import os
from pocketsphinx import AudioFile


def recognize(bot, file_id, sphinx):
    file = get_file_by_id(bot, file_id)
    text = transcribe(file, sphinx)
    print(text)
    return text


def get_file_by_id(bot, file_id):
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    print(type(downloaded_file))
    with open("./temp.ogg", "wb") as output:
        output.write(downloaded_file)
    subprocess.run(["rm", "./temp.wav"])
    subprocess.run(["/usr/local/bin/ffmpeg", "-i", "./temp.ogg", "./temp.wav"])
    # return open("./temp.wav", "rb")
    return "./temp.wav"


def transcribe(file, sphinx):
    r = sr.Recognizer()
    with sr.AudioFile(file) as source:
        audio = r.record(source)

    # sphinx.start_utt()
    # stream = open("./model/zero/decoder-test.wav", 'rb')
    # while True:
    #     buf = stream.read(1024)
    #     if buf:
    #         sphinx.process_raw(buf, False, False)
    #     else:
    #         break
    # sphinx.end_utt()

    # print(r.recognize_sphinx(audio, language="ru-RU"))

    # print(sphinx.decode(file, buffer_size=2048, no_search=False, full_utt=False))
    # print(sphinx.segments(detailed=True))

    try:
        result = [r.recognize_bing(audio, "b36426a2b335437eb3ce005c840553fe", language="ru-RU")]
        return " ".join(result)
        # return "ЫЫЫЫЫ"
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(e)
        return None


