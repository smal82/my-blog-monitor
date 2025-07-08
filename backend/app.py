import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime
import requests

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# --- Configurazione dell'Applicazione Flask ---
def create_app():
    app = Flask(__name__)

    # Configurazione della chiave segreta
    # Usa una stringa grezza (r'') per evitare SyntaxWarning con '\8'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # URL Base dell'API di WordPress per i post 'distro'
    WORDPRESS_API_BASE_URL = os.getenv('WORDPRESS_API_BASE_URL')
    if not WORDPRESS_API_BASE_URL:
        raise ValueError("WORDPRESS_API_BASE_URL non è impostato nel file .env")

    # Abilita CORS per permettere al frontend Vue.js di fare richieste
    # In produzione, è consigliato specificare l'origine esatta del tuo frontend:
    # CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})
    CORS(app)

    # --- Route API per i post di WordPress (di tipo "distro") ---
    # Queste route fungono da proxy verso l'API del tuo sito WordPress.

    @app.route('/api/distro-posts', methods=['GET'])
    def get_wordpress_distro_posts():
        try:
            search_query = request.args.get('search', '')
            params = {'search': search_query} if search_query else {}
            response = requests.get(f"{WORDPRESS_API_BASE_URL}/posts", params=params, timeout=10)
            response.raise_for_status() # Lancia un'eccezione per codici di stato HTTP di errore (4xx o 5xx)
            return jsonify(response.json())
        except requests.exceptions.Timeout:
            return jsonify({'message': 'Errore: Timeout della richiesta all\'API di WordPress.'}), 504
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Errore nel recupero dei post da WordPress: {str(e)}")
            return jsonify({'message': f'Errore nel recupero dei post da WordPress: {str(e)}'}), 500
        except Exception as e:
            app.logger.error(f"Errore inatteso nel recupero dei post: {str(e)}")
            return jsonify({'message': f'Errore inatteso: {str(e)}'}), 500


    @app.route('/api/distro-posts/<int:post_id>', methods=['GET'])
    def get_single_wordpress_distro_post(post_id):
        try:
            response = requests.get(f"{WORDPRESS_API_BASE_URL}/posts/{post_id}", timeout=10)
            response.raise_for_status()
            return jsonify(response.json())
        except requests.exceptions.Timeout:
            return jsonify({'message': 'Errore: Timeout della richiesta all\'API di WordPress.'}), 504
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Errore nel recupero del singolo post da WordPress (ID: {post_id}): {str(e)}")
            if response.status_code == 404:
                return jsonify({'message': 'Post WordPress non trovato.'}), 404
            return jsonify({'message': f'Errore nel recupero del post da WordPress: {str(e)}'}), 500
        except Exception as e:
            app.logger.error(f"Errore inatteso nel recupero del singolo post: {str(e)}")
            return jsonify({'message': f'Errore inatteso: {str(e)}'}), 500

    # --- Route per il monitoraggio del sito ---
    @app.route('/api/monitor', methods=['GET'])
    def monitor_site():
        site_url = "https://smal82.netsons.org"
        try:
            response = requests.get(site_url, timeout=5) # Prova a fare una richiesta al tuo sito
            status = "Online" if response.status_code == 200 else f"Offline (Codice: {response.status_code})"
            message = f"Sito raggiungibile. Codice HTTP: {response.status_code}"
        except requests.exceptions.RequestException as e:
            status = "Offline"
            message = f"Impossibile raggiungere il sito: {str(e)}"
        except Exception as e:
            status = "Errore"
            message = f"Errore generico nel monitoraggio: {str(e)}"

        return jsonify({
            'site': site_url,
            'status': status,
            'last_checked': datetime.utcnow().isoformat(),
            'message': message
        })

    return app

if __name__ == '__main__':
    app = create_app()
    # Per sviluppo:
    # app.run(debug=True, port=5000)
    # Per produzione con Waitress (su Windows), decommenta e commenta la riga sopra:
    from waitress import serve # Questa riga deve essere allineata con 'app = create_app()'
    print("Running Flask backend in production mode with Waitress...")
    serve(app, host="127.0.0.1", port=5000)