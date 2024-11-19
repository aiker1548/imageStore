<template>
    <div class="chat-room">
      <h2>Chat with {{ recipientId }}</h2>
  
      <div class="messages">
        <div v-for="(msg, index) in messages" :key="index" class="message">
          <strong>{{ msg.sender }}:</strong> {{ msg.text }}
        </div>
      </div>
  
      <input
        v-model="message"
        type="text"
        placeholder="Type a message..."
        @keyup.enter="sendMessage"
      />
      <button @click="sendMessage">Send</button>
    </div>
  </template>
  
  <script>
  import { useRoute } from 'vue-router';
  import { useStore } from 'vuex';
  
  export default {
    data() {
      return {
        socket: null,
        messages: [],
        message: "",
        recipientId: "",
      };
    },
    setup() {
      const route = useRoute();
      const store = useStore();
      return { route, store };
    },
    created() {
      this.recipientId = this.route.params.userId;
      this.initWebSocket();
    },
    methods: {
      initWebSocket() {
        const userId = this.store.state.userId || "guest"; // Используем Store через Composition API
        this.socket = new WebSocket(`ws://localhost:8000/ws/chat/${userId}`);
  
        this.socket.onopen = () => {
          console.log("Connected to WebSocket");
          const initMessage = {
            user_id: userId,
            message: `User ${userId} has joined the chat.`,
          };
          this.socket.send(JSON.stringify(initMessage));
        };
  
        this.socket.onmessage = (event) => {
          const data = JSON.parse(event.data);
          this.messages.push({
            sender: data.sender || "Server",
            text: data.text || data.message,
          });
        };
  
        this.socket.onclose = () => {
          console.log("WebSocket connection closed");
        };
      },
      sendMessage() {
        if (this.message.trim() !== "") {
          const userId = this.store.state.userId || "guest";
          const messageData = {
            to: this.recipientId,
            sender: userId,
            message: this.message,
          };
          this.socket.send(JSON.stringify(messageData));
          this.messages.push({
            sender: userId,
            text: this.message,
          });
          this.message = "";
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .chat-room {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 10px;
  }
  
  .messages {
    max-height: 400px;
    overflow-y: auto;
    margin-bottom: 10px;
  }
  
  .message {
    margin: 5px 0;
  }
  </style>
  