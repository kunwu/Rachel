<template>
    <div>
        <v-container>
            <v-row>
                <v-col>
                    <h1 class="text-h5">欢迎来到小吴双的智慧宝盒</h1>
                    <p class="text-body-1">一起来锻炼数字心算能力</p>
                </v-col>
            </v-row>
            <v-list>
                <v-list-item v-for="(route, index) in routes" :key="index">
                    <v-list-item-title>
                        <router-link :to="route.path">{{ route.meta.display }}</router-link>
                    </v-list-item-title>
                </v-list-item>
            </v-list>
        </v-container>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
const routes = router.options.routes.filter(route => route.path !== '/')
</script>
  