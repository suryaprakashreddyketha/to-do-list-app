print("surya")
import os
import requests
import base64
from flask import Flask, request, jsonify
from openai import AzureOpenAI
from dotenv import load_dotenv
from flask_cors import CORS

# THIS LINE MUST COME FIRST — it loads the .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Now create the client and variables AFTER loading env
client = AzureOpenAI(
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version=os.getenv('AZURE_OPENAI_API_VERSION')
)

DEPLOYMENT_NAME = os.getenv('AZURE_OPENAI_DEPLOYMENT')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# NOW it's safe to print debug info
print("GITHUB_TOKEN loaded:", "Yes" if GITHUB_TOKEN else "NO - MISSING!")
if GITHUB_TOKEN:
    print("First 5 chars of token:", GITHUB_TOKEN[:5])
else:
    print("Token is empty or missing!")

@app.route('/search', methods=['POST'])
def search_repo():
    data = request.json
    user_query = data.get('query')
    repo = data.get('repo')

    if not user_query or not repo:
        return jsonify({'error': 'Missing query or repo'}), 400

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    #search_params = {"q": f"{user_query} repo:{repo}", "per_page": 10}
    search_params = {"q": f"{user_query} in:file,path repo:{repo}", "per_page": 10}
    search_url = "https://api.github.com/search/code"

    search_response = requests.get(search_url, headers=headers, params=search_params)

    if search_response.status_code != 200:
        return jsonify({'error': 'GitHub search failed', 'details': search_response.json()}), 500

    items = search_response.json().get('items', [])
    if not items:
        return jsonify({'answer': 'No files matched your query in this repository.'})

    context = ""
    for item in items[:8]:  # Limit to 8 files to avoid token overflow
        file_path = item['path']
        content_url = f"https://api.github.com/repos/{repo}/contents/{file_path}"
        content_response = requests.get(content_url, headers=headers)

        if content_response.status_code == 200:
            content_data = content_response.json()
            if 'content' in content_data:
                file_content = base64.b64decode(content_data['content']).decode('utf-8', errors='ignore')
                context += f"### File: {file_path}\n{file_content[:3000]}\n\n"  # Limit per file
        else:
            context += f"### File: {file_path} (could not fetch full content)\n"

    system_prompt = "You are a helpful assistant that answers questions using only the provided repository code/files."
    user_prompt = f"""
User Question: {user_query}

Repository Content:
{context}

Answer clearly and include relevant file names and code snippets.
"""

    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=800,
            temperature=0.5
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        return jsonify({'error': 'Azure OpenAI error', 'details': str(e)}), 500

    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
