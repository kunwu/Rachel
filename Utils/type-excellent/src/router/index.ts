import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import PracticePad from '../components/PracticePad.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: {
        showOnMenu: true,
        displayText: 'Home'
      }
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
      meta: {
        showOnMenu: false,
        displayText: '关于'
      }
    },
    {
      path: '/practice',
      name: 'practice',
      component: PracticePad,
      meta: {
        showOnMenu: true,
        displayText: '练习'
      }
    }
  ]
})

export default router
