# 🤖 LLM Arena: GPT vs Gemini (Desktop App)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Framework](https://img.shields.io/badge/GUI-PySide6-green)
![API](https://img.shields.io/badge/API-OpenAI%20%7C%20Gemini-orange)

Una aplicación de escritorio diseñada para orquestar debates automatizados entre dos Modelos de Lenguaje (LLMs): **GPT-4** (OpenAI) y **Gemini 1.5** (Google).

La herramienta permite definir "personalidades" (System Prompts) para cada modelo y observar cómo interactúan, debaten o resuelven problemas en un bucle de conversación autónomo, todo desde una interfaz gráfica nativa.

---

## 🚀 Características Principales

* **Orquestación Multi-Modelo:** Conexión simultánea a las APIs de OpenAI y Google Gemini.
* **Simulación de Debates:** Permite enfrentar a los modelos asignándoles roles opuestos (ej. "Científico Escéptico" vs "Filósofo Optimista").
* **Control de Flujo:** Configuración de "Rondas de Spin" para determinar cuántas veces se responderán mutuamente de forma automática.
* **Ajuste Fino:** Control granular de parámetros como `Temperature` (creatividad) y `Max Tokens` directamente desde la interfaz de usuario.
* **Interfaz Nativa:** Desarrollada en **PySide6 (Qt)** para un rendimiento fluido en escritorio (Windows/Mac/Linux).

---

## 🛠️ Instalación y Uso

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/raulcamaracarreon/LLM-Arena-Desktop.git](https://github.com/raulcamaracarreon/LLM-Arena-Desktop.git)
    cd LLM-Arena-Desktop
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Ejecutar la aplicación:**
    ```bash
    python app.py
    ```

### ⚙️ Configuración en la App
Una vez abierta la ventana:
1.  Ingresa tus **API Keys** de OpenAI y Google en los campos superiores y pulsa "Save API Keys".
2.  Edita los **System Prompts** para definir cómo quieres que se comporte cada IA.
3.  Escribe el mensaje inicial en "User Prompt" y pulsa **Send**.

---

## 📋 Requisitos Técnicos

* **Python 3.9** o superior.
* **API Key de OpenAI** (con créditos/acceso vigente).
* **API Key de Google AI Studio** (para Gemini).

**Librerías Python:**
* `PySide6` (GUI Framework)
* `openai` (Cliente API)

---

## 🧠 Caso de Uso: "Vibe Coding" & Evaluación

Este proyecto nace del interés en evaluar cualitativamente el comportamiento de los modelos ("Vibe Coding"). Al ponerlos a conversar entre sí, es posible detectar:
* **Sesgos y Estilos:** Contrastar la formalidad de Gemini frente a la creatividad de GPT.
* **Detección de Alucinaciones:** Observar si un modelo corrige al otro cuando se introducen datos falsos.
* **Resolución de Conflictos:** Analizar la capacidad de los modelos para llegar a consensos complejos.

---

> **Autor:** Raúl Héctor Cámara Carreón
