from flask import Flask, request, jsonify
import speech_recognition as sr
import pyttsx3
from googletrans import Translator
import io

app = Flask(__name__)

translator = Translator()
r = sr.Recognizer()
engine = pyttsx3.init()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    if 'audio' in request.files:
        # Read the audio file from the request
        audio_file = request.files['audio']
        
        # Convert the audio file to an AudioFile object for speech recognition
        audio_data = sr.AudioFile(io.BytesIO(audio_file.read()))
        
        with audio_data as source:
            audio = r.record(source)
        
        try:
            # Recognize the speech
            MyText = r.recognize_google(audio)
            print(f"Recognized: {MyText}")
            
            # Translate the recognized speech
            translated = translator.translate(MyText, dest='es').text
            print(f"Translated: {translated}")
            
            # Speak the translated text (optional)
            engine.say(translated)
            engine.runAndWait()
            
            # Send the translated text back to the client
            return jsonify({"translatedText": translated})
        
        except sr.UnknownValueError:
            return jsonify({"translatedText": "Could not understand audio."}), 400
        except sr.RequestError as e:
            return jsonify({"translatedText": f"Could not request results; {e}"}), 500
    else:
        return jsonify({"translatedText": "No audio received."}), 400

if __name__ == "__main__":
    app.run(debug=True)