<template>
  <div>
    <h2>Авторизация</h2>
    <form @submit.prevent="loginUser">
      <input v-model="username" type="text" placeholder="Имя пользователя" required />
      <input v-model="password" type="password" placeholder="Пароль" required />
      <button type="submit">Войти</button>
    </form>
  </div>
</template>

<script>
import apiClient from '../apiClient.js';
import { store } from '../store/store.js';

export default {
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    async loginUser() {
      try {
        const response = await apiClient.post('/login/', {
          username: this.username,
          password: this.password
        });
        store.isAuthenticated = true;
        store.userId = response.data.userId;
        this.$router.push('/');
      } catch (error) {
        console.error(error);
        alert('Ошибка входа');
      }
    }
  }
};
</script>
