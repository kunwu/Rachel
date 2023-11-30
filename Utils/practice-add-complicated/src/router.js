import { createRouter, createWebHistory } from 'vue-router'
import HomePage from './components/HomePage.vue'
import AddNumbers from './components/AddNumbers.vue'
import Multiply from './components/Multiply.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: HomePage,
        display: 'Home'
    },
    {
        path: '/add-numbers',
        name: 'AddNumbers',
        component: AddNumbers,
        display: '心算连加'
    },
    {
        path: '/multiply',
        name: 'Multiply',
        component: Multiply,
        display: '心算乘法'
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router