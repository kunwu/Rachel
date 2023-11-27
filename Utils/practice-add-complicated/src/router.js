import { createRouter, createWebHistory } from 'vue-router'
import AddNumbers from './components/AddNumbers.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: AddNumbers
    },
    {
        path: '/add-numbers',
        name: 'AddNumbers',
        component: AddNumbers
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router