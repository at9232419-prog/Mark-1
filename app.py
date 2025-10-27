from flask import Flask, render_template, request
from openai import OpenAI
import os

app = Flask(__name__)

# ✅ Initialize OpenAI client (new syntax)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

# ✅ Chat route
@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.form["user_input"]
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # ✅ latest model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = completion.choices[0].message.content
        return f"Reply: {reply}"
    except Exception as e:
        return f"Error: {str(e)}"

# ✅ Image generation route (new OpenAI API format)
@app.route("/generate", methods=["POST"])
def generate():
    try:
        prompt = request.form["prompt"]
        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt
        )
        image_url = result.data[0].url
        return f"<img src='{image_url}' width='300'>"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
