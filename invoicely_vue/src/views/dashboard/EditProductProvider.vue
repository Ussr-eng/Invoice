<template>

    <div class="columns ">
        <div class="tabs">
          <ul>
            <li><router-link :to="{ name: 'MainPage' }" class="card-footer-item">Home</router-link></li>
            <li><router-link :to="{ name: 'AllProviders' }" class="card-footer-item">Все поставщики</router-link></li>
            <li><router-link :to="{ name: 'Provider', params:{ id: provider.id } }" class="card-footer-item">{{ provider.title }}</router-link></li>
            <li class="is-active"><a>{{ product.title }} (редактировать)</a></li>

          </ul>
        </div>
    </div>

    <div class="content column is-half is-offset-one-quarter">


        <div class="box" >
            <div class="columns is-multiline">
                <div class="column is-12">
                    <h1 class="title">Редактировать продукт</h1>
                </div>

                <div class="column">

                    <div class="field">
                        <label>Название товара:</label>
                        <div class="control">
                            <input type="text" class="input is-rounded" v-model="product.title">
                        </div>
                    </div>

                    <div class="field">
                        <label>Дроп цена:</label>
                        <div class="control">
                            <input type="number"  class="input is-rounded"  v-model="product.drop_price">
                        </div>
                    </div>

                    <div class="field">
                        <label>Цена продажи:</label>
                        <div class="control">
                            <input type="number"  class="input is-rounded" v-model="product.sale_price">
                        </div>
                    </div>

                </div>

                <div class="column is-12">
                    <button class="button is-success is-rounded" @click="submitForm">Сохранить</button>
                </div>
            </div>
        </div>
    </div>

</template>

<script>

    import axios from 'axios'
    import { toast } from 'bulma-toast'

    export default {
        name: 'EditProductProvider',
        data() {
            return {
                product : [],
                provider : []
            }
        },
        mounted() {
            this.getProduct()

        },
        methods: {
            getProduct() {

                const product_id = this.$route.params.id


                axios
                    .get(`/api/v1/products/?product_id=${product_id}`)
                    .then(response => {
                        this.product = response.data[0]


                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })

                this.timer = setTimeout(() => {


                    axios
                        .get(`/api/v1/providers/${this.product.get_provider_id}`)
                        .then(response => {
                            this.provider = response.data
                        })
                        .catch(error => {
                            console.log(JSON.stringify(error))
                        })

                }, 100)

            },

            submitForm() {
                axios
                    .post(`/api/v1/products/edit_price/`, this.product)
                    .then(response => {
                        toast({
                            message: 'Продукт успешно изменен',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 4000,
                            position: 'bottom-right',
                        })

                        this.$router.push(`/dashboard/provider/${this.provider.id}`)
                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })

            },
        }
    }

</script>