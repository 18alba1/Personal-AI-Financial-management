# Personal-AI-Financial-management


## How to run the project

First you need to install all the dependecies:
```
pip install -e .
```

Then, modify the `.streamlit/example_secrets.toml` file to include the OpenAI key and rename it to `.streamlit/secrets.toml`

Now, you can run the streamlit application by:
```
streamlit run money_mate/home_page.py
```