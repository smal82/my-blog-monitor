<template>
  <div class="monitor-container">
    <h1>Monitoraggio Sito: smal82.netsons.org</h1>
    <div v-if="monitorData" class="monitor-status">
      <p>
        Stato:
        <span
          :class="{
            'status-online': monitorData.status === 'Online',
            'status-offline': monitorData.status === 'Offline',
          }"
          >{{ monitorData.status }}</span
        >
      </p>
      <p>
        Ultimo controllo:
        {{ new Date(monitorData.last_checked).toLocaleString() }}
      </p>
      <p>{{ monitorData.message }}</p>
    </div>
    <div v-else>
      <p>Caricamento dati di monitoraggio...</p>
    </div>
    <button @click="fetchMonitorStatus" class="refresh-button">
      Aggiorna Stato
    </button>
    <p class="note">
      Nota: Per un monitoraggio reale, dovrai implementare la logica nel backend
      Flask per fare richieste effettive al tuo sito.
    </p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "MonitorView",
  data() {
    return {
      monitorData: null,
    };
  },
  created() {
    this.fetchMonitorStatus();
  },
  methods: {
    async fetchMonitorStatus() {
      try {
        const response = await axios.get("/api/monitor");
        this.monitorData = response.data;
      } catch (error) {
        console.error(
          "Errore nel recupero dello stato del monitoraggio:",
          error
        );
        this.monitorData = {
          site: "smal82.netsons.org",
          status: "Offline",
          last_checked: new Date().toISOString(),
          message: "Impossibile connettersi al server di monitoraggio.",
        };
      }
    },
  },
};
</script>

<style scoped lang="scss">
.monitor-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

.monitor-status {
  margin-top: 30px;
  padding: 25px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #eaf7ed;
  border: 1px solid #c8e6c9;
}

.status-online {
  color: #28a745;
  font-weight: bold;
}

.status-offline {
  color: #dc3545;
  font-weight: bold;
}

.refresh-button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;

  &:hover {
    background-color: #0056b3;
  }
}

.note {
  margin-top: 20px;
  font-size: 0.9em;
  color: #666;
  font-style: italic;
}
</style>
