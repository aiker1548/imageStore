import { createApp } from 'vue';
import App from './App.vue';
import router from './router/router.js';
import { store } from './store/store.js';
import './assets/style.css'; // Импорт стилей

const app = createApp(App);
app.use(store);
app.use(router);
app.provide('store', store); // Передаем Store через provide
app.mount('#app');


