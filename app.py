from flask import Flask, request
import requests
import os

app = Flask(__name__)
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')  # Agora lê do Vercel

@app.route('/webhook', methods=['POST'])
def webhook():
    user_message = request.form.get('Body', '').strip()
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": user_message}],
        "temperature": 0.7
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )
        response.raise_for_status()  # Levanta erro para status 4xx/5xx
        bot_response = response.json()["choices"][0]["message"]["content"]
        
        return f"""
        <Response>
            <Message>{bot_response}</Message>
        </Response>
        """
    
    except requests.exceptions.RequestException as e:
        print(f"Erro na API Groq: {str(e)}")
        return """
        <Response>
            <Message>⚠️ Erro temporário. Por favor, tente novamente.</Message>
        </Response>
        """
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        return """
        <Response>
            <Message>⚠️ Ops, tive um problema interno.</Message>
        </Response>
        """

# Removido app.run() pois o Vercel usa seu próprio servidor