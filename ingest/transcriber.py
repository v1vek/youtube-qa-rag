import whisper
from pathlib import Path
from config import TRANSCRIPT_DIR, WHISPER_MODEL

model = whisper.load_model(WHISPER_MODEL)

def transcribe_audio(audio_path: str, output_dir: str = TRANSCRIPT_DIR) -> str:
    """
    Transcribe audio from a given file and save the transcript to the specified output path.

    :param audio_path: The path to the audio file to transcribe.
    :param output_dir: The path where the transcript will be saved.
    :return: The path to the saved transcript file.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    audio_file = Path(audio_path)
    if not audio_file.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    transcript_file = Path(output_dir) / f"{audio_file.stem}.txt"
    if transcript_file.exists():
        print(f"Transcript already exists: {transcript_file}")
        return str(transcript_file)
    
    print(f"Transcribing audio: {audio_path}")
    result = model.transcribe(str(audio_file))

    with open(transcript_file, "w", encoding="utf-8") as f:
        for segment in result['segments']:
            if isinstance(segment, dict):
                start = segment['start']
                end = segment['end']
                text = segment['text'].strip()
            elif isinstance(segment, (list, tuple)) and len(segment) >= 3:
                start = segment[0]
                end = segment[1]
                text = str(segment[2]).strip()
            else:
                raise TypeError("Unexpected segment format: {}".format(type(segment)))
            f.write(f"[{start:.2f} - {end:.2f}] {text}\n")

    return str(transcript_file)