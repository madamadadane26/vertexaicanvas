from flask import Flask, render_template, request, jsonify
import vertexai
from vertexai.language_models import ChatModel, InputOutputTextPair

vertexai.init(project="gamebot-401519", location="us-central1")
chat_model = ChatModel.from_pretrained("chat-bison")
parameters = {
    "candidate_count": 1,
    "max_output_tokens": 1550,
    "temperature": 0.2,
    "top_p": 0.7,
    "top_k": 35
}
chat = chat_model.start_chat(
    context="""Given user input, you are supposed to generate ctx javascript-compatible code to interact with a canvas on a web app. The canvas size is width=\"500\" height=\"500\". The user input is supposed to help them visualize with animations and shapes. For example, if they ask for a circle and then ask for the circumference, then you should explain the visual, explain the problem if they are asking, and how to solve it. Give them some cool interactive ways to learn. Do not generate ASCII for the user. Include colors, animations, and details in the code to make the code visuals interesting. Be creative. Indicate the block of code separate from the explanation with the let method instead of var method. Generate the javascript code FIRST before the explanation. DO NOT BREAK THE CODE BLOCKS. This format is IMPORTANT, for every block of code follow this format. Have \\\"```\\\" included at the start and end of each javascript code block. Do not add // comments. I just want raw code with the format I requested. Generate a visualization to help them understand it AFTER the explanation. Use a 🤖 emoji to identify yourself. Always encourage the user to learn, be positive and cheerful. Use a bunch of emojis related to keywords.""",
)
app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send_message", methods=["POST"])
def send_message():
    user_input = request.form["user_input"]
    response = chat.send_message(user_input, **parameters)
    return jsonify({"response": response.text})

if __name__ == "__main__":
    app.run(debug=True)
