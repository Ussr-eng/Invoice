<template>
    <div class="columns">
        <div class="column is-5">
            <div class="field">
                <label>Название:</label>
                <div class="control">
                    <input type="text" class="input is-rounded" placeholder="Введите новый источник заказов" v-model="source.title">
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
        name: 'CreateSourceOrder',
        data() {
            return {
                source: {}
            }
        },
        methods: {
            submitForm () {
                this.$emit('updated')
                axios
                    .post('/api/v1/source_orders/', this.source)
                    .then(response => {
                        toast({
                            message: 'Новый источник заказа успешно добавлен',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 3000,
                            position: 'bottom-right',
                        })
                    })
            }
        }
    }

</script>