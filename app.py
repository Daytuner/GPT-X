from flask import Flask, request, render_template
from dotenv import load_dotenv
import os 
import openai 
import json 
import requests

def configure():
    load_dotenv()


openai.organization =os.getenv('ORGANISATION')
openai.api_key = os.getenv('API_KEY')



messages= [{    "role": "system", "content": "You are a kind helpful assistent."},]
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
   
    return render_template('index.html')

@app.route('/result',methods = ['GET','POST'])
def result():
    try:    
        if request.method == 'POST':
            ques = request.form['ques']
            
            URL = "https://api.openai.com/v1/chat/completions"

            payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": ques}],
            "temperature" : 1.0,
            "top_p":1.0,
            "n" : 1,
            "stream": False,
            "presence_penalty":0,
            "frequency_penalty":0,
            }

            headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai.api_key}"
            }

            response = requests.post(URL, headers=headers, json=payload, stream=False)
            y = json.loads(response.content)
            ans = y['choices'][0]['message']['content']

            return render_template('results.html',ans=ans)
        else:
            return render_template('index.html')
    except Exception as e:
        print(e)




if __name__ == '__main__':
    app.run(debug = True)
