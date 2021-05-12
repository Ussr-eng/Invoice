<template>
    <div id="wrapper">

                <nav class="navbar" role="navigation" aria-label="main navigation">
                    <div class="navbar-brand">
                        <router-link to="/" class="navbar-item"><strong><a class="fas fa-lemon fa-2x ml-3"></a></strong></router-link>

                        <a class="navbar-burger" @click="burger = !burger" :class="{ 'is-active': burger }">
                            <span></span>
                            <span></span>
                            <span></span>
                        </a>
                    </div>
                <div class="navbar-menu" id="navbarBasicExample" @click="burger = !burger" :class="{ 'is-active': burger }">
                    <template v-if="$store.state.isAuthenticated">
                        <div class="navbar-start">
                            <router-link :to="{ name: 'MainPage' }" class="navbar-item" >Home</router-link>
                            <router-link :to="{ name: 'AllProviders' }" class="navbar-item">Все поставщики</router-link>
                            <router-link :to="{ name: 'AllOrders' }" class="navbar-item" >Все заказы</router-link>

                        </div>
                        <div class="navbar-end">
                            <div class="navbar-item">
                                <div class="buttons">

                                    <router-link :to="{ name: 'AddProvider' }" class="button is-success " ><i class="fas fa-plus"></i>поставщик</router-link>

                                    <router-link :to="{ name: 'AddOrder' }" class="button is-success" ><i class="fas fa-plus"></i> заказ</router-link>

                                    <button @click="logout()" class="button is-danger">Выход</button>
                                </div>


                            </div>
                        </div>
                    </template>

                    <template v-else>
                        <div class="navbar-end">
                            <div class="navbar-item">
                                <div class="buttons">

                                    <router-link to="/log-in" class="button is-light">Войти</router-link>
                                    <router-link to="/sign-up" class="button is-success"><strong>Регистрация</strong></router-link>
                                </div>
                            </div>
                        </div>
                    </template>
                </div>
            </nav>

        <section class="section">
          <router-view/>
        </section>
    </div>

</template>

<script>
    import axios from 'axios'

    export default {
        name: 'App',
        beforeCreate() {
            this.$store.commit('initializeStore')

            const token = this.$store.state.token

            if (token) {
                axios.defaults.headers.common['Authorization'] = "Token " + token
            } else {
                axios.defaults.headers.common['Authorization'] = ""
            }
        },
        data () {
            return {
                burger: false
            }
        },
        methods: {
            logout() {
                axios
                    .post("/api/v1/token/logout/")
                    .then(response => {

                        axios.defaults.headers.common["Authorization"] = ""

                        localStorage.removeItem("username")
                        localStorage.removeItem("userid")
                        localStorage.removeItem("token")

                        this.$store.commit('removeToken')

                        this.$router.push('/')
                    })
            }
        }

    }
</script>



<style lang="scss">
@import '../node_modules/bulma';
@import "~@creativebulma/bulma-divider";

</style>

