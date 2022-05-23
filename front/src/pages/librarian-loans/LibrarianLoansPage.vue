<template>
  <h1>Libros reservados</h1>
  <section>
    <article v-for="loan in loans" :key="loan.loan_id">
      <img src="@/assets/img/logoliburu.png" alt="Libro" />
      <h2>Libro: {{ loan.title }}</h2>
      <h2>Usuario: {{ loan.user }}</h2>
    </article>
  </section>
</template>

<script>
import { useStorage } from "@vueuse/core";
export default {
  name: "LibrarianLoans",
  data() {
    return {
      loans: [],
      localUser: useStorage("user", {}),
    };
  },

  mounted() {
    this.loadData();
  },

  methods: {
    async loadData() {
      let settings = { headers: { Authorization: this.localUser.userId } };
      const endpoint = "http://localhost:5000/api/loans";
      let respone = await fetch(endpoint, settings);
      this.loans = await respone.json();
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Lora:ital@1&family=Raleway:wght@300&display=swap");
* {
  font-family: "Raleway", sans-serif;
}

article {
  margin: 2em;
  padding: 1em;
  border: 4px solid rgba(91, 99, 91, 0.377);
  background-color: rgba(184, 187, 192, 0.63);
  border-radius: 1em;
}
.edit {
  margin-left: 2em;
}
img {
  width: 70px;
}
</style>
