from flask import Flask, render_template, request, jsonify
import openai

# Set your OpenAI API key
openai.api_key = "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"

# Define the Chatbot class
class Chatbot:
    def __init__(self):
        # Initialize the chatbot's history with its persona
        self.history = [
            {"role": "system", "content": "You are a family doctor with a calm and caring demeanor, always ready to listen to your patients and provide them with the best advice"}
        ]

    def add_to_history(self, role, message):
        # Add a new message to the chatbot's history
        self.history.append({"role": role, "content": message})

    def chat_with_gpt(self, prompt):
        # Add the user's message to the history
        user_message = {"role": "user", "content": prompt}
        self.add_to_history(user_message["role"], user_message["content"])

        # Generate a response using OpenAI's GPT model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.history,
            temperature=0.2
        )

        # Extract the content from the response
        bot_response = response.choices[0].message['content'].strip()
        # Add the bot's response to the history
        self.add_to_history("assistant", bot_response)

        # Return the bot's response
        return bot_response

# Create a Flask app
app = Flask(__name__)
# Instantiate the chatbot
my_chatbot = Chatbot()

# Define routes and views
@app.route("/")
def index():
    # Render the index page
    return render_template('index.html')

@app.route("/chatpage")
def chatpage():
    # Render the chat page
    return render_template('chatpage.html')

@app.route("/get_response", methods=["POST"])
def get_response():
    # Get the user's input from the form
    user_input = request.form["user_input"]
    # Get the chatbot's response
    response = my_chatbot.chat_with_gpt(user_input)

    # Format the response for better organization
    organized_response = "\n".join(response.split("###"))

    # Return the organized response as JSON
    return jsonify({"response": organized_response})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
