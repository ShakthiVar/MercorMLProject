from flask import Flask, render_template, request
import requests
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    user_url = request.form['user_url']
    result = fetch_github_repositories(user_url)
    if result is None:
        return render_template('error.html', message='Failed to fetch repositories or perform analysis.')
    repositories_data, justification_text = result
    return render_template('result.html', repositories_data=repositories_data, justification=justification_text)
def fetch_github_repositories(user_url):
   # Extracting the GitHub username from the user URL
    username = user_url.split("/")[-1]

    # Ensure the username is not empty
    if not username:
        print("Invalid GitHub user URL.")
        return None

    # API endpoint to fetch user repositories
    api_url = f"https://api.github.com/users/{username}/repos"

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise exception if request was unsuccessful
        repositories = response.json()

        # Extracting repository names and URLs
        repositories_data = []
        for repo in repositories:
            repository_name = repo['name'].strip().lower()
            repository_url = repo['html_url']
            repositories_data.append({"name": repository_name, "url": repository_url})

        # Initialize tokenizer and model
        tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        model = GPT2LMHeadModel.from_pretrained("gpt2")

        # Process and score the repository names
        repository_scores = {}
        for data in repositories_data:
            repository_name = data['name']

            # Generate a prompt or template based on the repository name
            prompt = f"Evaluate the technical complexity of the repository: {repository_name}. Analyze the code and provide insights on its complexity."

            # Tokenize the prompt (same as before)
            input_ids = tokenizer.encode(prompt, add_special_tokens=False, truncation=True, max_length=100,
                                         return_tensors="pt")
            attention_mask = torch.ones_like(input_ids)

            with torch.no_grad():
                output = model.generate(input_ids=input_ids, attention_mask=attention_mask, max_new_tokens=200,
                                        pad_token_id=tokenizer.eos_token_id)

            processed_repo = tokenizer.decode(output[0], skip_special_tokens=True)
            complexity_score = len(processed_repo)
            repository_scores[repository_name] = complexity_score

        # Identify the repository with the highest complexity score
        most_complex_repo = max(repository_scores, key=repository_scores.get)

        # Generate clickable links for the most complex repositories
        complex_repositories_data = []
        for data in repositories_data:
            if data['name'] == most_complex_repo:
                complex_repositories_data.append({"name": data['name'], "url": data['url']})
            else:
                complex_repositories_data.append({"name": data['name'], "url": None})

        # Justify the selection using GPT (same as before)
        justification_prompt = f"Justification for selecting the most technically complex repository: {most_complex_repo}."
        justification_input_ids = tokenizer.encode(justification_prompt, add_special_tokens=False, truncation=True,
                                                   max_length=100, return_tensors="pt")

        attention_mask = torch.ones_like(justification_input_ids)

        with torch.no_grad():
            justification_output = model.generate(input_ids=justification_input_ids, attention_mask=attention_mask,
                                                  max_new_tokens=200, pad_token_id=tokenizer.eos_token_id)

        justification_text = tokenizer.decode(justification_output[0], skip_special_tokens=True)

        return complex_repositories_data, justification_text

    except requests.exceptions.HTTPError as err:
        print(f"An HTTP error occurred: {err}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")