<template>
    <div class="page-home">
        <div class="columns is-multiline">
            <div class="column is-12">
                <div class="columns">
                    <div class="tabs">
                      <ul>

                      </ul>
                    </div>
                </div>
            </div>
            <div class="column is-4 mt-4">

            </div>

            <div class="column is-4 mb-1">
                <label>По периоду:</label>
                <div class="select">
                    <select name="provider_id" v-model="selected_date" @change="getOrdersData(selected_date)">
                        <option value="" selected>За весь период</option>
                        <option value="7" >7 дней</option>
                        <option value="14" >14 дней</option>
                        <option value="30" >месяц</option>

                    </select>
                </div>
            </div>

            <div class="column is-4 mb-1">
                <div class="field">
                    <label>По дате:</label>
                        <div class="control">
                            <input type="date" id="date" name="date" class="input" v-model="date_input" @change="getOrdersData(this.date_input)">
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





            <div class="column is-12 ">



              <div class="divider is-info">Итоговые данные</div>

                <nav class="level">
                  <div class="level-item has-text-centered">
                    <div>
                      <p class="heading">Прибыль</p>

                      <p class="title" v-if="total_data.income">{{ total_data.income }}</p>
                      <p class="title" v-else>---</p>

                    </div>
                  </div>

                  <div class="level-item has-text-centered">
                    <div>
                      <p class="heading">Средняя прибыль с заказа</p>

                      <p class="title" v-if="total_data.average_profit_per_order">{{ total_data.average_profit_per_order }}</p>
                      <p class="title" v-else>---</p>

                    </div>
                  </div>

                  <div class="level-item has-text-centered">
                    <div>
                      <p class="heading">Сумма всех заказов</p>
                      <p class="title" v-if="total_data.sum_of_all_orders">{{ total_data.sum_of_all_orders }}</p>
                      <p class="title" v-else>---</p>
                    </div>
                  </div>
                  <div class="level-item has-text-centered">
                    <div>
                      <p class="heading">Количество заказов</p>
                      <p class="title" v-if="total_data.count_orders">{{ total_data.count_orders }}</p>
                      <p class="title" v-else>---</p>
                    </div>
                  </div>
                  <div class="level-item has-text-centered">
                    <div>
                      <p class="heading">Успешные</p>
                      <p class="title" v-if="total_data.successful">{{ total_data.successful }}</p>
                      <p class="title" v-else>---</p>
                    </div>
                  </div>
                  <div class="level-item has-text-centered">
                    <div>
                      <p class="heading">Неуспешные</p>
                      <p class="title" v-if="total_data.unsuccessful">{{ total_data.unsuccessful }}</p>
                      <p class="title" v-else>---</p>
                    </div>
                  </div>
                </nav>
              <div class="divider is-info">/</div>
            </div>



            <div class="column  is-6 mt-4">
                <div class="box table-container">
                    <h2 class="subtitle">Статистика по товарам</h2>
                    <table class="table is-fullwidth">
                        <thead>
                            <tr>
                                <th>Товар</th>
                                <th>Поставщик</th>
                                <th>Прибыль</th>
                                <th>Успешные</th>
                                <th>Неуспешные</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr
                                v-for="product in products_data[0]"
                                v-bind:key="product.id"
                            >
                                <td>{{ product.title }}</td>
                                <td>{{ product.get_provider.title }}</td>
                                <td>{{ product.income }}</td>
                                <td>{{ product.get_success_orders }}</td>
                                <td>{{ product.get_unsuccess_orders }}</td>

                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="column is-6 mt-4">
                <div class="box table-container">
                    <h2 class="subtitle">Статистика по поставщикам</h2>
                    <table class="table is-fullwidth">
                        <thead>
                            <tr>
                                <th>Поставщик</th>
                                <th>Прибыль</th>
                                <th>Успешные</th>
                                <th>Неуспешные</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr
                                v-for="provider in providers_data[0]"
                                v-bind:key="provider.id"
                            >
                                <td>{{ provider.title }}</td>
                                <td>{{ provider.get_income_success_orders }}</td>
                                <td>{{ provider.get_success_orders }}</td>
                                <td>{{ provider.get_unsuccess_orders }}</td>

                            </tr>

                        </tbody>
                    </table>
                </div>
            </div>


        </div>

    </div>

</template>

<script>

    import axios from 'axios'


    export default {
        name: 'MyHome',
        data() {
            return {
                selected_date: '',
                date_input: '',
                total_data: [],
                products_data: [],
                providers_data: []
            }
        },
        mounted() {
            this.getOrdersData()
            this.getProductsData()
            this.getProvidersData()

        },
        methods: {

            getOrdersData(date) {

                axios
                    .post(`/api/v1/orders/get_orders_total_data/`, {date})
                    .then(response => {

                        this.total_data = response.data

                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })
            },
            getProductsData() {

                axios
                    .post(`/api/v1/products/data_for_main_page/`)
                    .then(response => {
                        for (let i = 0; i < response.data.length; i++) {
                            this.products_data.push(response.data[i])
                        }

                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })

            },
            getProvidersData() {

                axios
                    .post(`/api/v1/providers/data_for_main_page/`)
                    .then(response => {
                        this.providers_data = response.data

                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })
            },
            changeDateField(){

                this.date_input = ''

                axios
                    .post(`/api/v1/orders/get_orders_total_data/`)
                    .then(response => {

                        this.total_data = response.data

                    })

            }

        }
    }
</script>


