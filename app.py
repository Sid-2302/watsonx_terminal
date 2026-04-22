import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from ibm_watsonx_ai.foundation_models import ModelInference

app = Flask(__name__)
# Enable CORS so our frontend can communicate with this API
CORS(app) 

# IBM Cloud Credentials
credentials = {
    "url": "https://au-syd.ml.cloud.ibm.com",
    "apikey": os.environ.get("WATSONX_API_KEY") 
}
project_id = "96bb60dc-c214-4680-98b8-a0ddfe811e70"
model_id = "ibm/granite-8b-code-instruct"

# Initialize Model
model = ModelInference(
    model_id=model_id,
    credentials=credentials,
    project_id=project_id
)

gen_params = {
    "max_new_tokens": 300,
    "temperature": 0.7
}

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("message", "")
    
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Ask the Watsonx model
        # Ask the Watsonx model
        prompt = f"You are a helpful Computer Science tutor. Answer the following question.\n\nUser: {user_input}\nAI:"
        response = model.generate_text(prompt=prompt, params=gen_params)
        
        # Send the AI's reply back to the frontend
        return jsonify({"reply": response})
        
    except Exception as e:
        # If IBM Cloud throws an error (like a bad API key), catch it here!
        print(f"Backend Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)