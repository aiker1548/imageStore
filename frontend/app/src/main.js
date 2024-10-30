import { createApp } from 'vue';
import App from './App.vue';
import router from './router/router.js';
import './assets/style.css'; // Импорт стилей

createApp(App)
  .use(router)
  .mount('#app');
