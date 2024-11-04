<template>
  <div>
    <h2>Регистрация</h2>
    <form @submit.prevent="registerUser">
      <input v-model="username" placeholder="Имя пользователя" required />
      <input v-model="password" type="password" placeholder="Пароль" required />
      <button type="submit">Зарегистрироваться</button>
    </form>
  </div>
</template>

<script>
import { store } from '../store/store.js';
import apiClient from '../apiClient.js';

export default {
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    async registerUser() {
      try {
        const response = await apiClient.post('/register/', {
          username: this.username,
          password: this.password
        });
        store.userId = response.data.userId;
        alert('Регистрация успешна!');
      } catch (error) {
        console.error(error);
        alert('Ошибка регистрации');
      }
    }
  }
};
</script>
