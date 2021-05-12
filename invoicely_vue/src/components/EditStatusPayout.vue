<template>
    <div class="columns">
        <div class="column is-6">
            <label>Статус:</label>
            <div class="select is-rounded">
                <select name="payout_status_id" v-model="payment.payout_status_id">
                    <option value="" selected>Виберете новый статус выплаты</option>
                    <option
                        v-for="status in payment_status"
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
        name: 'EditStatusPayout',
        data() {
            return {
                payment: {
                    payout_status_id: ''
                },
                payment_status: [],
            }
        },
        async mounted() {
            await this.getStatus()
        },
        methods: {
            getStatus() {

                axios
                    .get('/api/v1/payout_status/')
                    .then(response => {
                        this.payment_status = response.data
                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })

            },
            submitForm () {

                this.$emit('updated')
                const orderID = this.$route.params.id
                this.payment.payout_status_id = this.payment.payout_status_id.id

                axios
                    .patch(`/api/v1/orders/${orderID}/`, this.payment)
                    .then(response => {
                        toast({
                            message: 'Статус выплаты успешно изменен',
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