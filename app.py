import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from ibm_watsonx_ai.foundation_models import ModelInference

app = Flask(__name__)
CORS(app) 

project_id = "96bb60dc-c214-4680-98b8-a0ddfe811e70"
model_id = "ibm/granite-8b-code-instruct"

gen_params = {
    "max_new_tokens": 300,
    "temperature": 0.7,
    "stop_sequences": ["\nUser:", "User:"] # Tells the AI to shut up when its turn is over
}

# We will store the AI model here once it is initialized
watson_model = None 

def init_model():
    """Initializes the connection to IBM only when needed."""
    raw_key = os.environ.get("WATSONX_API_KEY")
    
    if not raw_key:
        raise ValueError("The WATSONX_API_KEY is completely missing from the environment.")
        
    credentials = {
        "url": "https://au-syd.ml.cloud.ibm.com",
        "apikey": raw_key.strip() # .strip() removes accidental copy-paste spaces
    }
    
    return ModelInference(
        model_id=model_id,
        credentials=credentials,
        project_id=project_id
    )

@app.route('/api/chat', methods=['POST'])
def chat():
    global watson_model
    
    data = request.json
    user_input = data.get("message", "")
    
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Lazy Initialization: Connect to IBM on the first chat request
        if watson_model is None:
            watson_model = init_model()
            
        prompt = f"You are a helpful Computer Science tutor. Answer the following question.\n\nUser: {user_input}\nAI:"
        response = watson_model.generate_text(prompt=prompt, params=gen_params)
        
        return jsonify({"reply": response})
        
    except Exception as e:
        # If the key is bad, the server won't crash. It sends the error to the UI.
        print(f"Backend Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)