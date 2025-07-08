# My Blog Monitor 📊

Un'applicazione web moderna, sviluppata con **Vue.js (Frontend)** e **Flask (Backend)**, progettata per visualizzare i contenuti di un blog WordPress. Questo progetto recupera gli articoli del custom post type "distro" da `smal82.netsons.org` e li presenta attraverso un'interfaccia pulita e responsiva.

## ✨ Funzionalità Principali

  * **Visualizzazione Post Recenti**: Mostra gli ultimi post del tipo "distro" in una griglia intuitiva e facile da navigare.
  * **Pagine di Dettaglio Post**: Ogni post ha una sua pagina dedicata che mostra il contenuto completo, inclusa l'immagine in evidenza per un'esperienza visiva ricca.
  * **Gestione Avanzata Link Magnetici**: I tag `[magnet=NomeFile]link_magnetico[/magnet]` nel contenuto dei post vengono automaticamente trasformati in icone cliccabili, semplificando il download per gli utenti.
  * **Design Responsivo**: L'applicazione è ottimizzata per garantire un'esperienza utente eccellente su desktop, tablet e smartphone.
  * **API WordPress Personalizzata**: Un plugin WordPress dedicato espone gli endpoint necessari per il recupero dei dati in modo efficiente e sicuro.
## 🚀 Come Iniziare

Segui questi passaggi per configurare ed avviare il progetto in locale sul tuo sistema.

### Prerequisiti

Assicurati di aver installato i seguenti strumenti:

  * [**Node.js**](https://nodejs.org/en/) (versione LTS raccomandata, include npm)
  * [**Python 3**](https://www.python.org/downloads/) (versione 3.8 o superiore)
  * [**Git**](https://git-scm.com/downloads)

### ⬇️ Installazione

1.  **Clona il repository**:
    Apri il terminale (o Git Bash su Windows) e clona il progetto:

    ```bash
    git clone https://github.com/smal82/my-blog-monitor.git
    cd my-blog-monitor
    ```

2.  **Configurazione del Backend (Flask)**:
    Naviga nella directory `backend`, installa le dipendenze Python e configura la `SECRET_KEY`.

    ```bash
    cd backend
    pip install -r requirements.txt
    ```

    Crea un file chiamato **`.env`** all'interno della directory `backend/` e aggiungi la tua chiave segreta. **Non caricare mai questo file su GitHub.**

    ```
    SECRET_KEY=UnaChiaveSegretaMoltoLungaEComplessaCheNonDeveEsserePubblica
    ```

    *Sostituisci il valore con una stringa casuale molto complessa.*

3.  **Configurazione del Frontend (Vue.js)**:
    Torna alla directory radice del progetto e poi naviga nella directory `frontend`:

    ```bash
    cd ..
    cd frontend
    npm install
    ```

### ▶️ Avvio del Progetto

Per avviare l'applicazione, dovrai eseguire il backend Flask e il frontend Vue.js in due terminali separati.

1.  **Avvia il Backend (nel primo terminale, dalla cartella `backend/`)**:

    ```bash
    cd backend
    python app.py
    ```

    Il backend sarà disponibile su `http://127.0.0.1:5000`.

2.  **Avvia il Frontend (nel secondo terminale, dalla cartella `frontend/`)**:

    ```bash
    cd frontend
    npm run serve
    ```

    Il frontend sarà disponibile su `http://localhost:8080` (o una porta simile, indicata dal terminale).

Apri il tuo browser e vai a `http://localhost:8080` per vedere l'applicazione in funzione\!

## ⚙️ Struttura del Progetto

Il repository è organizzato in una struttura chiara per separare il frontend dal backend:

```
my-blog-monitor/
├── backend/                  # Contiene l'applicazione Flask (API WordPress)
│   ├── .env                  # Variabili d'ambiente sensibili (IGNORATO da Git)
│   ├── app.py                # Codice principale del backend Flask
│   ├── requirements.txt      # Dipendenze Python del backend
│   └── ...                   # Altri file e cartelle del backend
├── frontend/                 # Contiene l'applicazione Vue.js
│   ├── node_modules/         # Dipendenze Node.js (IGNORATO da Git)
│   ├── public/               # File statici (index.html, favicon, ecc.)
│   ├── src/                  # Codice sorgente Vue.js
│   │   ├── assets/           # Immagini, icone, ecc.
│   │   ├── components/       # Componenti Vue riutilizzabili
│   │   ├── router/           # Configurazione delle rotte Vue Router
│   │   ├── views/            # Viste (pagine) principali dell'applicazione
│   │   ├── App.vue           # Componente radice dell'applicazione Vue
│   │   └── main.js           # Punto di ingresso dell'applicazione Vue
│   ├── .gitignore            # Regole di ignorazione per Git specifiche del frontend
│   ├── package.json          # Dipendenze e script npm del frontend
│   └── ...                   # Altri file di configurazione del frontend
├── .gitignore                # Regole di ignorazione globali per Git
└── README.md                 # Questo file
```
## 🤝 Contribuisci

Se desideri contribuire al progetto, sei il benvenuto\! Puoi segnalare bug, suggerire nuove funzionalità o inviare pull request.

1.  Forka il repository.
2.  Crea un nuovo branch (`git checkout -b feature/la-tua-feature`).
3.  Apporta le tue modifiche e committa (`git commit -m 'Aggiungi feature X'`).
4.  Esegui il push del tuo branch (`git push origin feature/la-tua-feature`).
5.  Apri una Pull Request.

## 📄 Licenza

Questo progetto è distribuito sotto licenza **MIT**. Puoi consultare il file `LICENSE` (se presente) nella radice del repository per maggiori dettagli. Se non presente, considera di aggiungerlo.
