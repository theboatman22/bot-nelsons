from flask import Flask, render_template, request, jsonify
import requests
import json
import os

app = Flask(__name__)

# Configuração da API do DeepSeek
DEEPSEEK_API_URL = "https://api.openrouter.ai/api/v1/chat/completions"
# IMPORTANTE: Configure sua API Key como variável de ambiente
# export DEEPSEEK_API_KEY="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"
DEEPSEEK_API_KEY = os.environ.get("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")

# Sistema de prompt para garantir que o bot fale apenas sobre Clash Royale
SYSTEM_PROMPT = """
Você é um especialista em Clash Royale. Sua função é fornecer dicas, estratégias e conselhos sobre o jogo Clash Royale.

REGRAS ESTRITAS:
1. Você deve responder APENAS sobre Clash Royale. 
2. Se o usuário fizer perguntas sobre outros tópicos, responda educadamente que você só pode ajudar com Clash Royale.
3. Foque em ajudar o usuário "gustavoweb" a melhorar suas habilidades no jogo.
4. Forneça dicas sobre:
   - Estratégias de deck building
   - Gerenciamento de elixir
   - Posicionamento de tropas
   - Contra-ataques
   - Ciclos de cartas
   - Meta atual do jogo
   - Como contra-atacar decks populares
5. Seja encorajador e construtivo em suas respostas.

Lembre-se: você está falando especificamente com "gustavoweb" para ajudá-lo a melhorar no Clash Royale.
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    if not user_message.strip():
        return jsonify({'error': 'Mensagem vazia'}), 400
    
    # Preparar a mensagem para a API do DeepSeek
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {DEEPSEEK_API_KEY}'
    }
    
    payload = {
        'model': 'deepseek-chat',
        'messages': [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': user_message}
        ],
        'temperature': 0.7,
        'max_tokens': 500
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        bot_response = data['choices'][0]['message']['content']
        
        return jsonify({'response': bot_response})
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Erro na comunicação com a API: {str(e)}'}), 500
    except KeyError as e:
        return jsonify({'error': 'Resposta da API em formato inesperado'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)