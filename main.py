# example to record audio
# stuff for wav file
import sounddevice as sd
import wavio as wv
# text to speech stuff
import speech_recognition as sr
# roku
from roku import Roku
from config import IP_ADDRESS


# records and audio file and saves it to the name givent
def record_wav_file(file_name: str, duration: int):

    # sampling frequency
    freq = 44100

    # start recording
    recording = sd.rec(int(duration * freq), samplerate= freq, channels = 2)

    # record audio for the given number
    sd.wait()

    # write to an audio file
    wv.write(f"{file_name}.wav", recording, freq, sampwidth=2)

# converts a wav file to text
def wav_to_text(file_name:str) -> str:
    r = sr.Recognizer()

    # open wave file
    with sr.AudioFile(file_name) as source:
        # listen for the data
        audio_data = r.record(source)
        # recognize
        try:
            text = r.recognize_google(audio_data)
            return text
        except:
            print("no command")

# controls roku tv
def control(command:str):
    roku = Roku(IP_ADDRESS)
    
    if command == "back":
        roku.back()
    elif command == "home":
        roku.home()
    elif command and "open" in command:
        # get the app name
        app_name = command[4:].title().strip()

        try:
            roku[app_name].launch()
        except:
            print('no app with that name found')
    else:
        print("not recognized")
   
def main():
    while True:
        # record a wave file
        record_wav_file('command', 3)
        # convert to text
        command = wav_to_text('command.wav')
        # execute roku command
        control(command)

if __name__ == "__main__":
    main()