## SPRINT #2

## Pagina selección de usuario(cambiar la pagina home)

endpoint para recibir usuarios: "/api/users" metodo: GET

el endpoit deberia devolver un json con la lista de usuarios:
[{
user_id: user_1,
user: usuario,
is_librarian: true
},
{
user_id: user_2,
user: usuario,
is_librarian: false
},
{
user_id: user_3,
user: usuario,
is_librarian: false
}]

## Pagina userDashboard

Ruta de la pantalla: /user/dashboard
src/pages/user-dashboard/UserDashboardPage.vue

## boton reservar

envia un post con el libro a reservar:
POST /api/loans
Body: {
id: book-id,
title: 'titulo',
publisher: 'editorial',
ean: numero_EAN
}
response: 200 OK

este endpoint deba ñadir el book id a la tabla de loans junto con el user ID que deberia recibirse por meido del dato persistente [APRENDER]

la pagina con este boton devbe hacer un get a api/loans/<id> para saber si esta el libro reservado.

## Pagina userLoans

Ruta de la pantalla: /user/loans
src/pages/user-loans/UserLoansPage.vue

endpoint para recibir reservas: "/api/loans" metodo: GET con autentificacion de usuario [APRENDER]

el endpoint deberia devolver un json con la lista de los libros reservados por el usuario

json = [
{
loan_id: loan_1,
book_id: book_3,
title: pilares
},
{
loan_id: loan_2,
book_id: book_2,
title: hobbit
}]
¡¡este json tiene que extraer datos de diferentes tablas!!
enpoint para devolver un libro: "/api/loans/<id>" metodo: DELETE para eliminar de la tabla loans el libro. ¡SOLO DE LA DE LOANS!

## pagina librarianDashboard

Ruta de la pantalla: /librarian/dashboard
src/pages/librarian-dashboard/LibrarianDashboardPage.vue

## pagina lista de reservas para bibliotecartia

Ruta de la pantalla: /librarian/loans
src/pages/librarian-loans/LibrarianLoansPage.vue

endpoint para recibir reservas: "/api/loans" metodo: GET con autentificacion de bibliotecaria [APRENDER]

el endpoint deberia devolver un json con la lista de los libros reservados por los usuarios

json = [
{
loan_id: loan_1,
book_id: book_3,
title: pilares,
user: usuario_2
},
{
loan_id: loan_1,
book_id: book_3,
title: pilares,
user: usuario_3
}]

¡¡este json tiene que extraer datos de diferentes tablas!!

