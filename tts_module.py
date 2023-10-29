import os
import spacy
from TTS.api import TTS
from pydub import AudioSegment
import numpy as np

OUTPUT_DIR = "output_files"

def initialize_tts():
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v1.1")
    tts.to("cuda:0")
    return tts

tts = initialize_tts()

def m4a_to_wav(file_path):
    audio = AudioSegment.from_file(file_path, "m4a")
    new_file_path = file_path.replace(".m4a", ".wav")
    audio.export(new_file_path, format="wav")
    return new_file_path

def save_audio_from_array(sample_rate, audio_array, output_path):
    audio_segment = AudioSegment(audio_array.tobytes(), frame_rate=sample_rate, sample_width=audio_array.dtype.itemsize, channels=1)
    audio_segment.export(output_path, format="wav")
    return output_path

def seslendir_ui(metin=None, referans_sesi=None, ses_kaydi=None, dil="en"):
    if not dil:
        return "Lütfen bir dil seçin!", None

    referans_sesi_dosya = referans_sesi.name if referans_sesi else None
    if referans_sesi_dosya and referans_sesi_dosya.endswith(".m4a"):
        referans_sesi_dosya = m4a_to_wav(referans_sesi_dosya)

    ses_kaydi_dosya = None
    if ses_kaydi:
        sample_rate, audio_array = ses_kaydi
        ses_kaydi_dosya = os.path.join(OUTPUT_DIR, "mikrofon_kaydi.wav")
        ses_kaydi_dosya = save_audio_from_array(sample_rate, np.array(audio_array), ses_kaydi_dosya)

    return seslendir(metin, referans_sesi_dosya or ses_kaydi_dosya, dil)

def seslendir(metin, referans_sesi, dil):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(metin)
    cumleler = [sent.text for sent in doc.sents]

    ses_dosyalari = []
    for cumle in cumleler:
        dosya_yolu = os.path.join(OUTPUT_DIR, f"temp_output.wav")
        tts.tts_to_file(text=cumle,
                        file_path=dosya_yolu,
                        speaker_wav=referans_sesi if referans_sesi else None,
                        language=dil)
        ses_dosyalari.append(AudioSegment.from_wav(dosya_yolu))

    birlesik_ses = sum(ses_dosyalari, AudioSegment.empty())
    dosya_yolu = os.path.join(OUTPUT_DIR, "birlesik_output.wav")
    birlesik_ses.export(dosya_yolu, format="wav")

    return dosya_yolu, referans_sesi if referans_sesi else None
