<template>
  <section class="dashboard">
    <div>
      <router-link to="/books"><button>Lista de libros</button></router-link>
    </div>
    <div>
      <router-link to="/librarian/loans"
        ><button>Prestamos de  los Usuarios</button>
      </router-link>
    </div>
    <div>
      <router-link to="/books/add"> <button>Añadir libro</button></router-link>
    </div>
  </section>
</template>

<script>
import { useStorage } from "@vueuse/core";

export default {
  data() {
    return {
      localUser: useStorage("user", {}),
    };
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Lora:ital@1&family=Raleway:wght@300&display=swap");
* {
  font-family: "Raleway", sans-serif;
}
section {
  display: flex;
  justify-content: center;
}

div button {
  background-color: #799d7bb2;
  border: none;
  color: rgb(17, 12, 12);
  padding: 1em 2em;
  text-decoration: none;
  font-size: 16px;
  margin: 0.5em 3em;
}
</style>