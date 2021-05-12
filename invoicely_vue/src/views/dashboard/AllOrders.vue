<template>

    <div class="page-orders">
        <div class="columns is-multiline">
            <div class="column is-12">
                <div class="columns ">
                    <div class="tabs">
                      <ul>
                        <li><router-link :to="{ name: 'MainPage' }" class="card-footer-item">Home</router-link></li>
                        <li class="is-active"><a>Все заказы</a></li>

                      </ul>
                    </div>
                </div>

            </div>
            <div class="column is-4 mt-5">
                <label>По статусу заказа:</label>
                <div class="select">
                    <select name="status_order" v-model="status_order" @change="getOrdersByProviderDate()">
                        <option value="" selected>Все заказы</option>
                        <option value="Продажа" >Продажа</option>
                        <option value="Отказ" >Отказ</option>
                        <option value="Заказ" >Заказ</option>
                    </select>
                </div>

            </div>

            <div class="column is-4 mt-5">
            <label>По поставщикам:</label>
                <div class="select">
                    <select name="provider_id" v-model="provider_id" @change="getOrdersByProviderDate()">
                        <option value="" selected>Все поставщики</option>
                        <option
                            v-for="provider in all_providers"
                            v-bind:key="provider.id"
                            v-bind:value="provider"
                        >
                            {{ provider.title }}
                        </option>
                    </select>
                </div>
            </div>


            <div class="column is-4 mt-5">
                <div class="field">
                    <label>По дате:</label>

                    <div class="control">
                        <input type="date" id="date" name="date" class="input" v-model="get_orders_by_providers_date.date" @change="getOrdersByProviderDate()">
                    </div>

                    <div class="control has-text-right mr-4">

                      <div class="dropdown is-right is-hoverable">
                        <div class="dropdown-trigger">
                            <a class="far fa-calendar-times mt-2" v-on:click="changeDateField()" aria-hidden="true" ></a>
                        </div>
                      <div class="dropdown-menu" id="dropdown-menu4" role="menu">
                        <div class="dropdown-content">
                          <div class="dropdown-item">
                            <p>Чтобы <strong>очистить поле</strong> даты нажмите на  <i class="far fa-calendar-times fa-sm"></i> .</p>
                          </div>
                        </div>
                      </div>

                    </div>

                    </div>


                </div>
            </div>




            <div class="column table-container ">
                <table class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth">
                    <thead>
                        <tr>
                          <th><abbr title="id">#</abbr></th>
                          <th><abbr title="дата">Дата</abbr></th>
                          <th><abbr title="клиент">Клиент</abbr></th>
                          <th><abbr title="товар">Товар</abbr></th>
                          <th><abbr title="город">Город</abbr></th>
                          <th><abbr title="Статус ТТН">ТТН</abbr></th>
                          <th><abbr title="общая сумма">Сумма</abbr></th>
                          <th><abbr title="статус выплаты">Выплата</abbr></th>
                          <th><abbr title="статус заказа">Статус</abbr></th>
                          <th style="text-align: center;"><abbr title="информация по заказу"><p class="fas fa-info-circle"></p></abbr></th>
                        </tr>
                    </thead>
                    <tfoot>
                        <tr>
                          <th><abbr title="id">#</abbr></th>
                          <th><abbr title="дата">Дата</abbr></th>
                          <th><abbr title="клиент">Клиент</abbr></th>
                          <th><abbr title="товар">Товар</abbr></th>
                          <th><abbr title="город">Город</abbr></th>
                          <th><abbr title="Статус ТТН">ТТН</abbr></th>
                          <th><abbr title="общая сумма">{{ totalSalePrice }}</abbr></th>
                          <th><abbr title="статус выплаты">Выплата</abbr></th>
                          <th><abbr title="статус заказа">Статус</abbr></th>
                          <th style="text-align: center;"><abbr title="информация по заказу"><p class="fas fa-info-circle"></p></abbr></th>
                        </tr>
                      </tfoot>

                    <tbody>
                        <tr
                            v-for="order in orders"
                            v-bind:key="order.id"
                        >
                            <td>{{ order.id }}</td>
                            <td>{{ order.get_date_formatted }}</td>
                            <td>{{ order.name }}</td>
                            <td>{{ order.product_id.title }}</td>
                            <td>{{ order.city }}</td>
                            <td v-if="order.consignment_note">{{ order.consignment_note }}</td>
                            <td v-else>вы не указали ТТН</td>
                            <td >{{ order.product_id.sale_price }}</td>
                            <td>{{ order.payout_status_id.title }}</td>
                            <td v-if="order.order_status_id.title  == 'Отказ'" style="background-color: #ff000091">{{ order.order_status_id.title }}</td>
                            <td v-if="order.order_status_id.title  == 'Продажа'" style="background-color: #00ff087a">{{ order.order_status_id.title }}</td>
                            <td v-if="order.order_status_id.title  == 'Доставка'" style="background-color: #ffd400a3">{{ order.order_status_id.title }}</td>
                            <td v-if="order.order_status_id.title  == 'Заказ'">{{ order.order_status_id.title }}</td>
                            <td style="text-align: center;"><router-link :to="{ name: 'Order', params: { id: order.id } }" ><i class="fas fa-info-circle"></i></router-link></td>
                        </tr>
                    </tbody>
                </table>


                <nav class="pagination is-centered" v-if="pagination_default">
                    <ul class="pagination-list">
                        <li>
                            <a class="pagination-link" v-if="showPrevButton" @click="loadPrev()"><a class="fas fa-chevron-circle-left"></a></a>
                            <a class="pagination-link" v-if="showNextButton" @click="loadNext()"><a class="fas fa-chevron-circle-right"></a></a>
                        </li>
                    </ul>
                </nav>

                <nav class="pagination is-centered" v-if="!pagination_default">
                    <ul class="pagination-list">
                        <li>
                            <a class="pagination-link" v-if="showPrevButton" @click="loadPrev()"><a class="fas fa-chevron-circle-left"></a></a>
                            <a class="pagination-link" v-if="showNextButton" @click="loadNext()"><a class="fas fa-chevron-circle-right"></a></a>
                        </li>
                    </ul>
                </nav>




            </div>
        </div>
    </div>

</template>

<script>

    import axios from 'axios'
    import Pagination from '@/components/Pagination.vue'
    import PaginationByProviderDate from '@/components/PaginationByProviderDate.vue'


    export default {
        name: 'AllOrders',
        components: { Pagination, PaginationByProviderDate },
        data() {
            return {
                get_orders_by_providers_date: {
                },
                pagination_default: true,
                showNextButton: false,
                showPrevButton: false,
                provider_id: '',
                status_order: '',
                orders: [],
                all_providers: [],
                quantity_page: 0,
                page: 1,

            }
        },
        mounted() {
            this.getOrders(this.page)
        },
        methods: {
            loadPrev(){
                this.showNextButton = false
                this.showPrevButton = false
                this.page -= 1
                if(this.pagination_default) {
                    this.getOrders(this.page)

                }else{
                    this.getOrdersByProviderDate(this.page)
                }
            },
            loadNext(){
                this.showNextButton = false
                this.showPrevButton = false
                this.page += 1
                if(this.pagination_default) {
                    this.getOrders(this.page)

                }else{
                    this.getOrdersByProviderDate(this.page)
                }
            },
            getOrders(pageNumber) {

                this.pagination_default = true

                axios
                    .get(`/api/v1/orders/?page=${pageNumber}`)
                    .then(response => {


                        if (response.data.next) {
                            this.showNextButton = true
                        } else {
                            this.showNextButton = false
                        }


                        if (response.data.previous) {
                            this.showPrevButton = true
                        } else {
                            this.showPrevButton = false
                        }


                        if (this.orders.length > 0) {
                            this.orders = []
                            for (let i = 0; i < response.data.results.length; i++) {
                                this.orders.push(response.data.results[i])
                            }
                        } else {
                            for (let i = 0; i < response.data.results.length; i++) {
                                this.orders.push(response.data.results[i])
                            }
                        }



                    })



                axios
                    .get('/api/v1/providers/')
                    .then(response => {
                        this.all_providers = response.data
                    })


            },
            getOrdersByProviderDate(pageNumber) {

                this.pagination_default = false

                this.get_orders_by_providers_date.provider_id = this.provider_id.id

                if (this.status_order){
                    this.get_orders_by_providers_date.status_order = this.status_order
                } else {
                    delete this.get_orders_by_providers_date.status_order
                }

                    if (pageNumber) {

                        axios
                            .post(`/api/v1/orders/get_orders_by_providers_date/?page=${pageNumber}`, this.get_orders_by_providers_date)
                            .then(response => {
                                if (response.data.next) {
                                    this.showNextButton = true
                                } else {
                                    this.showNextButton = false
                                }


                                if (response.data.previous) {
                                    this.showPrevButton = true
                                } else {
                                    this.showPrevButton = false
                                }

                                this.orders = response.data.results
                            })

                    } else {

                        axios
                            .post(`/api/v1/orders/get_orders_by_providers_date/?page=${1}`, this.get_orders_by_providers_date)
                            .then(response => {
                                if (response.data.next) {
                                    this.showNextButton = true
                                } else {
                                    this.showNextButton = false
                                }


                                if (response.data.previous) {
                                    this.showPrevButton = true
                                } else {
                                    this.showPrevButton = false
                                }

                                this.orders = response.data.results

                            })
                    }


            },
            changeDateField() {

                this.pagination_default = false
                delete this.get_orders_by_providers_date.date
                this.page = 1
                this.getOrdersByProviderDate()

            },

        },
        computed: {
            totalSalePrice() {
                let sum = 0

                for(let i = 0; i < this.orders.length; i++)
                    sum += this.orders[i].product_id.sale_price

                return sum
            }



        },
    }
</script>
