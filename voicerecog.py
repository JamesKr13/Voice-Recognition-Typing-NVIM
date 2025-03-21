import os
import sys
import wave
import json
import pyaudio
from vosk import Model, KaldiRecognizer
import subprocess
import threading
from rapidfuzz import fuzz
from rapidfuzz import process
import pynvim
text_to_char_mapping = {
    "square bracket": "[]",
    "curly bracket": "{}",
    "round bracket": "()",
    "colon": ":",
    "semicolon": ";",
    "exclamation mark": "!",
    "at": "@",
    "hash": "#",
    "dollar": "$",
    "percent": "%",
    "caret": "^",
    "ampersand": "&",
    "asterisk": "*",
    "open parenthesis": "(",
    "close parenthesis": ")",
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

def parse_text(text,nvim):
    if (fuzz.ratio(text.lower(), "new line")):
            nvim.command("normal! o")
            return 1
    for phrase, replacement in text_to_char_mapping.items():
        similarity = fuzz.ratio(text.lower(), phrase.lower())
        if similarity > 80:
            text = text.replace(phrase, replacement)
            break
    current_line = nvim.current.line  # Get the current line in Neovim
    updated_line = current_line + " " + text  # Append text to the current line
    nvim.current.line = updated_line

    
def process_text_thread(text, buffer):
    # Use threading to run parse_text in a separate thread
    thread = threading.Thread(target=parse_text, args=(text, buffer))
    thread.start()

def recognize_audio():
    while True:
        data = stream.read(2048, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_json = json.loads(result)
            text = result_json.get("text", "")
            if text:
                process_text_thread(text,nvim)
                


model_path = "/home/jamesrichards/Desktop/VoiceRecog/vosk-model/vosk-model-en-us-0.42-gigaspeech"

model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)

stream.start_stream()

nvim = pynvim.attach('socket', path='/tmp/nvimsocket')


print("Begin rambling")
recognition_thread = threading.Thread(target=recognize_audio)
recognition_thread.daemon = True  # Set as daemon so it exits when the main program exits
recognition_thread.start()

try:
    while True:
       pass

except KeyboardInterrupt:
    print("Exiting")
    stream.stop_stream()
    stream.close()
    p.terminate()





    
