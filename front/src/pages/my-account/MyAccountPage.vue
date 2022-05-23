<template>
  <h1>{{ localUser.user }}</h1>
  <h1>Página de usuario</h1>
  <section>
    <h3>Libros reservados</h3>
    <article v-for="loan in loans" :key="loan.loan_id">
      <h2>{{ loan.title }}</h2>
      <button @click="returnBook(loan.loan_id)">Devolver libro</button>
    </article>
    <router-link to="/books"><button>Reservar Otro</button></router-link>
  </section>
</template>

<script>
import { useStorage } from "@vueuse/core";
export default {
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

    async returnBook(id) {
      let today = new Date()
      today = today.toISOString().slice(0,10)

      let getLoan
      for (let book of this.loans){
        if (book.loan_id===id){
          getLoan=book
        }
      }

      let loanToReturn=Object.assign({},getLoan)
      delete loanToReturn.title
      delete loanToReturn.user
      loanToReturn['user_id']='no user needed'
      loanToReturn['final_date']=today
      //console.log('Loan original', getLoan)
      //console.log('Loan okCopy', loanToReturn)

      let endpoint = `http://localhost:5000/api/loans/${id}`;
      if (confirm("¿Está seguro que quiere devolver este maravilloso libro?")) {
        const settings = {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: this.localUser.userId 
            },
          body:JSON.stringify(loanToReturn)
        };
        let response = await fetch(endpoint, settings);
        this.loadData();
        return response;
      }
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
  border: 2px solid black;
  margin-top: 1em;
  margin-left: 3em;
  margin-right: 3em;
  padding: 1em;
  display: flex;
  justify-content: space-around;
}
</style>
