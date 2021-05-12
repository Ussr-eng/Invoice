<template>
    <div class="columns ">
        <div class="tabs">
          <ul>
            <li><router-link :to="{ name: 'MainPage' }" class="card-footer-item">Home</router-link></li>
            <li><router-link :to="{ name: 'AllProviders' }" class="card-footer-item">Все поставщики</router-link></li>
            <li><router-link :to="{ name: 'Provider', params:{ id: this.provider.id }}" >{{ this.provider.title }}</router-link></li>



          </ul>
        </div>
    </div>

    <div class="content column is-half is-offset-one-quarter">
        <div class="column">
            <div class="box">

                    <div class="column">
                        <div class="field">
                            <label>Название товара:</label>
                            <div class="control">
                                <input type="text" class="input is-rounded" v-model="product.title">
                            </div>
                        </div>
                    </div>

                    <div class="column">
                        <div class="field">
                            <label>Дроп цена:</label>
                            <div class="control">
                                <input type="number" class="input is-rounded" v-model="product.drop_price">
                            </div>
                        </div>
                    </div>

                    <div class="column">
                        <div class="field">
                            <label>Розничная цена:</label>
                            <div class="control">
                                <input type="number" class="input is-rounded" v-model="product.sale_price">
                            </div>
                        </div>
                    </div>

                    <div class="column">
                        <button class="button is-success is-rounded" @click="submitForm">Добавить товар</button>
                    </div>
            </div>
        </div>
    </div>

</template>

<script>

    import axios from 'axios'
    import { toast } from 'bulma-toast'

    export default {
        name: 'AddProduct',
        data() {
            return {
                product: {},
                provider: []
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
            submitForm() {


                axios
                    .post(`/api/v1/products/${this.$route.params.id}/create_product/`, this.product)
                    .then(response => {
                        toast({
                            message: 'Товар успешно добавлен',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 1500,
                            position: 'bottom-right',
                        })

                        this.$router.push(`/dashboard/provider/${this.provider.id}`)
                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })

            }
        }
    }

</script>