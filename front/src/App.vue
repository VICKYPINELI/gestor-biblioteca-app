<template>
  <header>
    <div>
      <h1>LIGURUTEGI</h1>
      <select
        class="user-navigator"
        name="user"
        @change="selectRoute"
        v-model="selectedRoute"
        v-show="onLoginPage"
      >
        <option :value="null">Hola, {{ localUser.user }}</option>
        <option value="home-page-librarian" v-if="localUser.isLibrarian">
          Home
        </option>
        <option value="home-page-usuary" v-else>Home</option>
        <option value="book-page">Lista de libros</option>
        <option value="loans" v-if="localUser.isLibrarian">
          Prestamos de Usuarios
        </option>
        <option value="add-book" v-if="localUser.isLibrarian">
          Añadir libro
        </option>
        <option value="finish-sesion">Cerrar sesion</option>
      </select>
    </div>
  </header>

  <router-view />
</template>

<script>
import { useStorage } from "@vueuse/core";

export default {
  name: "Header",

  data() {
    return {
      localUser: useStorage("user", {}),
      selectedRoute: null,
      onLoginPage: true,
    };
  },

  methods: {
    selectRoute() {
      console.log("selectRoute", this.selectedRoute);
      if (this.selectedRoute === "home-page-librarian") {
        this.$router.push("/librarian/dashboard");
      } else if (this.selectedRoute === "home-page-usuary") {
        this.$router.push("/user/my-account");
      } else if (this.selectedRoute === "book-page") {
        this.$router.push("/books");
      } else if (this.selectedRoute === "loans") {
        this.$router.push("/user/my-account");
      } else if (this.selectedRoute === "add-book") {
        this.$router.push("/books/add");
      } else if (this.selectedRoute === "finish-sesion") {
        this.$router.push("/");
      }
    },
  },
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Lora:ital@1&family=Nunito+Sans:wght@200&family=Press+Start+2P&display=swap");
* {
  margin: 0;
  padding: 0;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
}

header {
  background-color: rgb(67, 133, 184);
  padding-bottom: 1rem;
  padding-top: 1rem;
  margin-bottom: 1rem;
  color: rgb(248, 252, 255);
}
.user-navigator {
  margin: 10px;
  width: 40vw;
  border: none;
  background-color: transparent;
  font-size: 20px;
  color: rgb(177, 210, 238);
}
</style>