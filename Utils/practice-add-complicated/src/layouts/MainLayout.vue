<template>
    <v-app>
        <!-- Header -->
        <v-app-bar app color="primary" dark>
            <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
            <v-toolbar-title>小吴双的智慧宝盒</v-toolbar-title>
        </v-app-bar>

        <!-- Navigation Drawer -->
        <v-navigation-drawer v-model="drawer" app>
            <v-list dense>
                <v-list-item v-for="route in routes" :key="route.name" :to="route.path">
                    <v-list-item-title>{{ route.display }}</v-list-item-title>
                </v-list-item>
            </v-list>
        </v-navigation-drawer>

        <!-- Main content -->
        <v-main>
            <router-view></router-view>
        </v-main>

        <!-- Footer -->
        <v-footer app color="secondary" dark>
            <span>&copy; 2023</span>
        </v-footer>
    </v-app>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
    name: 'MainLayout',
    setup() {
        const drawer = ref(false);
        const router = useRouter();
        const routes = router.options.routes.map(route => ({
            name: route.name,
            path: route.path,
            display: route.display
        }));

        return { drawer, routes };
    },
};
</script>