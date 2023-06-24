# simple chat
A minimal ChatGPT-like UI built with Streamlit


git clone https://github.com/niels-oz/simple-chat.git
cd simple-chat
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# put your API key to the .env

streamlit run app.py

