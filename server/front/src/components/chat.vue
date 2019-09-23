<template>
  <div>
    <h1>Hi, this is ABChat!</h1>
    <div v-for="(message, idx) in message_list" :key="idx">
      <span>{{ message.data }}</span>
      <br />
    </div>
    <input type="text" ref="chat" v-model="my_message" @keyup.enter="getChatData" />
  </div>
</template>
<script>
import axios from "axios";

const BASE_URL = "http://13.125.17.8:5000";
let api = axios.create({
  baseURL: BASE_URL,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    withCredentials: false
  }
});

let get_result = async function(message) {
  let result = null;
  await api
    .request({
      method: "GET",
      url: `/${message}`,
      mode: "no-cors"
    })
    .then(res => {
      result = res;
    });
  return result;
};

export default {
  name: "ABChat",
  data() {
    return {
      message_list: [],
      my_message: "",
      your_message: "",
      raw_data: null
    };
  },
  methods: {
    async getChatData() {
      let my_message = {
        type: "user",
        data: this.my_message
      };
      await this.message_list.push(my_message);
      const res = await get_result(this.my_message);
      this.my_message = "";
      let ai_message = {
        type: "ai",
        data: res.data.result
      };
      await this.message_list.push(ai_message);
      this.$refs.chat.focus();
    }
  }
};
</script>
<style>
</style>