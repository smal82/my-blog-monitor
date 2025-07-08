import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import MonitorView from "../views/MonitorView.vue";
import PostDetailView from "../views/PostDetailView.vue"; // Questo è il componente per il dettaglio del post

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/monitor",
    name: "monitor",
    component: MonitorView,
  },
  {
    path: "/post/:id", // Questa è la rotta per visualizzare il dettaglio di un singolo post
    name: "post-detail",
    component: PostDetailView,
    props: true, // Questo permette di passare l'ID del post come prop al componente PostDetailView
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
