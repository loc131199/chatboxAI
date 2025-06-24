<template>
  <div class="chat-container">
    <div class="logo">
      <img src="/images.png" alt="Logo Bách Khoa" />
      <span><strong>Đại học Bách Khoa</strong></span>
    </div>
    <h1>Hôm nay bạn có thắc mắc gì về chương trình đào tạo ?</h1>

    <div class="chatbox" ref="chatbox">
      <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.sender]">
        {{ msg.text }}
      </div>
    </div>

    <div class="input-area">
      <input
        type="text"
        v-model="userInput"
        @keydown.enter="sendMessage"
        placeholder="Bạn có thắc mắc gì về chương trình đào tạo của trường Đại học Bách Khoa?"
      />
      <button @click="sendMessage">Gửi</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userInput: "",
      messages: []
    };
  },
  methods: {
    async sendMessage() {
      const text = this.userInput.trim();
      if (!text) return;
      this.messages.push({ text, sender: "user" });
      this.userInput = "";

      try {
        const res = await fetch("http://localhost:8000/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: text })
        });
        const data = await res.json();
        this.messages.push({ text: data.reply, sender: "bot" });

        this.$nextTick(() => {
          this.$refs.chatbox.scrollTop = this.$refs.chatbox.scrollHeight;
        });
      } catch (e) {
        this.messages.push({ text: "Lỗi kết nối đến máy chủ!", sender: "bot" });
      }
    }
  }
};
</script>

<style scoped>
@import "@/assets/style.css";
</style>
