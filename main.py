from flask import Flask, jsonify, request
import vertexai
from vertexai.language_models import ChatModel, InputOutputTextPair

app = Flask(__name__)

# Vertex AI setup
vertexai.init(project="gamebot-401519", location="us-central1")
chat_model = ChatModel.from_pretrained("chat-bison")
parameters = {
    "candidate_count": 1,
    "max_output_tokens": 1024,
    "temperature": 0.2,
    "top_p": 0.8,
    "top_k": 40
}
chat = chat_model.start_chat(
    context="""given a user input, you are supposed to generate a javascript code to interact with a canvas on a web app. The user input is supposed to help them visualize with animations and shapes. If they ask for a circle and then ask for the circumference. Generate a visualization to help them understand it. Explain it, explain the code. give them some cool interactive way to learn. Use a 🤖 emoji to identify yourself. Always encourage the user to learn and let's do it together. Use a bunch of emojis related to keywords"""
)

@app.route('/generate', methods=['POST'])
def generate_code():
    user_prompt = request.json.get('prompt', '')

    try:
        response = chat.send_message(user_prompt, **parameters)
        generated_js = response.text

        return jsonify({'js_code': generated_js})

    except Exception as e:
        # Error handling
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
