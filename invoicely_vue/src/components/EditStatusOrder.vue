<template>
    <div class="columns">
        <div class="column is-6">
            <label>Статус:</label>
            <div class="select is-rounded">
                <select name="order_status_id" v-model="order.order_status_id">
                    <option value="" selected>Виберете новый статус заказа</option>
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


        <div class="column is-4 mt-5">
            <div class="field">
                <button class="button is-success is-rounded" @click="submitForm">Изменить</button>
            </div>
        </div>
    </div>


</template>

<script>

    import axios from 'axios'
    import { toast } from 'bulma-toast'

    export default {
        name: 'EditStatusOrder',
        data() {
            return {
                order: {
                    order_status_id: ''
                },
                order_status: [],
            }
        },
        async mounted() {
            await this.getStatus()
        },
        methods: {
            getStatus() {

                axios
                    .get('/api/v1/order_status/')
                    .then(response => {
                        this.order_status = response.data
                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })

            },
            submitForm () {

                this.$emit('updated')
                const orderID = this.$route.params.id
                this.order.order_status_id = this.order.order_status_id.id

                axios
                    .patch(`/api/v1/orders/${orderID}/`, this.order)
                    .then(response => {
                        toast({
                            message: 'Статус заказа успешно изменен',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 3300,
                            position: 'bottom-right',
                        })
                    })
            }

        },

    }

</script>