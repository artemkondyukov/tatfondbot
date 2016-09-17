import speech_recognition as sr


def recognize(bot, file_id):
    file = get_file_by_id(bot, file_id)
    text = transcribe(file)
    return text


def get_file_by_id(bot, file_id):
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    return downloaded_file


def transcribe(file):
    r = sr.Recognizer()
    with sr.AudioFile(file) as source:
        audio = r.record(source)

    try:
        return r.recognize_sphinx(audio)
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None


