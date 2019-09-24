<template>
  <div>
    <h1>abchat</h1>
    <div class="chatbox">
      <div v-for="(message, idx) in message_list" :key="idx">
        <div class="arrow_box" v-if="message.type==='user'">
          <span>{{ message.data }}</span>
        </div>
        <div class="arrow_box2" v-else>
          <span>{{ message.data }}</span>
        </div>
      </div>

      <input
        type="text"
        ref="chat"
        class="inputbox"
        v-model="my_message"
        @keyup.enter="getChatData"
      />
    </div>
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
  name: "vue-abchat",
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
<style scoped>
.chatbox {
  margin: 3px;
  padding: 20px;
  background-color: rgb(216, 216, 216);
}

.inputbox {
  width: 100%;
  height: 30px;
  border-radius: 5px;
  border: 3px white;
  margin: 10px;
}
.arrow_box {
  padding: 10px;
  position: relative;
  background: #f0f0f0;
  border: 2px solid #f5f5f5;
  min-height: 30px;
  margin: 10px;
  border-radius: 7px;
  text-align: right;
}
.arrow_box:after,
.arrow_box:before {
  left: 100%;
  top: 50%;
  border: solid transparent;
  content: " ";
  height: 0;
  width: 0;
  position: absolute;
  pointer-events: none;
}

.arrow_box:after {
  border-color: rgba(232, 232, 232, 0);
  border-left-color: #f0f0f0;
  top: 15px;
  border-radius: 5px;
  border-width: 7px;
  margin-top: -7px;
}
.arrow_box:before {
  border-color: rgba(245, 245, 245, 0);
  border-left-color: #f5f5f5;
  top: 15px;
  border-radius: 5px;
  border-width: 10px;
  margin-top: -10px;
}

.arrow_box2 {
  position: relative;
  background: #f0f0f0;
  border: 2px solid #f5f5f5;
  min-height: 30px;
  margin: 10px;
  border-radius: 7px;
}
.arrow_box2:after,
.arrow_box2:before {
  right: 100%;
  top: 50%;
  border: solid transparent;
  content: " ";
  height: 0;
  width: 0;
  position: absolute;
  pointer-events: none;
}

.arrow_box2:after {
  border-color: rgba(232, 232, 232, 0);
  border-right-color: #f0f0f0;
  top: 15px;

  border-width: 7px;
  margin-top: -7px;
}
.arrow_box2:before {
  border-color: rgba(245, 245, 245, 0);
  border-right-color: #f5f5f5;
  top: 15px;

  border-width: 10px;
  margin-top: -10px;
}
</style>