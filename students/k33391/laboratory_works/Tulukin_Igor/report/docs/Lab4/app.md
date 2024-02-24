# main.ts

**Листинг кода**:
``` ts title="main.ts"
// @ts-nocheck
import { createApp } from 'vue'
import "./index.css"
import App from './App.vue'
import router from "./router";
import {createPinia} from "pinia";
import piniaPluginPersistedState, {createPersistedState} from "pinia-plugin-persistedstate"
import '@mdi/font/css/materialdesignicons.css'
import VueAwesomePaginate from "vue-awesome-paginate";

// import the necessary css file
import "vue-awesome-paginate/dist/style.css";

const pinia = createPinia();
pinia.use(piniaPluginPersistedState)

createApp(App).use(VueAwesomePaginate).use(pinia).use(router).mount('#app')

```