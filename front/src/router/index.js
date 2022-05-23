import { createRouter, createWebHistory } from "vue-router";
import Home from "../pages/home/HomePage.vue";
import About from "../pages/about/AboutPage.vue";
import Books from "../pages/bookslist/BooksListPage.vue";
import BookDetail from "../pages/bookdetail/BookDetailPage.vue";
import AddBookPage from "../pages/add_book/AddBookPage.vue";
import EditBookPage from "../pages/edit_book/EditBookPage.vue";
import MyAccount from "../pages/my-account/MyAccountPage.vue";
import LibrarianDashboard from "../pages/librarian_dashboard/LibrarianDashboardPage.vue";
import LibrarianLoans from "../pages/librarian-loans/LibrarianLoansPage.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/about",
    name: "About",
    component: About,
  },
  {
    path: "/books",
    name: "Books",
    component: Books,
  },
  {
    path: "/books/:id",
    name: "BookDetail",
    component: BookDetail,
  },
  {
    path: "/books/add",
    name: "AddBookPage",
    component: AddBookPage,
  },
  {
    path: "/books/edit/:id",
    name: "EditBookPage",
    component: EditBookPage,
  },
  {
    path: "/user/my-account",
    name: "MyAccount",
    component: MyAccount,
  },
  {
    path: "/librarian/dashboard",
    name: "LibrarianDashboard",
    component: LibrarianDashboard,
  },
  {
    path: "/librarian/loans",
    name: "LibrarianLoans",
    component: LibrarianLoans,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
