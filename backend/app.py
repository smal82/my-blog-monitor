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
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # URL Base dell'API di WordPress per i post 'distro'
    WORDPRESS_API_BASE_URL = os.getenv('WORDPRESS_API_BASE_URL')
    if not WORDPRESS_API_BASE_URL:
        # Questo caso è una configurazione mancante, è accettabile che l'errore sia specifico
        raise ValueError("WORDPRESS_API_BASE_URL non è impostato nel file .env")

    # Abilita CORS per permettere al frontend Vue.js di fare richieste
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
            app.logger.error("Errore: Timeout della richiesta all'API di WordPress per i post.")
            return jsonify({'message': 'Si è verificato un errore di timeout durante il recupero dei post.'}), 504
        except requests.exceptions.RequestException as e:
            # Logga l'errore completo per il debug interno
            app.logger.error(f"Errore nel recupero dei post da WordPress: {str(e)}")
            # Ritorna un messaggio generico all'utente
            return jsonify({'message': 'Impossibile recuperare i post dal blog. Riprova più tardi.'}), 500
        except Exception as e:
            # Logga l'errore completo per il debug interno
            app.logger.error(f"Errore inatteso nel recupero dei post: {str(e)}")
            # Ritorna un messaggio generico all'utente
            return jsonify({'message': 'Si è verificato un errore inatteso. Contatta l\'amministratore.'}), 500


    @app.route('/api/distro-posts/<int:post_id>', methods=['GET'])
    def get_single_wordpress_distro_post(post_id):
        try:
            response = requests.get(f"{WORDPRESS_API_BASE_URL}/posts/{post_id}", timeout=10)
            response.raise_for_status()
            return jsonify(response.json())
        except requests.exceptions.Timeout:
            app.logger.error(f"Errore: Timeout della richiesta all'API di WordPress per il singolo post (ID: {post_id}).")
            return jsonify({'message': 'Si è verificato un errore di timeout durante il recupero del post.'}), 504
        except requests.exceptions.RequestException as e:
            # Logga l'errore completo per il debug interno
            app.logger.error(f"Errore nel recupero del singolo post da WordPress (ID: {post_id}): {str(e)}")
            # Gestione specifica per 404, altrimenti messaggio generico
            if hasattr(e, 'response') and e.response.status_code == 404:
                return jsonify({'message': 'Post WordPress non trovato.'}), 404
            # Ritorna un messaggio generico all'utente
            return jsonify({'message': 'Impossibile recuperare il post dal blog. Riprova più tardi.'}), 500
        except Exception as e:
            # Logga l'errore completo per il debug interno
            app.logger.error(f"Errore inatteso nel recupero del singolo post: {str(e)}")
            # Ritorna un messaggio generico all'utente
            return jsonify({'message': 'Si è verificato un errore inatteso. Contatta l\'amministratore.'}), 500

    # --- Route per il monitoraggio del sito ---
    @app.route('/api/monitor', methods=['GET'])
    def monitor_site():
        site_url = "https://smal82.netsons.org"
        status = "Errore" # Default in caso di eccezione non catturata specificatamente
        message = "Si è verificato un errore inatteso durante il monitoraggio." # Default
        
        try:
            response = requests.get(site_url, timeout=5) # Prova a fare una richiesta al tuo sito
            response.raise_for_status() # Lancia eccezione per 4xx/5xx
            status = "Online"
            message = f"Sito raggiungibile. Codice HTTP: {response.status_code}"
        except requests.exceptions.Timeout:
            app.logger.error(f"Errore: Timeout nella verifica di raggiungibilità del sito {site_url}.")
            status = "Offline"
            message = "Timeout nella verifica della raggiungibilità del sito."
        except requests.exceptions.RequestException as e:
            # Logga l'errore completo per il debug interno
            app.logger.error(f"Impossibile raggiungere il sito {site_url}: {str(e)}")
            # Ritorna un messaggio generico all'utente
            status = "Offline"
            message = "Impossibile raggiungere il sito. Verifica la connessione."
        except Exception as e:
            # Logga l'errore completo per il debug interno
            app.logger.error(f"Errore generico inatteso nel monitoraggio del sito {site_url}: {str(e)}")
            # Ritorna un messaggio generico all'utente
            status = "Errore"
            message = "Errore interno durante il monitoraggio del sito."

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
    from waitress import serve
    print("Running Flask backend in production mode with Waitress...")
    serve(app, host="127.0.0.1", port=5000)
