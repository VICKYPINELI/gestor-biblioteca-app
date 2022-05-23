<template>
  <button @click="$router.go(-1)">↩</button>
  <h1>Añadir libro</h1>

  <form>
    <label for="title">Título</label>
    <input type="text" name="título" v-model="title" required />
    <label for="author">Autor </label>
    <input type="text" name="autor" v-model="author" required />
    <label for="publisher">Editorial </label>
    <input type="text" name="editorial" v-model="publisher" required />
    <label for="ean">Ean </label>
    <input type="text" name="ean" v-model="ean" required />
  </form>
  <p><b>Categorias</b></p>
  <section class="categories">
    <div v-for="category of categories" :key="category">
      <input
        type="checkbox"
        :id="category.category_id"
        :value="category.category_id"
        v-model="selectedCategoriesList"
      />
      <label>{{ category.category }} </label>
    </div>
    <br />
  </section>
  <button @click.prevent="addNewBook">Guardar</button>
</template>

<script>
import { useStorage } from "@vueuse/core";
import { v4 as uuidv4 } from "uuid";
export default {
  data() {
    return {
      title: "",
      author: "",
      publisher: "",
      ean: "",
      categories: [],
      localUser: useStorage("user", {}),
      selectedCategoriesList: [],
    };
  },
  mounted() {
    this.loadData();
  },
  methods: {
    async addNewBook() {
      let bookId = uuidv4();
      if (
        this.title != "" &&
        this.author != "" &&
        this.publisher != "" &&
        this.ean != "" &&
        this.categories != []
      ) {
        let newBook = {
          id: bookId,
          title: this.title,
          author: this.author,
          publisher: this.publisher,
          ean: this.ean,
          categories: this.selectedCategoriesList,
        };

        const settings = {
          method: "POST",
          body: JSON.stringify(newBook),
          headers: {
            "Content-Type": "application/json",
            Authorization: this.localUser.userId,
          },
        };
        console.log(settings);
        let response = await fetch("http://localhost:5000/api/books", settings);

        this.$router.push(`/books`);
        return response;
      }
    },
    async loadData() {
      const endpoint_categories = "http://localhost:5000/api/categories";
      let responsecat = await fetch(endpoint_categories);
      this.categories = await responsecat.json();
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Lora:ital@1&family=Raleway:wght@300&display=swap");
* {
  font-family: "Raleway", sans-serif;
}
h1 {
  font-size: 25px;
  text-decoration: underline;
  margin-bottom: 2em;
}
form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  margin-bottom: 2em;
}
form label {
  font-weight: bold;
  margin-left: 50%;
}
label,
input {
  margin-top: 1em;
}
form input {
  margin-right: 40em;
  padding: 5px;
}

button {
  padding: 0 1em;
}
.categories {
  display: grid;
  grid-template-rows: repeat(2, 1fr);
  grid-gap: 10px;
  margin-bottom: 1em;
}
</style>