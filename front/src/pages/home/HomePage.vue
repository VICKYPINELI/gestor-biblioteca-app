<template>
  <div class="home">
    <img alt="Vue logo" src="@/assets/img/logoliburu.png" />
    <h1>WELCOME</h1>
    <h3>Inicio de sesión</h3>
  </div>
  <select v-model="selectedUser">
    <option :value="null" disabled>Selecciona un usuario</option>
    <option v-for="user in users" :value="user" :key="user.id">
      {{ user.user }}
    </option>
  </select>
  <button @click="onButtonClicked">Acceder</button>
</template>

<script>
import { useStorage } from "@vueuse/core";

export default {
  name: "Home",
  data() {
    return {
      info: {},
      users: [],
      selectedUser: null,
      localUser: useStorage("user", {}),
      onLoginPage: false,
    };
  },
  mounted() {
    this.loadData();
  },
  methods: {
    async loadData() {
      const response = await fetch("http://localhost:5000/api/users");
      this.users = await response.json();
    },
    onButtonClicked() {
      this.localUser = {
        userId: this.selectedUser.user_id,
        user: this.selectedUser.user,
        isLibrarian: this.selectedUser.is_librarian,
      };
      if (this.localUser.isLibrarian == 1) {
        this.$router.push("/librarian/dashboard");
      } else {
        this.$router.push("/books");
      }
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Lora:ital@1&family=Nunito+Sans:wght@200&family=Press+Start+2P&display=swap");
* {
  font-family: "Nunito Sans", sans-serif;
}
body{
  height: 95vh;
}
h1 {
  font-style: italic;
}
button {
  margin: 1em;
  font-weight: bold;
  padding: 0 0.2em;
}
</style>
