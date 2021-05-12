<template>
    <div class="content column is-half is-offset-one-quarter">


        <div class="column">
            <div class="box">
                <div class="columns ">
                    <div class="column ">
                        <div class="field">
                            <label>Имя поставщика:</label>
                            <div class="control">
                                <input type="text" class="input is-focused is-rounded" v-model="provider.provid.title">
                            </div>
                        </div>
                    </div>
                </div>
                <h2 class="is-size-5 mb-5">Товары</h2>
                <ProviderForm
                    v-for="product in provider.product"
                    v-bind:initialProduct="product"
                >

                </ProviderForm>
                <button class="button is-link is-rounded" @click="addProduct">+1 товар</button>
            </div>
        </div>

        <div class="column is-12">
            <button class="button is-success is-rounded" @click="submitForm">Сохранить поставщика</button>
        </div>
    </div>

</template>

<script>

    import axios from 'axios'
    import { toast } from 'bulma-toast'
    import ProviderForm from '@/components/ProviderForm.vue'

    export default {
        name: 'AddProvider',
        components: {
            ProviderForm
        },
        data() {
            return {
                provider: {
                    provid: {},
                    product: [
                        {
                            title: '',
                            drop_price: 0,
                            sale_price: 0,

                        }
                    ],
                }
            }
        },
        methods: {
            addProduct () {
                this.provider.product.push({
                    title: '',
                    drop_price: 0,
                    sale_price: 0,
                })
            },
            submitForm() {
                this.provider.title = this.provider.provid.title

                axios
                    .post('/api/v1/providers/', this.provider)
                    .then(response => {
                        toast({
                            message: 'Поставщик успешно добавлен!',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 3500,
                            position: 'bottom-right',
                        })

                        this.$router.push('/dashboard/all_providers')
                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })
            }
        }
    }

</script>