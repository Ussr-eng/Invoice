<template>

    <div class="content column is-half is-offset-one-quarter">

        <div class="box" >

                <div class="columns is-multiline">
                    <div class="column is-12">
                        <h1 class="title">Создать заказ</h1>
                    </div>


                    <div class="column">

                        <div class="field">
                            <label>ФИО:</label>
                            <div class="control">
                                <input type="text" class="input is-rounded" v-model="result.name">
                            </div>
                        </div>

                        <div class="field">
                            <label>Номер телефона:</label>
                            <div class="control">
                                <input type="text"  class="input is-rounded" maxlength="18" v-model="result.telephone">
                            </div>
                        </div>


                        <label>Поставщик:</label>
                        <div class="select is-rounded">
                            <select name="provider_id"  @change="getProducts()" v-model="result.provider_id">
                                <option value="" selected>Выберите поствщика или добавьте нового</option>
                                <option
                                    v-for="provider in providers"
                                    v-bind:key="provider.id"
                                    v-bind:value="provider"
                                >
                                    {{ provider.title }}
                                </option>
                            </select>
                        </div>



                            <router-link :to="{ name: 'AddProvider' }">Добавить поставщика</router-link>
                            <div class="mt-4" @change="getProduct()" v-if="result.provider_id">
                                <label>Товар:</label>
                                <div class="select is-rounded">
                                    <select name="product_id" v-model="result.product_id">
                                        <option value="" selected>Выберите товар</option>
                                        <option
                                            v-for="product in products"
                                            v-bind:key="product.id"
                                            v-bind:value="product"
                                        >
                                            {{ product.title }}
                                        </option>
                                    </select>
                                </div>
                            </div>
                            <div class="columns mt-2">
                                <div class="column" v-if="result.product_id.id">
                                    <div class="field">
                                        <label>Дроп цена:</label>
                                        <div class="control">
                                            <input type="number" class="input is-rounded" v-model="result.product_detail.drop_price">
                                        </div>
                                    </div>
                                </div>

                                <div class="column" v-if="result.product_id.id">
                                    <div class="field">
                                        <label>Цена продажи:</label>
                                        <div class="control">
                                            <input type="number" class="input is-rounded" v-model="result.product_detail.sale_price">
                                        </div>
                                    </div>
                                </div>

                                <div class="column" v-if="result.product_id.id">
                                    <div class="field">
                                        <label>Размер:</label>
                                        <div class="control">
                                            <input placeholder="пометка к размеру" type="text" class="input is-rounded" v-model="result.size">
                                        </div>
                                    </div>
                                </div>


                                <div class="column" v-if="result.product_id.id">
                                    <div class="field">
                                        <label>Количество:</label>
                                        <div class="control">
                                            <input type="number" class="input is-rounded" v-model="result.quantity">
                                        </div>
                                    </div>
                                </div>
                            </div>



                        <div class="field">
                            <label>Город:</label>
                                <div class="control">
                                    <input type="text"  class="input is-rounded" v-model="result.city">
                                </div>
                        </div>


                        <div class="field">
                            <label>Отделение почты:</label>
                                <div class="control">
                                    <input type="text" class="input is-rounded" v-model="result.warehouse">
                                </div>
                        </div>


                        <div class="field">
                             <label>Накладная:</label>
                                <div class="control">
                                    <input type="text" placeholder="Это поле вы сможете добавить позже" class="input is-rounded" v-model="result.consignment_note">
                                </div>
                        </div>

                           <div class="field">
                            <div class="control">
                                <input type="radio" value="Доставка Новой почтой" v-model="result.settings_delivery" />
                                    <label> Доставка Новой почтой</label>
                            </div>
                            <div class="control">
                                <input type="radio" value="Доставка Укр почтой" v-model="result.settings_delivery" />
                                    <label> Доставка Укр почтой</label>
                            </div>
                            <div class="control">
                                <input type="radio" value="Самомывоз" v-model="result.settings_delivery" />
                                    <label> Самомывоз</label>
                            </div>
                            <div class="control">
                            <input type="radio" value="Доставка курьером" v-model="result.settings_delivery" />
                                <label> Доставка курьером</label>

                            </div>




                       <div class="columns mt-1">
                            <div class="column">
                                <div class="field">
                                    <label>Предоплата:</label>
                                    <div class="control">
                                        <input type="number" placeholder="Введите сумму предоплаты" class="input is-rounded" v-model="result.prepayment">
                                    </div>
                                </div>
                            </div>

                            <div class="column">
                                <div class="field">
                                    <label>Наложенный платеж:</label>
                                    <div class="control">
                                        <input type="number" class="input is-rounded" v-model="result.cash_on_delivery">
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>

                    <div class="field">
                        <div class="mt-4">
                            <label>Источник заказа:</label>
                            <div class="select is-rounded">
                                <select name="source_order_id" v-model="result.source_order_id">
                                    <option value="" selected>Выберите источник заказа</option>
                                    <option
                                        v-for="source in source_order"
                                        v-bind:key="source.id"
                                        v-bind:value="source"
                                    >
                                        {{ source.title }}
                                    </option>
                                </select>
                            </div>
                        </div>
                        <a v-if="!this.createNewSourceOrder"  @click="hideAddingSourceOrder">Добавить источник заказа</a>
                        <a v-else @click="hideAddingSourceOrder">Скрыть</a>
                    </div>
                    <div v-if="createNewSourceOrder">
                        <CreateSourceOrder v-on:updated="UpdatedSourceOrder"/>
                    </div>


                    <div class="field">
                        <div class="mt-4">
                            <label>Источник трафика:</label>
                            <div class="select is-rounded">
                                <select name="source_traffic_id" v-model="result.source_traffic_id">
                                    <option value="" selected>Выберите источник трафика</option>
                                    <option
                                        v-for="source in source_traffic"
                                        v-bind:key="source.id"
                                        v-bind:value="source"
                                    >
                                        {{ source.title }}
                                    </option>
                                </select>
                            </div>
                        </div>
                        <a v-if="!this.createNewSource"  @click="hideAddingSource">Добавить источник трафика</a>
                        <a v-else @click="hideAddingSource">Скрыть</a>
                    </div>
                    <div v-if="createNewSource">
                        <CreateSourceTraffic v-on:updated="UpdatedSourceTraffic"/>
                    </div>


                    <div class="field mt-3">
                        <div class="mt-4">
                            <label>Статус заказа:</label>
                            <div class="select is-rounded">
                                <select name="order_status_id" v-model="result.order_status_id">
                                    <option value="" selected>Выберите статус заказа</option>
                                    <option
                                        v-for="status in order_status"
                                        v-bind:key="status.id"
                                        v-bind:value="status"
                                    >
                                        {{ status.title }}
                                    </option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <div class="field">
                        <div class="mt-4">
                            <label>Статус выплаты:</label>
                            <div class="select is-rounded">
                                <select name="payout_status_id" v-model="result.payout_status_id">
                                    <option value="" selected>Выберите статус выплаты</option>
                                    <option
                                        v-for="status in payout_status"
                                        v-bind:key="status.id"
                                        v-bind:value="status"
                                    >
                                        {{ status.title }}
                                    </option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <div class="columns mt-2">
                        <div class="column">
                            <div class="">
                                <button class="button is-success is-rounded" @click="submitForm">Сохранить заказ</button>
                            </div>
                        </div>

                        <div class="column">
                        </div>

                        <div class="column">
                        </div>

                        <div class="column ml-5 mt-2">
                            <p v-if="superimposed_amount">прибыль с заказа: {{ superimposed_amount }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>




<script>

    import axios from 'axios'
    import { toast } from 'bulma-toast'
    import CreateSourceTraffic from '@/components/CreateSourceTraffic.vue'
    import CreateSourceOrder from '@/components/CreateSourceOrder.vue'

    export default {
        name: 'AddOrder',
        components: { CreateSourceTraffic, CreateSourceOrder },
        data () {
            return {
                result: {
                    name: '',
                    telephone: '',
                    quantity: 1,
                    cash_on_delivery: 0,
                    payout_status_id: '',
                    order_status_id: '',
                    source_traffic_id: '',
                    source_order_id: '',
                    provider_id: '',
                    product_id: '',
                    product_detail: {},
                    size: '',
                    city: '',
                    warehouse: '',
                    consignment_note: '',
                    settings_delivery: '',
                    prepayment: '',
                },
                createNewSourceOrder: false,
                createNewSource: false,
                providers: [],
                products: [],
                source_traffic: [],
                source_order: [],
                order_status: [],
                payout_status: [],

            }
        },
        async mounted() {
            await this.getProviders()
        },
        methods: {
            getProviders () {
                axios
                    .get('/api/v1/providers/')
                    .then(response => {
                        this.providers = response.data
                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })

                axios
                    .get('/api/v1/source_traffic/')
                    .then(response => {
                        if (response.data.length ==  0) {
                            axios
                                .get('/api/v1/source_traffic/set_default/')
                                .then(response => {
                                    this.source_traffic = response.data
                                })
                                .catch(error => {
                                    console.log(JSON.stringify(error))
                                })
                        } else {
                            this.source_traffic = response.data
                        }
                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })

                axios
                    .get('/api/v1/source_orders/')
                    .then(response => {
                        if (response.data.length ==  0) {
                            axios
                                .get('/api/v1/source_orders/set_default/')
                                .then(response => {
                                    this.source_order = response.data
                                })
                                .catch(error => {
                                    console.log(JSON.stringify(error))
                                })
                        } else {
                            this.source_order = response.data
                        }
                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })

                axios
                    .get('/api/v1/order_status/')
                    .then(response => {
                        if (response.data.length ==  0) {
                            axios
                                .get('/api/v1/order_status/set_default/')
                                .then(response => {
                                    this.order_status = response.data
                                })
                                .catch(error => {
                                    console.log(JSON.stringify(error))
                                })
                        } else {
                            this.order_status = response.data
                        }
                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })

                axios
                    .get('/api/v1/payout_status/')
                    .then(response => {
                        if (response.data.length ==  0) {
                            axios
                                .get('/api/v1/payout_status/set_default/')
                                .then(response => {
                                    this.payout_status = response.data
                                })
                                .catch(error => {
                                    console.log(JSON.stringify(error))
                                })
                        } else {
                            this.payout_status = response.data
                        }
                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })

            },
            getProducts () {

                axios
                    .get(`/api/v1/products/?provider_id=${this.result.provider_id.id}`)
                    .then(response => {
                        this.products = response.data
                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })
            },
            getProduct() {

                axios
                    .get(`/api/v1/products/?product_id=${this.result.product_id.id}`)
                    .then(response => {
                        this.result.product_detail = response.data[0]
                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })
            },
            hideAddingSourceOrder() {
                this.createNewSourceOrder = !this.createNewSourceOrder
            },
            hideAddingSource() {
                this.createNewSource = !this.createNewSource
            },
            UpdatedSourceTraffic() {
                if (this.createNewSource == true) {
                    this.timer = setTimeout(() => {
                        this.createNewSource = !this.createNewSource;
                    }, 300);
                }


                this.timer = setTimeout(() => {
                    axios
                        .get('/api/v1/source_traffic/')
                        .then(response => {
                            this.source_traffic = response.data
                        })
                        .catch(error => {
                            console.log(JSON.stringify(error))
                        })
                }, 600)
            },
            UpdatedSourceOrder() {
                if (this.createNewSourceOrder == true) {
                    this.timer = setTimeout(() => {
                        this.createNewSourceOrder = !this.createNewSourceOrder;
                    }, 300);
                }


                this.timer = setTimeout(() => {
                    axios
                        .get('/api/v1/source_orders/')
                        .then(response => {
                            this.source_order = response.data
                        })
                        .catch(error => {
                            console.log(JSON.stringify(error))
                        })
                }, 600)
            },
            submitForm() {


                this.result.name = this.result.name
                this.result.telephone = this.result.telephone
                this.result.provider_id = this.result.provider_id.id
                this.result.product_id = this.result.product_id.id
                this.result.size = this.result.size
                this.result.quantity = this.result.quantity
                this.result.city = this.result.city
                this.result.warehouse = this.result.warehouse
                this.result.consignment_note = this.result.consignment_note
                this.result.settings_delivery = this.result.settings_delivery
                this.result.prepayment = this.result.prepayment
                this.result.cash_on_delivery = this.result.cash_on_delivery
                this.result.source_order_id = this.result.source_order_id.id
                this.result.source_traffic_id = this.result.source_traffic_id.id
                this.result.order_status_id = this.result.order_status_id.id
                this.result.payout_status_id = this.result.payout_status_id.id


                axios
                    .post(`/api/v1/products/edit_price/`, this.result.product_detail)
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })

                this.timer = setTimeout(() => {
                    axios
                        .post('/api/v1/orders/', this.result)
                        .then(response => {
                        toast({
                            message: 'Заказ успешно добавлен!',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 3000,
                            position: 'bottom-right',
                        })

                        this.$router.push('/dashboard/orders')
                    })
                        .catch(error => {
                            console.log(JSON.stringify(error))
                        })
                }, 150)



            }
        },
        computed: {
            superimposed_amount() {

                return this.result.product_detail.sale_price - this.result.product_detail.drop_price
            }
        }

    }
</script>




