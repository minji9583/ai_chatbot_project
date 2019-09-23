import chat from './components/chat.vue'

const install = (Vue) => {
  Vue.component(chat.name, chat)
}

// auto install if used in browser
if (typeof window !== 'undefined' && window.Vue) {
  install(window.Vue)
}

export {
  chat
}

export default install