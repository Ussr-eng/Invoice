<template>

        <div class="columns ">
            <div class="tabs">
              <ul>
                <li><router-link :to="{ name: 'MainPage' }" class="card-footer-item">Home</router-link></li>
                <li><router-link :to="{ name: 'AllProviders' }" class="card-footer-item">Все поставщики</router-link></li>
                <li class="is-active"><a>{{ provider.title }}</a></li>

              </ul>
            </div>
        </div>
        <div class="columns is-multiline">


            <div class="column is-12 mt-4">
                <h1 class="title mt-2 ml-2">{{ provider.title }}</h1>
            </div>

            <div class="column is-12 mt-1">
                <div class="buttons">
                    <router-link :to="{ name: 'AddProduct', params: { id: this.$route.params.id } }" class="button is-link is-outlined">Добавить товар</router-link>
                    <button @click="deleteProvider()" class="button is-danger is-outlined">Удалить поставщика</button>
                </div>
            </div>

            <div class="column is-12 mt-4 ml-2">
                <h2 class="subtitle">Детальная информация</h2>
                <b/>
                    <p>Количество заказов: <strong>{{ provider.count_orders }} </strong></p>
            </div>
        </div>

        <div class="column is-6">
            <div class="box table-container">
                <h2 class="subtitle">Товары данного поставщика</h2>

                        <table class="table is-bordered is-striped is-fullwidth">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Товар</th>
                            <th>Дроп цена</th>
                            <th>Розничная цена</th>
                            <th>Изменить</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr
                            v-for="(prod, index) in provider.product"
                            v-bind:key="prod.id"
                        >
                            <td>{{ index + 1 }}</td>
                            <td>{{ prod.title }}</td>
                            <td>{{ prod.drop_price }}</td>
                            <td>{{ prod.sale_price }}</td>
                            <td><router-link :to="{ name: 'EditProductProvider', params: { id: prod.id } }" class="button is-outlined">Изменить</router-link></td>

                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

</template>

<script>

    import axios from 'axios'
    import { toast } from 'bulma-toast'

    export default{
        name: 'Provider',
        data() {
            return {
                provider: {
                    product: []
                }
            }
        },
        mounted() {
            this.getProvider()
        },
        methods: {
            getProvider() {
                const providerId = this.$route.params.id

                axios
                    .get(`/api/v1/providers/${providerId}`)
                    .then(response => {
                        this.provider = response.data
                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })
            },
            deleteProvider(){
                const providerId = this.$route.params.id

                axios
                    .delete(`/api/v1/providers/${providerId}`)
                    .then(response => {

                        toast({
                            message: 'Поставщик успешно удален!',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 3000,
                            position: 'bottom-right',
                        })

                        this.$router.push('/dashboard/all_providers')
                    })
                    .catch(error => {
                        console.log(error);
                    })
            }
        }
    }

</script>