<template>
    <div class="content column is-half is-offset-one-quarter">
        <div class="box" >
            <div class="columns is-multiline">
                <div class="column is-10">
                    <h1 class="title">Информация о заказе №{{ client.id }}</h1>
                </div>
                <div class="column is-1 mt-2">
                    <a><i class="fas fa-file-download  fa-lg ml-4" @click="getPdf()"></i></a>
                </div>
                <div class="column is-1 mt-2">
                    <a><i class="far fa-trash-alt fa-lg mr-5" @click="deleteOrder()"></i></a>
                </div>


                <div class="column is-12">
                    <p v-if="client.id"><strong>id:</strong> {{ client.id }}</p>
                    <p v-if="client.get_date_formatted"><strong>Дата:</strong> {{ client.get_date_formatted }}</p>

                    <p  v-if="client.order_status_id"><strong>Статус заказа:</strong> {{ client.order_status_id.title }} <a><i class="fas fa-edit ml-2" @click="hideEditStatusOrder"></i></a></p>
                    <p  v-if="editOrderStatusId">
                        <EditStatusOrder v-on:updated="UpdatedStatusOrder"/>
                    </p>

                    <p  v-if="client.order_status_id"><strong>Статус выплаты:</strong> {{ client.payout_status_id.title }} <a><i class="fas fa-edit  ml-2" @click="hideEditStatusPayout"></i></a></p>
                    <p  v-if="editPayoutStatusId">
                        <EditStatusPayout v-on:updated="UpdatedStatusPayout"/>
                    </p>

                    <p v-if="client.consignment_note"><strong>Номер накладной:</strong> {{ client.consignment_note }} <a><i class="fas fa-edit  ml-2" @click="hideEditConsignmentNote"></i></a></p>
                    <p v-if="!client.consignment_note"><strong>Номер накладной:</strong> Вы не указали <a><i class="fas fa-edit  ml-2" @click="hideEditConsignmentNote"></i></a></p>
                    <p v-if="editConsignmentNote">
                        <EditConsignmentNote v-on:updated="UpdatedConsignmentNote"/>
                    </p>
                    <p v-if="client.product_id"><strong>Сумма:</strong> {{ client.product_id.sale_price }}</p>
                    <p v-if="client.income"><strong>Прибыль:</strong> {{ client.income }}</p>
                    <hr style="height: 3px;">
                    <p v-if="client.telephone"><strong>Имя клиента:</strong> {{ client.name }}</p>
                    <p v-if="client.telephone"><strong>Номер телефона:</strong> {{ client.telephone }}</p>
                    <p v-if="client.product_id"><strong>Товар:</strong> {{ client.product_id.title }}</p>
                    <p v-if="client.provider_id"><strong>Поставщик:</strong> {{ client.provider_id.title }}</p>
                    <p v-if="client.city"><strong>Город:</strong> {{ client.city }}</p>
                    <p v-if="client.warehouse"><strong>Отделение почты:</strong> {{ client.warehouse }}</p>
                    <p v-if="client.prepayment"><strong>Предоплата:</strong> {{ client.prepayment }}</p>
                    <p v-if="client.source_order_id"><strong>Источник заказа:</strong> {{ client.source_order_id.title }}</p>
                    <p v-if="client.source_traffic_id"><strong>Источник трафика:</strong> {{ client.source_traffic_id.title }}</p>

                </div>
            </div>
        </div>
    </div>
</template>

<script>

    import axios from 'axios'
    import EditStatusOrder from '@/components/EditStatusOrder.vue'
    import EditStatusPayout from '@/components/EditStatusPayout.vue'
    import EditConsignmentNote from '@/components/EditConsignmentNote.vue'
    import { toast } from 'bulma-toast'
    const fileDownload = require('js-file-download')

    export default {
        name: 'Order',
        components: { EditStatusOrder, EditStatusPayout, EditConsignmentNote },
        data () {
            return {
                client: {

                },
                editOrderStatusId: false,
                editPayoutStatusId: false,
                editConsignmentNote: false,

            }
        },
        mounted() {
            this.getOrder()
        },
        methods: {
            getOrder() {
                const orderID = this.$route.params.id

                axios
                    .get(`/api/v1/orders/${orderID}`)
                    .then(response => {
                        this.client = response.data
                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })
            },

            UpdatedStatusOrder() {

                const orderID = this.$route.params.id


                this.timer = setTimeout(() => {
                    this.editOrderStatusId = !this.editOrderStatusId

                    axios
                        .get(`/api/v1/orders/${orderID}`)
                        .then(response => {
                            this.client.order_status_id = response.data['order_status_id']


                        })

                        .catch(error => {
                            console.log(JSON.stringify(error))
                        })
                }, 100)
            },

            UpdatedStatusPayout() {

                const orderID = this.$route.params.id


                this.timer = setTimeout(() => {
                    this.editPayoutStatusId = !this.editPayoutStatusId

                    axios

                        .get(`/api/v1/orders/${orderID}`)
                        .then(response => {
                            this.client.payout_status_id = response.data['payout_status_id']

                        })
                        .catch(error => {
                            console.log(JSON.stringify(error))
                        })

                }, 100)

            },

            UpdatedConsignmentNote() {

                const orderID = this.$route.params.id


                this.timer = setTimeout(() => {
                    this.editConsignmentNote = !this.editConsignmentNote

                    axios

                        .get(`/api/v1/orders/${orderID}`)
                        .then(response => {
                            this.client.consignment_note = response.data['consignment_note']
                            this.client.order_status_id = response.data['order_status_id']

                        })
                        .catch(error => {
                            console.log(JSON.stringify(error))
                        })

                }, 100)

            },

            hideEditStatusOrder() {
                this.editOrderStatusId = !this.editOrderStatusId
            },
            hideEditStatusPayout() {
                this.editPayoutStatusId = !this.editPayoutStatusId
            },
            hideEditConsignmentNote() {
                this.editConsignmentNote = !this.editConsignmentNote
            },
            getPdf() {
                const order_id = this.$route.params.id

                axios
                    .get(`/api/v1/order/${order_id}/generate_pdf_only`, {
                        responseType: 'blob',
                    })
                    .then(response => {
                        fileDownload(response.data, `order_${order_id}.pdf`);
                    })
                    .catch(error => {
                        console.log(error);
                    })
            },

            deleteOrder() {
                const order_id = this.$route.params.id

                axios
                    .delete(`/api/v1/orders/${order_id}`)
                    .then(response => {
                        toast({
                            message: 'Заказ успешно удален!',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 3000,
                            position: 'bottom-right',
                        })

                        this.$router.push('/dashboard/orders')
                    })
                    .catch(error => {
                        console.log(error);
                    })

            }
        }
    }
</script>