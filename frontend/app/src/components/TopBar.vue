<template>
<div class="top-bar">
    <button @click="logout">Выйти</button>
    <button @click="goToChats">Чаты</button>
</div>
</template>

<script>
import { store } from '../store/store.js';

export default {
    computed: {
    isAuthenticated() {
        return store.isAuthenticated;
    }
},
methods: {
    logout() {
    store.isAuthenticated = false;
    store.userId = -1;
    this.$router.push('/login');
    console.log('Вы вышли из системы');
    },
    goToChats() {
    this.$router.push('/chats');
    console.log('Переход к чатам');
    }
}
}
</script>

<style scoped>
.top-bar {
display: flex;
justify-content: space-between;
padding: 10px;
background-color: #f8f9fa;
}
button {
cursor: pointer;
}
</style>