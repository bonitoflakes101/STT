from pvrecorder import PvRecorder
import wave
import struct
import threading
import openai

# STEP 1: Records user's speech then saves it into an audio file
class Recorder:
    def __init__(self, device_index=0, output_file='user_voice_record.wav', frame_length=512, channels=1, sampwidth=2, framerate=16000):
        self.device_index = device_index
        self.output_file = output_file
        self.frame_length = frame_length
        self.channels = channels
        self.sampwidth = sampwidth
        self.framerate = framerate
        self.recorder = None
        self.wave_file = None
        self.stop_event = threading.Event()

    def list_devices(self):
        devices = PvRecorder.get_available_devices()
        for index, device in enumerate(devices):
            print(f"[{index}] {device}")
    
    def start_recording(self):
        self.recorder = PvRecorder(device_index=self.device_index, frame_length=self.frame_length)
        self.recorder.start()
        print("Recording... Press Enter to stop.")

        self.wave_file = wave.open(self.output_file, 'w')
        self.wave_file.setnchannels(self.channels)
        self.wave_file.setsampwidth(self.sampwidth)
        self.wave_file.setframerate(self.framerate)

        self.recording_thread = threading.Thread(target=self._write_frames)
        self.recording_thread.start()

        # wait for user to press Enter to stop recording
        input()  
        self.stop_event.set()
        self.recording_thread.join()
        print("Recording stopped.")

    def _write_frames(self):
        try:
            while not self.stop_event.is_set():
                frame = self.recorder.read()
                self.wave_file.writeframes(struct.pack('h' * len(frame), *frame))
        finally:
            self.recorder.stop()
            self.wave_file.close()

    def get_output_file(self):
        return self.output_file

# STEP 2: Transcribes user's recorded audio file into text
class WhisperTranscriber:
    def __init__(self, api_key, model_id='whisper-1'):
        openai.api_key = api_key
        self.model_id = model_id

    def transcribe(self, audio_file_path, language='en'):
        with open(audio_file_path, 'rb') as audio_file:
            response = openai.audio.transcriptions.create(
                model=self.model_id,
                file=audio_file,
                language=language
            )
        return response['text']

    # if confirmed na anong mic gamitin, set it directly device_index = 0. 
    def record_and_transcribe(self, device_index=0, output_file='user_voice_record.wav', language='en'):
        recorder = Recorder(device_index=device_index, output_file=output_file)
        recorder.list_devices() # pwede tanggalin to, pero this is just to check kung ano available mics to use then just edit device_index
        recorder.start_recording() # records and saves audio file
        transcribed_text = self.transcribe(recorder.get_output_file(), language) # transcribes audio to text
        print("Transcribed Text: ", transcribed_text)
        return transcribed_text

# Example usage, place this sa main file
if __name__ == "__main__":
    API_KEY = 'YOUR_API_KEY'  # replace with your actual Whisper API key
    whisper_transcriber = WhisperTranscriber(api_key=API_KEY)
    whisper_transcriber.record_and_transcribe() # outputs the transcribed text
