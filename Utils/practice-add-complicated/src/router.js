import Vue from 'vue'
import VueRouter from 'vue-router'

import AddNumbersVue from './components/AddNumbers.vue';

Vue.use(VueRouter);

const routes = [
    {
        path: '/',
        name: 'Home',
        component: AddNumbersVue,
    },
    {
        path: '/add-numbers',
        name: 'AddNumbers',
        component: AddNumbersVue,
    },
];

const router = new VueRouter({
    routes,
    mode: 'history',
});

export default router;