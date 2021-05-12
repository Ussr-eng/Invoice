<template>

    <div class="all providers">
        <div class="columns is-multiline">
            <div class="column is-12">
                <div class="columns ">
                    <div class="tabs">
                      <ul>
                        <li><router-link :to="{ name: 'MainPage' }" class="card-footer-item">Home</router-link></li>
                        <li class="is-active"><a>Все поставщики</a></li>

                      </ul>
                    </div>
                </div>
            </div>
        </div>

            <div class="columns is-multiline mt-6">
                <div
                    class="column is-2"
                    v-for="provider in providers"
                    v-bind:key="provider.id"
                >
                    <div class="card">
                      <header class="card-header">
                        <p class="card-header-title">
                          {{ provider.title }}
                        </p>
                          <p class="card-header-title-right mr-3 mt-3" >
                            <i class="fas fa-user-alt"></i>
                            </p>
                      </header>
                      <div class="card-content">
                        <div class="content">
                          количество заказов: {{ provider.count_orders }}
                          количество продуктов: {{ provider.count_product }}


                          <br>

                        </div>
                      </div>
                      <footer class="card-footer">
                        <router-link :to="{ name: 'Provider', params:{ id: provider.id } }" class="card-footer-item">информация</router-link>

                      </footer>
                    </div>
                </div>
            </div>
        </div>

</template>

<script>

    import axios from 'axios'

    export default {
        name: 'AllProviders',
        data() {
            return {
                providers: []
            }
        },
        mounted() {
            this.getProviders()
        },
        methods: {
            getProviders() {
                axios
                    .get('/api/v1/providers/')
                    .then(response => {
                        for (let i = 0; i < response.data.length; i++) {
                            this.providers.push(response.data[i])
                        }
                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })
            }
        }

    }


</script>