import os
import sys
#from dotenv import load_dotenv  # Ya no lo necesitamos

# PySide6
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox,
    QSpinBox, QDoubleSpinBox
)


from openai import OpenAI


###########################################
#Funciones para llamar a cada LLM (las pasaremos como métodos de clase)
###########################################
def call_gpt(openai_instance, messages, gpt_system, temperature=0.7, max_tokens=500):
    """
    Llama a GPT con la sintaxis de openai < 1.0.0.
    - messages: lista [{"role": "user"/"assistant", "content": "..."}]
    - gpt_system: string con el prompt system de GPT
    - temperature y max_tokens ajustables desde la interfaz
    """
    if not openai_instance:
        return "Error: GPT no está inicializado. Por favor ingresa tu API Key y presiona 'Save API Keys'."

    prompts = [{"role": "system", "content": gpt_system}] + messages
    try:
        response = openai_instance.chat.completions.create(
            model="gpt-4o-mini",  # Ajusta si no tienes acceso a este
            messages=prompts,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error llamando a GPT: {e}"


def call_gemini(openai_instance, messages, gemini_system, temperature=0.7, max_tokens=500):
    """
    Llama a Gemini con la misma interfaz (emulando la API de OpenAI).
    """
    if not openai_instance:
        return "Error: Gemini no está inicializado. Por favor ingresa tu API Key y presiona 'Save API Keys'."

    prompts = [{"role": "system", "content": gemini_system}] + messages
    try:
        response = openai_instance.chat.completions.create(
            model="gemini-1.5-flash",  # Ajusta si corresponde
            messages=prompts,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error llamando a Gemini: {e}"


###########################################
# Interfaz PySide6
###########################################
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GPT vs Gemini - Discussion with GUI controls")

        # Instancias de OpenAI se crearán dinámicamente
        self.gpt = None
        self.gemini = None

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        ########################################
        # Campos para las API Keys
        ########################################
        api_keys_layout = QHBoxLayout()
        self.label_gpt_key = QLabel("GPT API Key:")
        self.input_gpt_key = QLineEdit()
        self.label_gemini_key = QLabel("Gemini API Key:")
        self.input_gemini_key = QLineEdit()
        # Botón para guardar las keys
        self.save_keys_button = QPushButton("Save API Keys")
        self.save_keys_button.clicked.connect(self.on_save_api_keys)

        api_keys_layout.addWidget(self.label_gpt_key)
        api_keys_layout.addWidget(self.input_gpt_key)
        api_keys_layout.addWidget(self.label_gemini_key)
        api_keys_layout.addWidget(self.input_gemini_key)
        api_keys_layout.addWidget(self.save_keys_button)

        main_layout.addLayout(api_keys_layout)

        # System Prompt GPT
        self.label_gpt_system = QLabel("System Prompt GPT:")
        self.text_gpt_system = QTextEdit()
        self.text_gpt_system.setPlainText("You are GPT, an argumentative assistant.")

        # System Prompt Gemini
        self.label_gemini_system = QLabel("System Prompt Gemini:")
        self.text_gemini_system = QTextEdit()
        self.text_gemini_system.setPlainText("You are Gemini, a polite and courteous assistant.")

        main_layout.addWidget(self.label_gpt_system)
        main_layout.addWidget(self.text_gpt_system)

        main_layout.addWidget(self.label_gemini_system)
        main_layout.addWidget(self.text_gemini_system)

        # Controles de parámetros
        self.params_layout = QHBoxLayout()
        main_layout.addLayout(self.params_layout)

        # 5.1) Control para Número de Rondas
        self.label_rounds = QLabel("Spin rounds:")
        self.spin_rounds = QSpinBox()
        self.spin_rounds.setRange(1, 10)
        self.spin_rounds.setValue(2)  # Valor por defecto
        self.params_layout.addWidget(self.label_rounds)
        self.params_layout.addWidget(self.spin_rounds)

        # 5.2) Control para Temperature
        self.label_temp = QLabel("Temperature:")
        self.spin_temp = QDoubleSpinBox()
        self.spin_temp.setRange(0.0, 2.0)
        self.spin_temp.setSingleStep(0.1)
        self.spin_temp.setValue(0.7)
        self.params_layout.addWidget(self.label_temp)
        self.params_layout.addWidget(self.spin_temp)

        # 5.3) Control para Max Tokens
        self.label_max_tokens = QLabel("Max Tokens:")
        self.spin_max_tokens = QSpinBox()
        self.spin_max_tokens.setRange(50, 4000)
        self.spin_max_tokens.setValue(500)
        self.params_layout.addWidget(self.label_max_tokens)
        self.params_layout.addWidget(self.spin_max_tokens)

        # Prompt de usuario + botón
        user_prompt_layout = QHBoxLayout()
        self.label_user_prompt = QLabel("User Prompt:")
        self.input_user_prompt = QLineEdit()
        self.send_button = QPushButton("Send message")
        self.send_button.clicked.connect(self.on_send)

        # Área de conversación
        self.conversation_label = QLabel("Conversation:")
        self.conversation_area = QTextEdit()
        self.conversation_area.setReadOnly(True)

        user_prompt_layout.addWidget(self.label_user_prompt)
        user_prompt_layout.addWidget(self.input_user_prompt)
        user_prompt_layout.addWidget(self.send_button)
        main_layout.addLayout(user_prompt_layout)

        main_layout.addWidget(self.conversation_label)
        main_layout.addWidget(self.conversation_area)

        # Mantendremos DOS listas de mensajes separadas
        self.gpt_messages = []
        self.gemini_messages = []

    def on_save_api_keys(self):
        """
        Guarda las API Keys y crea las instancias de OpenAI (GPT, Gemini).
        """
        openai_api_key = self.input_gpt_key.text().strip()
        google_api_key = self.input_gemini_key.text().strip()

        if not openai_api_key or not google_api_key:
            QMessageBox.warning(self, "Warning", "Por favor ingresa ambas API Keys antes de guardar.")
            return

        try:
            # GPT
            self.gpt = OpenAI(api_key=openai_api_key)
            # Gemini
            self.gemini = OpenAI(
                api_key=google_api_key,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
            )
            QMessageBox.information(self, "Info", "API Keys guardadas correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo crear instancias: {e}")
            self.gpt = None
            self.gemini = None

    def on_send(self):
        """
        Cuando el usuario hace clic en "Enviar mensaje":
         1) Tomamos el user prompt y lo agregamos a GPT como "user".
         2) GPT contesta.
         3) Empezamos la "ronda" de intercambios:
            - GPT -> Gemini
            - Gemini -> GPT
            - Repetir tantas veces como spin_rounds indica
        """
        user_text = self.input_user_prompt.text().strip()
        if not user_text:
            QMessageBox.warning(self, "Warning", "Please insert a user message.")
            return

        # Leemos los valores de la GUI
        num_rounds = self.spin_rounds.value()
        temperature = self.spin_temp.value()
        max_tokens = self.spin_max_tokens.value()

        gpt_system = self.text_gpt_system.toPlainText()
        gemini_system = self.text_gemini_system.toPlainText()

        # 1) Usuario habla -> GPT
        self.gpt_messages.append({"role": "user", "content": user_text})
        self.conversation_area.append(f"**User**: {user_text}")

        # GPT contesta una vez al usuario
        gpt_answer = call_gpt(
            self.gpt,
            self.gpt_messages,
            gpt_system,
            temperature=temperature,
            max_tokens=max_tokens
        )
        self.gpt_messages.append({"role": "assistant", "content": gpt_answer})
        self.conversation_area.append(f"**GPT**: {gpt_answer}")

        # 2) Arrancamos el "ping-pong" con 'num_rounds' de intercambios
        for i in range(num_rounds):
            # GPT -> Gemini
            self.gemini_messages.append({"role": "user", "content": gpt_answer})
            gemini_answer = call_gemini(
                self.gemini,
                self.gemini_messages,
                gemini_system,
                temperature=temperature,
                max_tokens=max_tokens
            )
            self.gemini_messages.append({"role": "assistant", "content": gemini_answer})
            self.conversation_area.append(f"**Gemini**: {gemini_answer}")

            # Gemini -> GPT
            self.gpt_messages.append({"role": "user", "content": gemini_answer})
            gpt_answer = call_gpt(
                self.gpt,
                self.gpt_messages,
                gpt_system,
                temperature=temperature,
                max_tokens=max_tokens
            )
            self.gpt_messages.append({"role": "assistant", "content": gpt_answer})
            self.conversation_area.append(f"**GPT**: {gpt_answer}")

        # Limpiamos el prompt del usuario
        self.input_user_prompt.clear()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
