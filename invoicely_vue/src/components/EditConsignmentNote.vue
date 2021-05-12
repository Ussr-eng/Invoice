<template>

    <div class="columns">
        <div class="column is-6">
            <div class="field">
                <label>ТТН:</label>
                <div class="control">
                    <input type="number" placeholder="введите ТТН заказа" class="input is-rounded" v-model="ttn.consignment_note">
                </div>
            </div>
        </div>

        <div class="column is-4 mt-5">
            <div class="field">
                <button class="button is-success is-rounded" @click="submitForm">Добавить</button>
            </div>
        </div>
    </div>

</template>

<script>

    import axios from 'axios'
    import { toast } from 'bulma-toast'

    export default {
        name: 'EditConsignmentNote',
        data() {
            return {
                ttn: {

                }
            }
        },
        methods: {
            submitForm() {

                this.$emit('updated')

                axios
                    .post(`/api/v1/orders/${this.$route.params.id}/edit_consignment_note/`, this.ttn)
                    .then(response => {


                        toast({
                            message: 'ТТН успешно добавлен',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 3300,
                            position: 'bottom-right',
                        })
                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })

            }
        }
    }

</script>