# from flask import Flask, request, jsonify, render_template
# import requests
# from gtts import gTTS
# from langdetect import detect
# import os
# import uuid

# app = Flask(__name__)

# ESP32_URL = "http://192.168.79.160"  # replace with your ESP32 local IP

# @app.route("/")
# def index():
#     return render_template("index.html")

# def speak(text):
#     lang = detect(text)
#     tts = gTTS(text=text, lang=lang)
#     os.makedirs("static", exist_ok=True)
#     filename = f"static/{uuid.uuid4()}.mp3"
#     tts.save(filename)
#     return filename

# @app.route("/command", methods=["POST"])
# def command():
#     text = request.json.get("text", "").lower()

#     if any(word in text for word in ["led", "light", "bulb"]) and any(word in text for word in ["on", "chalu", "chaalu"]):
#         requests.get(f"{ESP32_URL}/on")
#         msg = "LED turned on"
#     elif any(word in text for word in ["led", "light", "bulb"]) and any(word in text for word in ["off", "band"]):
#         requests.get(f"{ESP32_URL}/off")
#         msg = "LED turned off"
#     else:
#         msg = "Sorry, I did not understand."

#     voice_file = speak(msg)
#     return jsonify({"message": msg, "voice": voice_file})

# # if __name__ == "__main__":
# #     app.run(debug=True)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=10000)



from flask import Flask, request, jsonify, render_template
from gtts import gTTS
from langdetect import detect
import os
import uuid

app = Flask(__name__)

# Store the latest LED command ("on", "off", or "none")
latest_led_command = "none"

@app.route("/")
def index():
    return render_template("index.html")

def speak(text):
    lang = detect(text)
    tts = gTTS(text=text, lang=lang)
    os.makedirs("static", exist_ok=True)
    filename = f"static/{uuid.uuid4()}.mp3"
    tts.save(filename)
    return filename

@app.route("/command", methods=["POST"])
def command():
    global latest_led_command
    text = request.json.get("text", "").lower()

    if any(word in text for word in ["led", "light", "bulb"]) and any(word in text for word in ["on", "chalu", "chaalu"]):
        latest_led_command = "on"
        msg = "LED turned on"
    elif any(word in text for word in ["led", "light", "bulb"]) and any(word in text for word in ["off", "band"]):
        latest_led_command = "off"
        msg = "LED turned off"
    else:
        latest_led_command = "none"
        msg = "Sorry, I did not understand."

    voice_file = speak(msg)
    return jsonify({"message": msg, "voice": voice_file})


@app.route("/get-command")
def get_command():
    global latest_led_command
    response = jsonify({"led": latest_led_command})
    
    # After sending, reset it so ESP32 only acts once
    latest_led_command = "none"
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

