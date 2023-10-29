import gradio as gr
import os
import tts_module
from tts_module import seslendir_ui
from logging_module import configure_logging, log_messages

# Log ayarlarını yapılandır
configure_logging()

# Çıktıların kaydedileceği klasör yolu
if not os.path.exists(tts_module.OUTPUT_DIR):
    os.makedirs(tts_module.OUTPUT_DIR)

# Gradio arayüzünün oluşturulması
arayuz = gr.Interface(
    fn=seslendir_ui,
    inputs=[
        gr.components.Textbox(placeholder="Metni buraya yazın...", label="Metin", default=""),
        gr.components.File(label="Referans Ses Dosyası Yükleyin:"),
        gr.components.Audio(source="microphone", label="Mikrofondan Ses Kaydedin:"),
        gr.components.Dropdown(choices=[
            "en", "es", "fr", "de", "it", "pt", "pl", "tr", 
            "ru", "nl", "cs", "ar", "zh-cn", "ja"
        ], label="Dil Seçimi:", default="en")
    ],
    outputs=[
        gr.components.Audio(type="filepath", label="Seslendirme Çıktısı"),
        gr.components.Audio(type="filepath", label="Referans Ses")
    ]
)

log_messages()
arayuz.launch(debug=True)
