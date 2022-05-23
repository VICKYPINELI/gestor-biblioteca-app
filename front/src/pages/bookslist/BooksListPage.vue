<template>
  <section>
    <div>
      <input type="text" placeholder="Buscar libro..." v-model="selectedText" />
      <select v-model="selectedCategory">
        <option class="desplegable-categorias" :value="null">
          Todas las categorias
        </option>
        <option
          v-for="category in categories"
          :value="category.category"
          :key="category.category_id"
        >
          {{ category.category }}
        </option>
      </select>
    </div>
    <article v-for="card in filteredCards" :key="card.ean">
      <!-- <img src="@/assets/img/libro.png" alt="Libro" /> -->
      <div>
      <h2 class="title">{{ card.title }}</h2>
      <h3 class="author">Autor: {{ card.author }}</h3>
      </div>
      <div>
      <button
        class="boton-detalles-libro"
        @click="$router.push(`/books/${card.id}`)"
      >
       + info
      </button>
      </div>
    </article>
  </section>
</template>

<script>
import { useStorage } from "@vueuse/core";
export default {
  data() {
    return {
      cards: [],
      selectedText: "",
      localUser: useStorage("user", {}),
      categories: [],
      selectedCategory: null,
    };
  },
  mounted() {
    this.loadData();
  },
  methods: {
    async loadData() {
      const endpoint = "http://localhost:5000/api/books";
      let response = await fetch(endpoint);
      this.cards = await response.json();

      const endpoint_categories = "http://localhost:5000/api/categories";
      let responsecat = await fetch(endpoint_categories);
      this.categories = await responsecat.json();
    },
  },

  computed: {
    filteredCards() {
      const selectedByTitle = (card) => {
        if (
          card.title.toLowerCase().includes(this.selectedText.toLowerCase()) ||
          this.selectedText === ""
        ) {
          return true;
        } else {
          return false;
        }
      };
      const selectedByCategory = (card) => {
        if (
          card.categories.includes(this.selectedCategory) ||
          this.selectedCategory === null
        ) {
          return true;
        } else {
          return false;
        }
      };
      return this.cards.filter(selectedByTitle).filter(selectedByCategory);
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
  border: 1px solid rgb(211, 207, 202);
  background-color: rgb(237, 243, 243);
  margin: 1em;
  padding: 1em;
  display: block;
  width: 80vw;
}
.author,
.publisher,
.ean {
  font-weight: 100vw;
  font-size: 15px;
}
.title {
  font-weight: bolder;
}
.add-book-button {
  float: left;
  margin-left: 3em;
  margin-top: 0.5em;
}
.boton-detalles-libro {
  font-weight: bold;
  padding: 0 0.5em;
  margin-top: 1em;
  
}
img {
  height: 50px;
}
.desplegable-categorias {
  font-weight: bold;
}
</style>
