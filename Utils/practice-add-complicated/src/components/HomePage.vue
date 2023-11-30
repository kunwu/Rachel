<template>
    <div>
        <ul class="mx-10 my-5">
            <li class="my-3 text-h5" v-for="(route, index) in routes" :key="index">
                <router-link :to="route.path">{{ route.display }}</router-link>
            </li>
        </ul>
    </div>
</template>
  
<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
const routes = router.options.routes
</script>
  