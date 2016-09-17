import speech_recognition as sr
import subprocess


def recognize(bot, file_id):
    file = get_file_by_id(bot, file_id)
    text = transcribe(file)
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
    return open("./temp.wav", "rb")


def transcribe(file):
    r = sr.Recognizer()
    with sr.AudioFile(file) as source:
        audio = r.record(source)

    try:
        result = []
        result.append(r.recognize_bing(audio, "b36426a2b335437eb3ce005c840553fe", language="ru-RU"))
        return " ".join(result)
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(e)
        return None


