import { createRouter, createWebHistory } from 'vue-router';
import Instructions from '../views/Instructions.vue';
import Home from '../views/Home.vue';
import Application from '../views/Application.vue';
// import Status from '../views/Status.vue';
import Dashboard from '../views/Dashboard.vue';
import Success from '../views/Success.vue';
import NotFound from '../views/NotFound.vue'

const routes = [
    { path: '/', name: 'Instructions', component: Instructions },
    { path: '/voucher', name: 'Home', component: Home },
    { path: '/apply', name: 'Application', component: Application },
    // { path: '/status', name: 'Status', component: Status },
    { path: '/dashboard', name: 'Dashboard', component: Dashboard },
    { path: '/success', name: 'Success', component: Success },
    { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
