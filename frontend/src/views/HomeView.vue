<template>
  <div class="home-page">
    <h1>Latest Distro Posts from smal82.netsons.org</h1>
    <p class="subtitle">Scopri gli ultimi articoli sul tuo sito.</p>

    <div v-if="loading" class="loading-message">Caricamento post...</div>
    <div v-if="error" class="error-message">Errore: {{ error }}</div>

    <div class="posts-grid" v-if="!loading && !error">
      <div v-for="post in posts" :key="post.id" class="post-card">
        <router-link
          :to="{ name: 'post-detail', params: { id: post.id } }"
          class="post-link"
        >
          <div class="post-thumbnail-container">
            <img
              :src="
                post.featured_image_url ||
                'https://via.placeholder.com/300x200?text=No+Image'
              "
              :alt="post.title"
              class="post-thumbnail"
            />
          </div>
          <div class="post-content">
            <h2>{{ post.title }}</h2>
            <div class="post-excerpt" v-html="post.excerpt"></div>
            <p class="read-more">Leggi di più &raquo;</p>
          </div>
        </router-link>
      </div>
      <div v-if="posts.length === 0" class="no-posts-found">
        Nessun post di tipo "distro" trovato.
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "HomeView",
  data() {
    return {
      posts: [],
      loading: false,
      error: null,
    };
  },
  created() {
    this.fetchPosts();
  },
  methods: {
    async fetchPosts() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get("/api/distro-posts");

        this.posts = response.data.map((post) => {
          // L'immagine in evidenza è ora fornita direttamente dal campo featured_image_url
          // Non serve più la logica di _embedded
          let featuredImage = post.featured_image_url;

          // L'excerpt dovrebbe arrivare più pulito, ma lo puliamo ulteriormente se contiene HTML
          let cleanExcerpt = post.excerpt;
          if (cleanExcerpt) {
            const div = document.createElement("div");
            div.innerHTML = cleanExcerpt;
            cleanExcerpt = div.textContent || div.innerText || "";
            cleanExcerpt = cleanExcerpt.substring(0, 150); // Taglia a 150 caratteri se molto lungo
          }

          return {
            id: post.id,
            title: post.title, // Il titolo dovrebbe essere già pulito
            content: post.content,
            excerpt: cleanExcerpt,
            date: post.date,
            author_name: post.author_name,
            link: post.link,
            featured_image_url:
              featuredImage ||
              "https://via.placeholder.com/300x200?text=No+Image", // Fallback
          };
        });
      } catch (err) {
        console.error("Errore nel recupero dei post di WordPress:", err);
        this.error =
          "Impossibile recuperare i post. Controlla la console per i dettagli.";
        if (err.response && err.response.data && err.response.data.message) {
          this.error = `Errore: ${err.response.data.message}`;
        }
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped lang="scss">
/* Stili uguali a prima */
.home-page {
  padding: 40px 20px;
  text-align: center;
  background-color: #f8f9fa;
}

h1 {
  color: #343a40;
  margin-bottom: 10px;
  font-size: 2.5rem;
}

.subtitle {
  color: #6c757d;
  font-size: 1.1rem;
  margin-bottom: 30px;
}

.loading-message,
.error-message,
.no-posts-found {
  margin-top: 20px;
  padding: 15px;
  border-radius: 8px;
  font-size: 1.1rem;
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

.no-posts-found {
  background-color: #e2e3e5;
  color: #6c757d;
  border: 1px solid #adb5bd;
}

.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
}

.post-card {
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.post-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.post-link {
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.post-thumbnail-container {
  width: 100%;
  height: 200px; /* **Altezza fissa per il contenitore. L'immagine si adatterà a questo** */
  overflow: hidden;
  background-color: #ffffff; /* **AGGIUNTO: Sfondo bianco per il contenitore** */
  display: flex;
  align-items: center; /* Centra verticalmente l'immagine se più piccola */
  justify-content: center; /* Centra orizzontalmente l'immagine se più piccola */
}

.post-thumbnail {
  width: 100%; /* **L'immagine occupa il 100% della larghezza del contenitore** */
  height: 100%; /* **L'immagine occupa il 100% dell'altezza del contenitore** */
  object-fit: cover; /* **Fondamentale: copre il contenitore mantenendo le proporzioni e ritagliando se necessario** */
  display: block;
}

.post-content {
  padding: 20px;
  text-align: left;
  flex-grow: 1; /* Permette al contenuto di occupare lo spazio rimanente */
  display: flex;
  flex-direction: column;
}

.post-content h2 {
  font-size: 1.6rem;
  color: #007bff;
  margin-top: 0;
  margin-bottom: 10px;
  line-height: 1.3;
}

.post-excerpt {
  font-size: 0.95rem;
  color: #495057;
  line-height: 1.6;
  margin-bottom: 15px;
  flex-grow: 1;
}

.read-more {
  color: #28a745;
  font-weight: bold;
  font-size: 0.9rem;
  margin-top: auto; /* Spinge "Leggi di più" in basso */
}

@media (max-width: 768px) {
  .posts-grid {
    grid-template-columns: 1fr;
  }
}
</style>
