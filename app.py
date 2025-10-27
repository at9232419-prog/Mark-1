import os
from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__, static_folder="static", template_folder="templates")

openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form.get('message', '') or request.json.get('message', '')
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}],
            max_tokens=300
        )
        reply = resp['choices'][0]['message']['content'].strip()
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/imagegen', methods=['POST'])
def imagegen():
    prompt = request.form.get('prompt', '') or request.json.get('prompt', '')
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    try:
        img = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        url = img['data'][0]['url']
        return jsonify({"image_url": url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
