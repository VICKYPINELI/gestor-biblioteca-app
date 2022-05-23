<template>
  <h1>Detalles del libro</h1>
  <article>
    <img src="@/assets/img/logoliburu.png" alt="Libro" />
    <h2>{{ book.title }}</h2>
    <p>Autor : {{ book.author }}</p>
    <p>Editorial: {{ book.publisher }}</p>
    <p>EAN : {{ book.ean }}</p>
    <p>Categorias:</p>
    <h4 v-for="category in book.categories" :key="category">
      {{ category }}
    </h4>
  </article>

    <button class="delete" @click="deleteBook" v-if="localUser.isLibrarian">
    Eliminar
  </button>

  <button
    class="edit"
    @click="$router.push(`/books/edit/${book.id}`)"
    v-if="localUser.isLibrarian"
  >
    Editar libro
  </button>
  <p v-else>[No existen permisos para editar]</p>
  <button class="reserve" @click="reserveBook" v-if="!isReserved">
    Reservar libro
  </button>
  <div v-else>
     <p >[RESERVADO]</p>
      <button class="returnbook" @click="returnBookToLibrary" >
    Devolver
  </button>
  </div>
 

 
 

  <!-- <pre> Datos de los prestamos extraidos en back:
    {{ dataLoansList }}
  </pre>  -->

</template>

<script>
import { useStorage } from "@vueuse/core";
import { v4 as uuidv4 } from "uuid";

export default {
  name: "BookDetail",
  data() {
    return {
      book: {},
      bookId: this.$route.params.id,
      localUser: useStorage("user", {}),
      isReserved: undefined,
      loan: {},
      dataLoansList: []
    
    };
  },

  mounted() {
    this.loadData();
    this.fetchReserve();
  },

  methods: {
    async loadData() {
      //Extrayendo datos del libro
      let endpoint = "http://localhost:5000/api/books/" + this.bookId;
      let response = await fetch(endpoint);
      this.book = await response.json();

      //Extrayendo la lista total de loans
      let settings = { headers: { 'Authorization': this.localUser.userId } };
      let endpointLoans = "http://localhost:5000/api/loans"
      let responseLoans = await fetch(endpointLoans, settings);
      this.dataLoansList = await responseLoans.json();
    
      // Extrayendo los datos  del loan concreto del book_id
      this.extractLoanDatafromList();
      // Extrayendo los datos  del loan concreto del book_id


    },
    extractLoanDatafromList(){
      for(let oneLoan of this.dataLoansList){
        
         if(oneLoan.book_id == this.bookId){
          this.loan = oneLoan
          console.log("this loan " + this.loan.initial_date)
          console.log("this loan final date " + this.loan.final_date)
          console.log("this loan " + this.loan.loan_id)
    
        }
      }
    },

    async returnBookToLibrary() {
      console.log("localuser " + this.localUser.user )

      let today = new Date()
      today = today.toISOString().slice(0,10)
      console.log("fecha hoy : " +    today)
       
      let body_loan = {"loan_id": this.loan.loan_id,
            "book_id": this.bookId,
            "user_id": this.loan.user_id,
            "initial_date":this.loan.initial_date,
            "final_date":today}
      
      console.log(body_loan)
      let endpoint = "http://localhost:5000/api/loans/" + this.loan.loan_id;
      if (confirm("¿Está seguro que quiere devolver este libro?")) {
        const settings = {
          method: "PUT",
          body: JSON.stringify(body_loan),
          headers: {
            "Content-Type": "application/json",
            Authorization: this.localUser.userId,
          },
        };

        let response = await fetch(endpoint, settings);
        this.$router.push(`/books`);
        return response;
      }
    },

    async reserveBook() {

      let todayToProcess= new Date().toISOString();
      let today= todayToProcess.slice(0,10);
      let loanId = uuidv4();
      let endpoint = "http://localhost:5000/api/loans";
      if (confirm("¿Está seguro que quiere reservar este libro?")) {
        let loan = {
          loan_id: loanId,
          book_id: this.bookId,
          user_id: this.localUser.userId,
          initial_date: today
        };
        const settings = {
          method: "POST",
          body: JSON.stringify(loan),
          headers: {
            "Content-Type": "application/json",
            Authorization: this.localUser.userId,
          },
        };

        let response = await fetch(endpoint, settings);
        this.$router.push(`/user/my-account`);
        console.log(response);
        return response;
      }
    },
    async fetchReserve() {
      const settings = {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: this.localUser.userId,
        },
      };
      let endpoint = "http://localhost:5000/api/loans/" + this.loan.loan_id;
      let response = await fetch(endpoint, settings);

      if (response.status == 200) {
         this.isReserved = true;
      }
       if (response.status == 404) {
         this.isReserved = false;
      }
    },
    async deleteBook() {
      let endpoint = "http://localhost:5000/api/books/";
      endpoint += this.bookId;
      if (confirm("¿Está seguro que quiere eliminar este libro?")) {
        const settings = {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            Authorization: this.localUser.userId,
          },
        };

        let response = await fetch(endpoint, settings);
        this.$router.push(`/books`);
        return response;
      }
    }

  },
};
</script>


<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Lora:ital@1&family=Raleway:wght@300&display=swap");
* {
  font-family: "Raleway", sans-serif;
}
h1 {
  font-weight: bold;
}
p {
  font-weight: 400;
}
article {
  margin: 2em;
  padding: 1em;
  border: 4px solid rgba(107, 110, 107, 0.425);
  background-color: rgba(153, 151, 149, 0.301);
  border-radius: 1em;
}
img {
  height: 80px;
}
.edit {
  margin-left: 2em;
}
button {
  font-weight: bold;
  margin: 1em;
  padding: 0 0.2em;
}
</style>
