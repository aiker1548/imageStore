import { createRouter, createWebHistory } from 'vue-router';
import ImageGallery from '../components/ImageGallery.vue';
import UserLogin from '../components/UserLogin.vue';
import UserRegister from '../components/UserRegister.vue';
import { store } from '../store/store.js'; // Импортируйте store

const routes = [
  { path: '/login', component: UserLogin },
  { path: '/register', component: UserRegister },
  {
    path: '/',
    component: ImageGallery,
    meta: { requiresAuth: true } // Защищённый маршрут
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Глобальный навигационный охранник
router.beforeEach((to, from, next) => {
  const isAuthenticated = store.isAuthenticated; // Получаем статус аутентификации
  if (to.meta.requiresAuth && !isAuthenticated) {
    // Если маршрут требует авторизации, но пользователь не авторизован
    next('/login'); // Перенаправляем на страницу входа
  } else {
    next(); // Разрешаем переход
  }
});

export default router;
