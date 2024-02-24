import {createRouter, createWebHistory} from "vue-router";
import Warriors from "@/components/Warriors.vue";

const routes = [
   {
   path: '/warriors',
   component: Warriors
}
]

const router = createRouter({
   history: createWebHistory(), routes
})

export default router