import component from './components/vue-abchat.vue';


function install(Vue) {
  if (install.installed) return;
  install.installed = true;
  Vue.component('abchat', component);
}

const plugin = {
  install,
};

// Auto-install when vue is found (eg. in browser via <script> tag)
let GlobalVue = null;
if (typeof window !== 'undefined') {
  GlobalVue = window.Vue;
} else if (typeof global !== 'undefined') {
  GlobalVue = global.Vue;
}
if (GlobalVue) {
  GlobalVue.use(plugin);
}

component.install = install

// To allow use as module (npm/webpack/etc.) export component
export default component;