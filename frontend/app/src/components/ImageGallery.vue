<template>
  <div>
    <h2>Галерея изображений</h2>
  <div class="top-bar">
    <button @click="logout">Выйти</button>
    <button @click="goToChats">Чаты</button>
</div>
    <div class="gallery-container">
      <div v-for="image in images" :key="image.id" class="image-item">
        <img :src="getImagePath(image.path)" alt="Image" />
        <p>Загрузил: {{ image.username }}</p>
        <button @click="downloadImage(image.id)">Скачать</button>
      </div>
    </div>

    <h3>Загрузить изображение</h3>
    <label class="file-upload-label">
      Выберите файл
      <input type="file" @change="handleFileUpload" />
    </label>
    <button @click="uploadImage" :disabled="!selectedFile">Загрузить</button>
  </div>
</template>

<script>
import apiClient from '../apiClient.js';
import defaultPhoto from '../assets/defaultPhoto.jpg'; // Импорт изображения по умолчанию
import { store } from '../store/store.js';

export default {
  data() {
    return {
      images: [],
      selectedFile: null,
    };
  },
  created() {
    this.fetchImages();
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
    },
    async fetchImages() {
      try {
        const response = await apiClient.get('/images/');
        this.images = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    getImagePath(path) {
      // Разрешенные расширения
      const allowedExtensions = ['jpg', 'jpeg', 'png'];
      const fileExtension = path ? path.split('.').pop().toLowerCase() : '';

      // Проверка расширения файла, если оно разрешено
      if (!allowedExtensions.includes(fileExtension)) {
        return path;
      }
      
      // Если расширение не разрешено, возвращаем изображение по умолчанию
      return defaultPhoto;
    },
    async downloadImage(image_id) {
      try {
        const response = await apiClient.get(`/download/${image_id}`, { responseType: 'blob' });
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `image_${image_id}.jpg`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } catch (error) {
        console.error(error);
        alert("Ошибка скачивания изображения");
      }
    },
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
    },
    async uploadImage() {
      const formData = new FormData();
      formData.append('file', this.selectedFile);
      formData.append('user_id', this.userId || 1);



      try {
        await apiClient.post('/upload/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        alert('Изображение успешно загружено!');
        this.selectedFile = null;
        this.fetchImages();
      } catch (error) {
        console.error(error);
        alert("Ошибка загрузки изображения");
      }
    },
  },
};
</script>

<style>
.file-upload-label {
    display: inline-block;
    padding: 10px 20px;
    background-color: #5cb85c;
    color: white;
    border: none;
    border-radius: 5px;
    text-align: center;
    cursor: pointer;
    margin: 10px 0;
}

.file-upload-label:hover {
    background-color: #4cae4c;
}


</style>
