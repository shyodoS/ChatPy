from flask import Flask, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do arquivo .env

app = Flask(__name__)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Adicione sua chave no .env

@app.route('/webhook', methods=['POST'])
def webhook():
    # Recebe mensagem do Twilio (WhatsApp/SMS)
    user_message = request.form.get('Body', '').strip()

    # Configuração da API Groq
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama3-70b-8192",  # Modelo gratuito e poderoso
        "messages": [{"role": "user", "content": user_message}],
        "temperature": 0.7  # Controla a criatividade (0-1)
    }

    try:
        # Envia a requisição para a Groq
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )
        response_data = response.json()
        
        # Extrai a resposta do chatbot
        bot_response = response_data["choices"][0]["message"]["content"]
        
        # Formata a resposta para o Twilio
        return f"""
        <Response>
            <Message>{bot_response}</Message>
        </Response>
        """
    
    except Exception as e:
        print("Erro:", e)  # Debug
        return """
        <Response>
            <Message>⚠️ Ops, tive um problema. Tente novamente!</Message>
        </Response>
        """

if __name__ == '__main__':
    app.run(debug=True)