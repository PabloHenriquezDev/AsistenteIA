import os, json
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

# Carpeta donde guardamos los JSON
CONVERSATIONS_DIR = os.path.join(os.path.dirname(__file__), 'conversations')
os.makedirs(CONVERSATIONS_DIR, exist_ok=True)

def get_history(persona):
    path = os.path.join(CONVERSATIONS_DIR, f"{persona}.json")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    # Si no existe, arrancamos con un system prompt
    return [{"role": "system", "content": persona}] if persona else []

def save_history(persona, history):
    path = os.path.join(CONVERSATIONS_DIR, f"{persona}.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    persona = data.get('persona', '').strip()
    prompt  = data.get('prompt', '').strip()

    # 1) Cargo historial previo
    history = get_history(persona)

    # 2) Añado el mensaje del usuario
    history.append({"role": "user", "content": prompt})

    # 3) Preparo el input para Ollama
    lines = []
    for turn in history:
        lines.append(f"{turn['role']}: {turn['content']}")
    lines.append("assistant:")
    full_input = "\n\n".join(lines)

    # 4) Llamo a Ollama
    proc = subprocess.Popen(
        ["ollama", "run", "gemma3:12b"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding='utf-8', errors='replace'
    )
    out, err = proc.communicate(input=full_input)
    respuesta = (out or err).strip()

    # 5) Añado la respuesta al historial y la guardo
    history.append({"role": "assistant", "content": respuesta})
    save_history(persona, history)

    return jsonify({"respuesta": respuesta})

if __name__ == '__main__':
    app.run(port=5000)
