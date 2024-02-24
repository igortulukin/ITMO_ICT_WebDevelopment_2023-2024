# router.ts

**Листинг кода**:
``` ts title="router.ts"
import {createRouter, createWebHistory} from 'vue-router'

const Main = () => import("../components/MainPage/Main.vue")
const StartProgram = () => import("../components/StartProgramPage/StartProgram.vue")
const EditProgram = () =>  import("../components/EditProgram/EditProgram.vue")
const EditingProgram = () =>  import("../components/EditProgram/EditingProgram.vue")
const EditConfiguration = () =>  import("../components/EditConfiguration/EditConfiguration.vue")
const EditingConfiguration = () =>  import("../components/EditConfiguration/EditingConfiguration.vue")
const EditReagent = () =>  import("../components/EditReagent/EditReagent.vue")
const Settings = () =>  import("../components/Settings.vue")
const Test = () => import("../components/Test/TestPage.vue")
const Statistics = () => import("../components/Statistic/Statistics.vue");
const UsageStatistics = () => import("../components/Statistic/UsageStatistics.vue")
const EventStatistics = () => import("../components/Statistic/EventStatistics.vue")
const EditUser = () =>  import("../components/EditUser/EditUser.vue")
const EditingUser = () => import("../components/EditUser/EditingUser.vue")
const NewUser = () =>  import("../components/EditUser/NewUser.vue")
const Pause = () =>  import("../components/PausePage/Pause.vue")
const TakeCart = () =>  import("../components/TakeCart.vue")

const Stages = () =>  import("../components/Stages.vue")
import {UserStore} from "../store/UserStore"
import LogIn from "../components/LoginPage/LogIn.vue";
import {AppStore} from "../store/AppStore.ts";

const routes = [
    {
        path: '/login',
        name: 'login',
        component: LogIn,
        alias: ['/']
    },
    {path: '/process', name: 'process', component: Main},
    {path: '/start-program', name: 'start Program', component: StartProgram},
    {path: '/edit-program', name:'editProgram', component: EditProgram},
    {path: '/editing-program/:id', name:'editingProgram', component: EditingProgram, props: true},
    {path: '/edit-configuration', name:'editConfiguration', component: EditConfiguration},
    {path: '/editing-configuration/:id', name:'newConfiguration', component: EditingConfiguration, props: true},
    {path: '/edit-reagent', name:'editReagent', component: EditReagent},
    {path: '/settings', name:'settings', component: Settings},
    {path: '/test', name:'test', component: Test},
    {path: '/statistics', name:'statistics', component: Statistics},
    {path: '/usage-statistics', name:'usageStatistics', component: UsageStatistics},
    {path: '/event-statistics', name:'eventStatistics', component: EventStatistics},
    {path: '/edit-user', name:'editUser', component: EditUser},
    {path: '/editing-user', name:'editingUser', component: EditingUser},
    {path: '/new-user', name:'newUser', component: NewUser},
    {path: '/pause', name:'newUser', component: Pause},
    {path: '/take-cart', name:'takeCart', component: TakeCart},
    {path: '/stages', name:'stages', component: Stages}

]

const router = createRouter({
    history: createWebHistory(),
    routes
})
router.beforeEach((to) => {
    // redirect to login page if not logged in and trying to access a restricted page
    const user = UserStore();
    const program = AppStore();
    program.loading = true;
    const publicPages = ['/login'];
    const authRequired = !publicPages.includes(to.path);
    const loggedIn = user.getToken();
    if (authRequired && !loggedIn) {
        return {name: 'login'}
    }

    if (user.getUser() !== 'SERVICE' && to.path === '/test') {
        return {name: 'test'}
    }
    return
})

router.afterEach(() => {
    const program = AppStore();
    program.loading = false;
})

export default router

```