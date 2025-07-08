<template>
  <div class="post-detail-page">
    <div v-if="loading" class="loading-message">Caricamento post...</div>
    <div v-if="error" class="error-message">Errore: {{ error }}</div>

    <div v-if="post" class="post-content-wrapper">
      <div class="post-detail-thumbnail-container">
        <img
          :src="
            post.featured_image_url ||
            'https://via.placeholder.com/600x400?text=No+Image'
          "
          :alt="post.title"
          class="post-detail-thumbnail"
        />
      </div>

      <h1 class="post-title">{{ post.title }}</h1>
      <div class="post-meta">
        Pubblicato il {{ formatDate(post.date) }} da {{ post.author_name }}
      </div>

      <div class="post-full-content" v-html="processedContent"></div>
    </div>

    <div v-if="!loading && !error && !post" class="no-post-found">
      Post non trovato.
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "PostDetailView",
  props: ["id"], // Riceve l'ID del post dalla rotta
  data() {
    return {
      post: null,
      loading: false,
      error: null,
    };
  },
  computed: {
    // Computed property per processare il contenuto prima di renderizzarlo
    processedContent() {
      if (!this.post || !this.post.content) {
        return "";
      }
      let content = this.post.content;
      let finalContent = "";
      let startIndex = 0;
      let magnetTagStart = content.indexOf("[magnet=", startIndex);

      while (magnetTagStart !== -1) {
        // Aggiungi la parte di contenuto prima del tag magnetico
        finalContent += content.substring(startIndex, magnetTagStart);

        // Trova la fine del tag magnetico
        const magnetTagEnd = content.indexOf("[/magnet]", magnetTagStart);

        if (magnetTagEnd === -1) {
          // Tag di chiusura non trovato, aggiungi il resto del contenuto e esci
          finalContent += content.substring(magnetTagStart);
          break;
        }

        const fullMagnetTag = content.substring(
          magnetTagStart,
          magnetTagEnd + "[/magnet]".length
        );

        // Estrai il nome e il link
        const nameStart = fullMagnetTag.indexOf("=");
        const nameEnd = fullMagnetTag.indexOf("]");
        const linkStart = nameEnd + 1;

        if (nameStart !== -1 && nameEnd !== -1 && linkStart !== -1) {
          const name = fullMagnetTag.substring(nameStart + 1, nameEnd);
          const link = fullMagnetTag.substring(
            linkStart,
            fullMagnetTag.indexOf("[/magnet]")
          );

          // Decodifica le entità HTML nel link (se necessario)
          const decodedLink = link.replace(/&amp;/g, "&");

          // Costruisci il tag <a> con l'immagine al posto del testo
          // Aggiungi una classe per poter stilizzare l'immagine se necessario
          finalContent += `<a href="${decodedLink}" class="magnet-link-icon" title="Scarica ${name}" data-name="${name}">
                               <img src="https://i.postimg.cc/JnHPtdGJ/Magnet-Icon2.png" alt="Magnet link per ${name}" class="magnet-icon" />
                           </a>`;
        } else {
          // Fallback: se il parsing fallisce, aggiungi il tag così com'è
          finalContent += fullMagnetTag;
        }

        startIndex = magnetTagEnd + "[/magnet]".length;
        magnetTagStart = content.indexOf("[magnet=", startIndex);
      }

      // Aggiungi l'eventuale parte finale del contenuto dopo l'ultimo tag magnetico
      finalContent += content.substring(startIndex);

      return finalContent;
    },
  },
  watch: {
    // Osserva i cambiamenti dell'ID nella rotta, utile se navighi tra post senza ricaricare la pagina
    id: "fetchPost",
  },
  created() {
    this.fetchPost();
  },
  methods: {
    async fetchPost() {
      this.loading = true;
      this.error = null;
      this.post = null; // Resetta il post precedente

      try {
        const response = await axios.get(`/api/distro-posts/${this.id}`);
        this.post = response.data;
      } catch (err) {
        console.error("Errore nel recupero del post:", err);
        if (err.response && err.response.status === 404) {
          this.error = "Post non trovato.";
        } else if (
          err.response &&
          err.response.data &&
          err.response.data.message
        ) {
          this.error = `Errore: ${err.response.data.message}`;
        } else {
          this.error =
            "Si è verificato un errore durante il caricamento del post.";
        }
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateString) {
      if (!dateString) return "N/A";
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(dateString).toLocaleDateString("it-IT", options);
    },
  },
};
</script>

<style scoped>
/* Il resto dello stile rimane invariato, come te l'ho fornito in precedenza */
.post-detail-page {
  padding: 40px 20px;
  max-width: 900px;
  margin: 0 auto;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.loading-message,
.error-message,
.no-post-found {
  margin-top: 20px;
  padding: 15px;
  border-radius: 8px;
  font-size: 1.1rem;
  text-align: center;
}

.loading-message {
  background-color: #e9f5ff;
  color: #007bff;
  border: 1px solid #007bff;
}

.error-message {
  background-color: #fff3cd;
  color: #dc3545;
  border: 1px solid #dc3545;
}

.no-post-found {
  background-color: #e2e3e5;
  color: #6c757d;
  border: 1px solid #adb5bd;
}

.post-content-wrapper {
  background-color: #ffffff;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.post-detail-thumbnail-container {
  width: 100%;
  max-height: 400px; /* Altezza massima per evitare immagini enormi */
  overflow: hidden;
  margin-bottom: 25px;
  border-radius: 8px;
  background-color: #ffffff; /* Sfondo bianco per il contenitore */
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.post-detail-thumbnail {
  width: 100%; /* L'immagine occupa il 100% della larghezza */
  height: 100%; /* L'immagine occupa il 100% dell'altezza del contenitore */
  object-fit: contain; /* **Modificato: `contain` per mostrare l'intera immagine all'interno del contenitore senza ritaglio** */
  display: block;
}

.post-title {
  font-size: 2.8rem;
  color: #343a40;
  margin-bottom: 15px;
  line-height: 1.2;
  text-align: center;
}

.post-meta {
  font-size: 0.95rem;
  color: #6c757d;
  margin-bottom: 30px;
  text-align: center;
}

.post-full-content {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #343a40;
  text-align: left;
}

/* Stili per il contenuto HTML renderizzato dall'API */
.post-full-content >>> p {
  margin-bottom: 1em;
}

.post-full-content >>> h1,
.post-full-content >>> h2,
.post-full-content >>> h3,
.post-full-content >>> h4,
.post-full-content >>> h5,
.post-full-content >>> h6 {
  margin-top: 1.5em;
  margin-bottom: 0.8em;
  color: #007bff;
}

.post-full-content >>> ul,
.post-full-content >>> ol {
  margin-bottom: 1em;
  padding-left: 1.5em;
}

.post-full-content >>> a {
  color: #28a745;
  text-decoration: none;
  font-weight: bold;
}

.post-full-content >>> a:hover {
  text-decoration: underline;
}

.post-full-content >>> img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 20px auto;
  border-radius: 5px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Nuovi stili per il link magnetico con immagine */
.post-full-content >>> .magnet-link-icon {
  display: inline-flex; /* Usa flexbox per centrare l'immagine se necessario */
  align-items: center;
  justify-content: center;
  border: none; /* Rimuovi il bordo del "button" precedente */
  background: none; /* Rimuovi lo sfondo del "button" precedente */
  padding: 0; /* Rimuovi padding */
  margin: 5px 10px 5px 0; /* Spazio intorno all'icona */
  vertical-align: middle; /* Allinea l'icona con il testo adiacente */
  transition: transform 0.2s ease-in-out;
}

.post-full-content >>> .magnet-link-icon:hover {
  transform: translateY(-2px); /* Un piccolo effetto al passaggio del mouse */
  text-decoration: none; /* Assicurati che non ci sia sottolineatura */
}

.post-full-content >>> .magnet-icon {
  width: 320px; /* Dimensione dell'icona (puoi cambiarla) */
  height: auto; /* Mantieni proporzioni */
  display: block; /* Rimuovi spazio extra sotto l'immagine */
  border: none; /* Assicurati che l'immagine non abbia un bordo */
  box-shadow: none; /* Rimuovi eventuali ombre predefinite */
  margin: 0; /* Rimuovi margini predefiniti */
}
</style>
