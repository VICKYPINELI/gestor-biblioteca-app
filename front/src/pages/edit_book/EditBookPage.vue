<template>
  <form>
    <section class="book-info-wrapper">
      <div>
        <label for="title">Título:</label>
        <input
          type="text"
          name="título"
          v-model="modifiedBook.title"
          required
        />
      </div>
      <div>
        <label for="author">Autor: </label>
        <input
          type="text"
          name="autor"
          v-model="modifiedBook.author"
          required
        />
      </div>
      <div>
        <label for="publisher">Editorial: </label>
        <input
          type="text"
          name="editorial"
          v-model="modifiedBook.publisher"
          required
        />
      </div>
      <div>
        <label for="ean">Ean: </label>
        <input type="number" name="ean" v-model="modifiedBook.ean" required />
      </div>
    </section>
    <p class="titulo-categorias">Categorias del libro:</p>
    <section
      class="categories-wrapper"
      v-for="category of categories"
      :key="category.category_id"
    >
      <input
        class="categories-checkbox"
        type="checkbox"
        :id="category.category_id"
        :value="category.category"
        :checked="isChecked(category.category_id)"
        v-model="modifiedCategories"
      />

      <label :for="category.category_id" class="category-name"
        >{{ category.category }}
        <!-- {{ category.category_id }} -->
      </label>
    </section>
    <br />
    <!-- {{ modifiedCategories }} -->
  </form>
  <br />

  <button class="boton-guardar-cambios" @click.prevent="editBook">
    Guardar Cambios
  </button>
</template>


    


<script>
import { useStorage } from "@vueuse/core";
export default {
  data() {
    return {
      bookId: this.$route.params.id,
      book: {},
      modifiedBook: {},
      categories: [],
      localUser: useStorage("user", {}),
      modifiedCategories: [],
    };
  },
  mounted() {
    this.loadData();
  },
  methods: {
    async loadData() {
      //Carga los datos del libro en la variable "book"
      let endpoint = "http://localhost:5000/api/books/" + this.bookId;
      let response = await fetch(endpoint);
      this.book = await response.json();

      // Creamos la variable "modifiedBook" y "modifiedCategories" con 2 objetivos:
      // 1 - Cuando se carga la página: Para enseñar los datos del libro y sus categorias
      // 2 - Para comprobar si el usuario ha editado algo:
      //     comparando los datos de  "book" y ("modifiedBook" + "modifiedCategories")

      this.modifiedBook.id = this.book.id;
      this.modifiedBook.title = this.book.title;
      this.modifiedBook.author = this.book.author;
      this.modifiedBook.publisher = this.book.publisher;
      this.modifiedBook.ean = this.book.ean;

      this.modifiedCategories = this.book.categories;

      //Carga todas las categorias que tenemos en el back y las guarda en "categories"
      const endpoint_categories = "http://localhost:5000/api/categories";
      let responsecat = await fetch(endpoint_categories);
      this.categories = await responsecat.json();
    },

    isChecked(id_cat) {
      console.log(id_cat, this.modifiedCategories.keys);
      return id_cat in this.modifiedCategories.keys;
    },

    isEmptyBook() {
      return (
        this.modifiedBook.title === "" ||
        this.modifiedBook.author === "" ||
        this.modifiedBook.publisher === "" ||
        this.modifiedBook.ean === ""
      );
    },

    isEditedBook() {
      return (
        this.book.title != this.modifiedBook.title ||
        this.book.author != this.modifiedBook.author ||
        this.book.publisher != this.modifiedBook.publisher ||
        this.book.ean != this.modifiedBook.ean
      );
    },

    isEditedCategories() {
      return this.book.categories != this.modifiedCategories;
    },

    async editBook() {
      let estaModificadoLibro =
        this.book.title != this.modifiedBook.title ||
        this.book.author != this.modifiedBook.author ||
        this.book.publisher != this.modifiedBook.publisher ||
        this.book.ean != this.modifiedBook.ean;

      let estanModificadasCategorias =
        this.book.categories != this.modifiedCate;
      console.log("*** ¿se ha modificado el Libro? ****", estaModificadoLibro);
      console.log(
        "*** ¿se ha modificado categorias? ****",
        estanModificadasCategorias
      );

      console.log("this.modifiedCategories: ---> ", this.modifiedCategories);

      console.log("this.book+: ---> ", this.book);
      console.log("this.modifiedCategories: ---> ", this.modifiedCategories);

      //  categories=body["categories"]
      // book_id=body["book_id"]

      if (this.isEditedBook()) {
        if (confirm("¿Está seguro de que quiere editar este libro?")) {
          const settings = {
            method: "PUT",
            body: JSON.stringify(this.modifiedBook),
            headers: {
              "Content-Type": "application/json",
              Authorization: this.localUser.userId,
            },
          };
          let endpoint = "http://localhost:5000/api/books/" + this.bookId;
          await fetch(endpoint, settings);
        } //fin del if CONFIRM
      }

      if (this.isEditedCategories()) {
        //Para que sólo se vea un mensaje //editar: - el libro o -las categorias
        if (!this.isEditedBook()) {
          confirm("¿Está seguro de que quiere editar las categorías?");
        }

        // Convertir la lista de nombres de cat. en >> lista de category_id de tipo INTEGER
        let categoriesIdList = [];
        for (let category of this.categories) {
          console.log(category.category);
          console.log(category.category_id);

          if (this.modifiedCategories.includes(category.category)) {
            let id = String(category.category_id);
            id = parseInt(id);

            //id = parseInt(id)

            categoriesIdList.push(id);
          }
        }
        console.log("categoriesIdList: - " + categoriesIdList);

        // Convertir la lista de nombres de cat. en >> lista de category_id de tipo INTEGER

        let list_contrato_de_negocio = {
          book_id: this.modifiedBook.id,
          categories: categoriesIdList, // lista de INTEGERs
        };
        const settings = {
          method: "PUT",
          body: JSON.stringify(list_contrato_de_negocio),
          headers: {
            "Content-Type": "application/json",
            Authorization: this.localUser.userId,
          },
        };
        let endpoint = "http://localhost:5000/api/categories";
        await fetch(endpoint, settings);
      }

      if (!this.isEditedCategories() && !this.isEditedBook()) {
        alert("No se ha modificado ningún dato del libro");
      }

      let route = "/books/" + this.bookId;
      this.$router.push(route);
      //return response;
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Lora:ital@1&family=Raleway:wght@300&display=swap");
* {
  font-family: "Raleway", sans-serif;
}
.book-info-wrapper {
  display: flex;
  flex-direction: column;
  margin-bottom: 1.5em;
}
.titulo-categorias {
  font-weight: bold;
}
.book-info-wrapper div {
  margin: 0.5em;
}
.book-info-wrapper div input {
  margin-left: 1em;
}
.book-info-wrapper div label {
  font-weight: bold;
}
.categories-wrapper {
  display: inline-block;
  margin: 1em;
}
.category-checkbox {
  grid-template-columns: 1fr 1fr;
}
.category-name {
  grid-template-columns: 1fr 1fr 1fr;
}
.boton-guardar-cambios {
  font-weight: bold;
  padding: 0.2em;
}
</style>