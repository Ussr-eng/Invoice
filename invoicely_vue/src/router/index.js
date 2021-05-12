import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import  Dashboard from '../views/dashboard/Dashboard.vue'
import  MainPage from '../views/dashboard/MainPage.vue'
import MyAccount from '../views/dashboard/MyAccount.vue'
import SignUp from '../views/SignUp.vue'
import LogIn from '../views/Login.vue'
import Clients from '../views/dashboard/Clients.vue'
import Client from '../views/dashboard/Client.vue'
import EditClient from '../views/dashboard/EditClient.vue'
import EditTeam from '../views/dashboard/EditTeam.vue'
import EditProductProvider from '../views/dashboard/EditProductProvider.vue'
import AddClient from '../views/dashboard/AddClient.vue'
import Invoices from '../views/dashboard/Invoices.vue'
import Invoice from '../views/dashboard/Invoice.vue'
import AddInvoice from '../views/dashboard/AddInvoice.vue'
import AddProvider from '../views/dashboard/AddProvider.vue'
import AddProduct from '../views/dashboard/AddProduct.vue'
import AllProviders from '../views/dashboard/AllProviders.vue'
import Provider from '../views/dashboard/Provider.vue'
import AddOrder from '../views/dashboard/AddOrder.vue'
import AllOrders from '../views/dashboard/AllOrders.vue'
import Order from '../views/dashboard/Order.vue'
import store from '../store'


const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/sign-up',
    name: 'SignUp',
    component: SignUp
  },
  {
    path: '/log-in',
    name: 'LogIn',
    component: LogIn
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta:{
        requireLogin: true
    }
  },
  {
    path: '/main_page',
    name: 'MainPage',
    component: MainPage,
    meta:{
        requireLogin: true
    }
  },
  {
    path: '/dashboard/orders',
    name: 'AllOrders',
    component: AllOrders,
    meta:{
        requireLogin: true
    }
  },
  {
    path: '/dashboard/orders/:id',
    name: 'Order',
    component: Order,
    meta:{
        requireLogin: true
    }
  },
  {
    path: '/home/provider/addproduct/:id',
    name: 'AddProduct',
    component: AddProduct,
    meta:{
        requireLogin: true
    }
  },
  {
    path: '/dashboard/invoices',
    name: 'Invoices',
    component: Invoices,
    meta:{
        requireLogin: true
    }
  },
  {
    path: '/dashboard/add_order',
    name: 'AddOrder',
    component: AddOrder,
    meta:{
        requireLogin: true
    }
  },
  {
    path: '/dashboard/all_providers',
    name: 'AllProviders',
    component: AllProviders,
    meta:{
        requireLogin: true
    }
  },
  {
    path: '/dashboard/provider/:id',
    name: 'Provider',
    component: Provider,
    meta:{
        requireLogin: true
    }
  },
  {
    path: '/home/provider/editproduct/:id',
    name: 'EditProductProvider',
    component: EditProductProvider,
    meta:{
        requireLogin: true
    }
  },
  {
    path: '/dashboard/providers/add',
    name: 'AddProvider',
    component: AddProvider,
    meta:{
        requireLogin: true
    }
  },
  {
    path: '/dashboard/invoices/add',
    name: 'AddInvoice',
    component: AddInvoice,
    meta:{
        requireLogin: true
    }
  },
  {
    path: '/dashboard/invoices/:id',
    name: 'Invoice',
    component: Invoice,
    meta:{
        requireLogin: true
    }
  },
  {
    path: '/dashboard/clients',
    name: 'Clients',
    component: Clients,
    meta:{
        requireLogin: true
    }
  },
  {
    path: '/dashboard/clients/add',
    name: 'AddClient',
    component: AddClient,
    meta:{
        requireLogin: true
    }
  },
  {
    path: '/dashboard/clients/:id',
    name: 'Client',
    component: Client,
    meta:{
        requireLogin: true
    }
  },
  {
    path: '/dashboard/clients/:id/edit',
    name: 'EditClient',
    component: EditClient,
    meta:{
        requireLogin: true
    }
  },
  {
    path: '/dashboard/my-account',
    name: 'MyAccount',
    component: MyAccount,
    meta:{
        requireLogin: true
    }
  },
  {
    path: '/dashboard/my-account/edit-team',
    name: 'EditTeam',
    component: EditTeam,
    meta:{
        requireLogin: true
    }
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
        next('/log-in')
    } else {
        next()
    }
})

export default router
