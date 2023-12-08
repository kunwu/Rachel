<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>小吴双的风暴打字机</v-toolbar-title>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" app>
      <v-list>
        <v-list-group>
          <v-list-item v-for="route in menuRoutes" :key="route.name" link :to="route.path">
            <v-list-item-title>{{ route.meta.displayText }}</v-list-item-title>
          </v-list-item>
        </v-list-group>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <router-view />
    </v-main>

    <v-footer app color="secondary" dark>
      <v-col class="text-center" cols="12">
        <span>&copy; 2023 吴双</span>
      </v-col>
    </v-footer>
  </v-app>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default defineComponent({
  name: 'App',
  setup() {
    const drawer = ref(false)
    const router = useRouter()
    const route = useRoute()

    const menuRoutes = computed(() => router.getRoutes().filter(r => r.meta && r.meta.showOnMenu))
    const currentRoute = computed(() => route.path)

    return {
      drawer,
      menuRoutes,
      currentRoute
    }
  }
})
</script>