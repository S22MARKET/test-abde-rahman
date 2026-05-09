import os
import glob
import speech_recognition as sr
from pydub import AudioSegment
import imageio_ffmpeg

# إعداد مسار ffmpeg تلقائياً
AudioSegment.converter = imageio_ffmpeg.get_ffmpeg_exe()

def transcribe_audio(file_path):
    print(f"Processing: {os.path.basename(file_path)}")
    
    wav_path = file_path + ".wav"
    try:
        print("  -> Converting to WAV...")
        audio = AudioSegment.from_file(file_path)
        # توحيد التردد لتحسين التعرف على الصوت
        audio = audio.set_channels(1).set_frame_rate(16000)
        audio.export(wav_path, format="wav")
    except Exception as e:
        print(f"  -> Error converting {file_path}: {e}")
        return
        
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(wav_path) as source:
            print("  -> Reading audio data...")
            audio_data = recognizer.record(source)
            
        print("  -> Transcribing...")
        # استخدام التعرف على الصوت من جوجل
        text = recognizer.recognize_google(audio_data, language="en-US")
        print(f"  -> Done!")
        
        with open("transcripts_output.txt", "a", encoding="utf-8") as f:
            f.write(f"\n=====================================\n")
            f.write(f"File: {os.path.basename(file_path)}\n")
            f.write(f"=====================================\n")
            f.write(text + "\n\n")
            
    except sr.UnknownValueError:
        print("  -> Google STT could not understand audio")
    except sr.RequestError as e:
        print(f"  -> API error: {e}")
    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)

if __name__ == "__main__":
    audio_dir = "sawtiyat"
    audio_files = glob.glob(os.path.join(audio_dir, "*.m4a")) + glob.glob(os.path.join(audio_dir, "*.ogg"))
    
    with open("transcripts_output.txt", "w", encoding="utf-8") as f:
        f.write("AUTOMATIC TRANSCRIPTIONS\n\n")
        
    print(f"Found {len(audio_files)} audio files.")
    for file in audio_files:
        transcribe_audio(file)
        
    print("\n--- All Done! Transcripts saved to transcripts_output.txt ---")
