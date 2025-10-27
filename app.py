from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['message']
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}]
    )
    return jsonify({"reply": response.choices[0].message.content})

@app.route('/textgen', methods=['POST'])
def textgen():
    prompt = request.form['prompt']
    response = client.completions.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=200
    )
    return jsonify({"text": response.choices[0].text.strip()})

@app.route('/imagegen', methods=['POST'])
def imagegen():
    prompt = request.form['prompt']
    image = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="512x512"
    )
    return jsonify({"image_url": image.data[0].url})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
