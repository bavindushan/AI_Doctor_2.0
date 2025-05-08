import os
import platform
import subprocess
from gtts import gTTS
from pydub import AudioSegment
from dotenv import load_dotenv
import elevenlabs
from elevenlabs.client import ElevenLabs

# Load environment variables
load_dotenv()
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

# Convert mp3 to wav
def convert_mp3_to_wav(mp3_path, wav_path):
    sound = AudioSegment.from_mp3(mp3_path)
    sound.export(wav_path, format="wav")

# Fix the function signature
def text_to_speech_with_gtts(input_text, output_filepath="gtts_output.mp3"):
    language = "en"
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_filepath)

    # Convert to WAV
    wav_path = output_filepath.replace(".mp3", ".wav")
    convert_mp3_to_wav(output_filepath, wav_path)

    # Autoplay
    os_name = platform.system()
    try:
        if os_name == "Windows":
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_path}").PlaySync();'])
        elif os_name == "Darwin":
            subprocess.run(['afplay', wav_path])
        elif os_name == "Linux":
            subprocess.run(['aplay', wav_path])
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while playing audio: {e}")

    return wav_path  # return the wav path to be used later in Gradio


# ElevenLabs TTS with autoplay
def text_to_speech_with_elevenlabs(input_text, output_mp3_path):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=input_text,
        voice="Aria",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_mp3_path)

    # Convert to WAV
    wav_path = output_mp3_path.replace(".mp3", ".wav")
    convert_mp3_to_wav(output_mp3_path, wav_path)

    # Autoplay
    os_name = platform.system()
    try:
        if os_name == "Windows":
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_path}").PlaySync();'])
        elif os_name == "Darwin":
            subprocess.run(['afplay', wav_path])
        elif os_name == "Linux":
            subprocess.run(['aplay', wav_path])
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while playing audio: {e}")


# === Run the TTS with autoplay ===
# input_text = "Hi, this is AI with Bavindu. Autoplay test successful!"
# text_to_speech_with_gtts(input_text, "gtts_autoplay.wav")

# To test ElevenLabs playback, uncomment below:
# text_to_speech_with_elevenlabs(input_text, "elevenlabs_autoplay.mp3")
