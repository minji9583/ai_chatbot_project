<template>
  <div>
    <div class="hidebtn" v-show="!hideflag" @click="hideflag = !hideflag">
      <span>{{ button_title }}</span>
    </div>
    <div id="complayout" v-show="hideflag">
      <div class="headerlayout">
        <div style="flex-basis: 30%;"></div>
        <span class="header" style="flex-basis: 30%;">{{ title }}</span>
        <div style="flex-basis: 30%;" class="btns">
          <div class="btn" @click="message_list=[]">C</div>
          <div class="btn" @click="hideflag = !hideflag">
            <div class="hidebtn2"></div>
          </div>
        </div>
      </div>
      <div class="chatlayout">
        <div v-for="(message, idx) in message_list" :key="idx">
          <div class="arrow_box box_font" v-if="message.type==='user'">
            <span>{{ message.data }}</span>
          </div>
          <div class="arrow_box2 box_font" v-else>
            <span v-if="message.loadflag" class="loader"></span>
            <span v-else>{{ message.data }}</span>
          </div>
        </div>
      </div>
      <div class="inputlayout">
        <input
          type="text"
          ref="chat"
          class="inputbox"
          v-model="my_message"
          @keyup.enter="getChatData"
        />
        <button class="abutton" @click="getChatData">send</button>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";

export default {
  name: "vue-abchat",
  props: {
    base_url: {
      type: String,
      required: true
    },
    width: {
      type: Number,
      default: 300
    },
    height: {
      type: Number,
      default: 400
    },
    position: {
      type: String,
      default: "bottom-right"
    },
    title: {
      type: String,
      default: "ABChat"
    },
    button_title: {
      type: String,
      default: "chat"
    },
    colors: {
      type: Object
    }
  },
  data() {
    return {
      message_list: [],
      my_message: "",
      your_message: "",
      raw_data: null,
      hideflag: true,
      api: axios.create({
        baseURL: this.base_url,
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          withCredentials: false
        }
      }),
      loadflag: false,
      loadidx: null
    };
  },
  methods: {
    async get_result(message) {
      let result = null;
      await this.api
        .request({
          method: "GET",
          url: `/${message}`,
          mode: "no-cors"
        })
        .then(res => {
          result = res;
        })
        .catch(function(error) {
          result = error;
        });
      return result;
    },
    async getChatData() {
      if (this.my_message == "") {
        return;
      }
      if (this.loadflag) {
        return;
      }
      document.getElementsByClassName("abutton")[0].textContent = await 'wait'
      await document.getElementsByClassName("abutton")[0].classList.add("bbutton");
      await document.getElementsByClassName("abutton")[0].classList.remove("abutton");
      this.loadflag = true;
      this.loadidx = this.message_list.length;
      let my_message = {
        type: "user",
        data: this.my_message.replace(/[\\/]/g, ""),
        idx: this.loadidx
      };
      this.my_message = "";
      await this.message_list.push(my_message);
      let height = document.getElementsByClassName("chatlayout")[0]
        .scrollHeight;

      await document
        .getElementsByClassName("chatlayout")[0]
        .scrollTo(0, height);

      await this.message_list.push({
        type: "ai",
        data: "loading",
        loadflag: true,
        idx: this.loadidx + 1
      });

      await document
        .getElementsByClassName("chatlayout")[0]
        .scrollTo(0, height);

      let ai_message = {};
      const res = await this.get_result(my_message.data);
      if (res.status == 200) {
        ai_message = {
          type: "ai",
          data: res.data.result,
          loadflag: false,

          idx: this.loadidx + 1
        };
      } else {
        ai_message = {
          type: "ai",
          data: "서버가 이상해요",
          loadflag: false,
          idx: this.loadidx + 1
        };
      }

      this.message_list.splice(this.loadidx + 1, 1, ai_message);
      document.getElementsByClassName("bbutton")[0].textContent = await 'send'
      document.getElementsByClassName("bbutton")[0].classList.add("abutton");
      document.getElementsByClassName("bbutton")[0].classList.remove("bbutton");
      this.loadflag = false;

      height = await document.getElementsByClassName("chatlayout")[0]
        .scrollHeight;
      await document
        .getElementsByClassName("chatlayout")[0]
        .scrollTo(0, height);

      this.$refs.chat.focus();
    },
    setCompSize() {
      document.getElementById("complayout").style.height =
        this.height.toString() + "px";
      document.getElementById("complayout").style.width =
        this.width.toString() + "px";
    }
  },
  mounted() {
    this.setCompSize();
  }
};
</script>
<style scoped>
.btns {
  display: flex;
  justify-content: flex-end;
  color: white;
  font-weight: 500;
}

.hidebtn2 {
  width: 14px;
  height: 2px;
  background-color: #fff;
}

.btn {
  width: 22px;
  height: 22px;
  border: 1.5px rgba(255, 255, 255, 0.699) solid;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 30%;
  background-color: rgba(255, 255, 255, 0.13);
  margin-right: 3px;
}
.btn:hover {
  cursor: pointer;
  background-color: rgba(255, 255, 255, 0.603);
}

.hidebtn {
  position: fixed;
  bottom: 15px;
  right: 15px;
  padding: 0.1em 0.3em;
  width: 40px;
  height: 40px;
  background-color: rgb(240, 61, 37);
  border-radius: 17px;
  color: white;
  font-size: 1.5em;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 1px 1px 3px 1px rgba(0, 0, 0, 0.788);
}

[top] .hidebtn {
  top: 15px;
}
[bottom] .hidebtn {
  bottom: 15px;
}
[right] .hidebtn {
  right: 15px;
}
[left] .hidebtn {
  left: 15px;
}

.hidebtn:hover {
  cursor: pointer;
  background-color: rgb(233, 123, 33);
}

#complayout {
  position: fixed;
  bottom: 30px;
  right: 30px;
  display: flex;
  justify-content: center;
  flex-direction: column;
  border-radius: 10px;
  box-shadow: 1px 1px 8px 1px rgba(0, 0, 0, 0.788);
}

[top] #complayout {
  top: 30px;
}
[bottom] #complayout {
  bottom: 30px;
}
[right] #complayout {
  right: 30px;
}
[left] #complayout {
  left: 30px;
}

.headerlayout {
  text-align: center;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  background-color: rgb(51, 78, 121);
  padding: 5px 15px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.header {
  color: white;
  font-size: 1.2em;
  font-weight: 700;
}

.chatlayout::-webkit-scrollbar {
  display: none;
}
.chatlayout {
  -ms-overflow-style: none;
  height: 100%;
  overflow: auto;
  padding-right: 1.2em;
  padding-left: 1.2em;
  background-color: rgb(163, 171, 197);
  border-left: 2px rgba(31, 31, 31, 0.26) solid;
  border-right: 2px rgba(31, 31, 31, 0.26) solid;
}
.inputlayout {
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
  padding: 0.5em 0.5em;
  background-color: rgb(51, 78, 121);
  display: flex;
  justify-content: center;
  align-items: center;
}

.inputbox {
  font-size: 1em;
  border: 0px;
  width: 100%;
  height: 100%;
  border-radius: 7px;
  padding: 3px;
  margin-right: 0.5em;
  box-sizing: border-box;
}

.abutton {
  width: 65px;
  padding: 0.5em 0.5em;
  background: rgb(202, 207, 226);
  color: rgb(80, 77, 77);
  font-size: 1em;
  font-weight: 700;
  border: 0px white;
  border-radius: 0.5em;
}
.bbutton {
  width: 65px;
  padding: 0.5em 0.5em;
  background: rgb(233, 96, 78);
  color: rgb(255, 255, 255);
  font-size: 1em;
  font-weight: 700;
  border: 0px white;
  border-radius: 0.5em;
}

.box_font {
  font-weight: 500;
}

.arrow_box {
  padding: 1px 10px;
  position: relative;
  background: #feffe9;
  border: 1px solid #f5f5f5;
  min-height: 30px;
  border-radius: 7px;
  word-break: break-all;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin: 0.5em 0;
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
  border-left-color: #feffe9;
  top: 15px;
  border-radius: 5px;
  border-width: 3px;
  margin-top: -3px;
}
.arrow_box:before {
  border-color: rgba(245, 245, 245, 0);
  border-left-color: #f5f5f5;
  top: 15px;
  border-radius: 5px;
  border-width: 7px;
  margin-top: -7px;
}

.arrow_box2 {
  padding: 1px 10px;
  position: relative;
  background: #dfefff;
  border: 1px solid #f5f5f5;
  min-height: 30px;
  border-radius: 7px;
  word-break: break-all;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  margin: 0.5em 0;
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
  border-right-color: #dfefff;
  top: 15px;
  border-width: 3px;
  margin-top: -3px;
}
.arrow_box2:before {
  border-color: rgba(245, 245, 245, 0);
  border-right-color: #f5f5f5;
  top: 15px;
  border-width: 7px;
  margin-top: -7px;
}
.loader,
.loader:before,
.loader:after {
  border-radius: 50%;
  width: 0.9em;
  height: 0.9em;
  -webkit-animation-fill-mode: both;
  animation-fill-mode: both;
  -webkit-animation: load7 1.8s infinite ease-in-out;
  animation: load7 1.8s infinite ease-in-out;
}
.loader {
  color: #5684c9;
  font-size: 1px;
  margin: 5px auto;
  margin-bottom: 45px;
  position: relative;
  text-indent: -9999em;
  -webkit-transform: translateZ(0);
  -ms-transform: translateZ(0);
  transform: translateZ(0);
  -webkit-animation-delay: -0.16s;
  animation-delay: -0.16s;
}
.loader:before,
.loader:after {
  content: "";
  position: absolute;
  top: 0;
}
.loader:before {
  left: -3em;
  -webkit-animation-delay: -0.32s;
  animation-delay: -0.32s;
}
.loader:after {
  left: 3em;
}
@-webkit-keyframes load7 {
  0%,
  80%,
  100% {
    box-shadow: 0 2.5em 0 -1.3em;
  }
  40% {
    box-shadow: 0 2.5em 0 0;
  }
}
@keyframes load7 {
  0%,
  80%,
  100% {
    box-shadow: 0 2.5em 0 -1.3em;
  }
  40% {
    box-shadow: 0 2.5em 0 0;
  }
}
</style>