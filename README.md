# GitHub Complex Repository Analyzer

The GitHub Repository Analyzer is a web application that analyzes the technical complexity of GitHub repositories and provides insights on their complexity. It uses a pre-trained language model to evaluate repository names and select the most complex one. Additionally, it generates a justification for the selection using the language model.

## Features

- Fetches repositories from a GitHub user's profile
- Scores the repositories based on their technical complexity
- Identifies the most complex repository
- Generates a justification for the selection using a language model

- ## Technologies Used

- Python
- Flask (web framework)
- Requests (HTTP library)
- PyTorch (deep learning library)
- Hugging Face Transformers (NLP library)

- ## Installation

1. Clone the repository:
   
```
git clone https://github.com/ShakthiVar/MercorMLProject.git
cd MercorMLProject 
```   

## Implementation Steps

1.Create a virtual environment and activate it:


```
python -m venv venv

venv\Scripts\activate 
```

2.Install the required dependencies:

```
pip install -r requirements.txt
```

3.Run the application:

```
python main.py
```

4.Open your web browser and go to http://localhost:5000 to access the application.

# Usage

1.Open the web application in your browser.

2.Enter a valid GitHub user URL in the provided input field and click the "Analyze" button.

3.The application will fetch the repositories from the user's profile, analyze their complexity, and display the result.

4.The most complex repository will be shown with a link to its GitHub page, and a justification for the selection will be provided.


Feel free to modify the content and structure of the README.md file to fit your project's requirements and add any additional sections or information as needed!!


  
