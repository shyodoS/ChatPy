from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Configuração otimizada para Vercel
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Verifica se a chave API está disponível
        groq_api_key = os.environ.get('GROQ_API_KEY')
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY não configurada")

        user_message = request.form.get('Body', '').strip()
        
        headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "llama3-70b-8192",
            "messages": [{"role": "user", "content": user_message}],
            "temperature": 0.7
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=10  # Timeout de 10 segundos
        )
        response.raise_for_status()
        
        bot_response = response.json()["choices"][0]["message"]["content"]
        
        return f"""
        <Response>
            <Message>{bot_response}</Message>
        </Response>
        """
        
    except Exception as e:
        print(f"ERRO CRÍTICO: {str(e)}")
        return """
        <Response>
            <Message>⚠️ Serviço temporariamente indisponível</Message>
        </Response>
        """, 500

# Handler para erros 404
@app.errorhandler(404)
def not_found(e):
    return jsonify(error="Endpoint não encontrado"), 404

# Handler para erros 500
@app.errorhandler(500)
def server_error(e):
    return jsonify(error="Erro interno do servidor"), 500