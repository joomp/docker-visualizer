import { createApp } from 'vue';
import App from './App.vue';
import store from './store';
import 'bootstrap-icons/font/bootstrap-icons.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';
import { tooltip } from './directives/tooltip';
import VNetworkGraph from 'v-network-graph';
import 'v-network-graph/lib/style.css';

createApp(App)
  .use(store)
  .directive('tooltip', tooltip)
  .use(VNetworkGraph)
  .mount('#app');
