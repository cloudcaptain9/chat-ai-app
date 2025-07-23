from flask import Flask, request, jsonify, render_template
import boto3
import json

app = Flask(__name__)

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
model_id = "mistral.mistral-7b-instruct-v0:2"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        body = request.get_json()
        prompt = body.get("message", "")
        if not prompt:
            raise ValueError("No message provided")

        formatted_prompt = f"<s>[INST] {prompt} [/INST]"

        payload = {
            "prompt": formatted_prompt,
            "max_tokens": 512,
            "temperature": 0.7
        }

        response = bedrock.invoke_model(
            modelId=model_id,
            body=json.dumps(payload),
            contentType="application/json",
            accept="application/json"
        )

        response_body = json.loads(response["body"].read())
        answer = response_body.get("outputs", [{}])[0].get("text", "No response.")

        return jsonify({ "response": answer })

    except Exception as e:
        return jsonify({ "error": str(e) }), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)

