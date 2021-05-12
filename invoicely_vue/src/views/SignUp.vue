<template>
        <div class="page-signup">
            <section class="hero is-fullheight is-light-grey is-bold">
                <div class="container">

                    <div class="animated preFadeInLeft fadeInLeft">
                        <div class="auth-card">
                            <div class="auth-card-header header-primary">
                                <h1 class="has-text-centered">Созданние аккаунта</h1>
                            </div>

                            <form @submit.prevent="submitForm">
                                <div class="field">
                                    <label>Адрес эл. почты</label>
                                    <div class="control">
                                        <input type="email" name="username" class="input" v-model="username">
                                    </div>
                                </div>

                                <div class="field">
                                    <label>Пароль</label>
                                    <div class="control">
                                        <input type="password" name="password" class="input" v-model="password">
                                    </div>
                                </div>

                                <div class="notification is-danger" v-if="errors.length">
                                    <p
                                        v-for="error in errors"
                                        v-bind:key="error"
                                    >
                                        {{ error }}
                                    </p>
                                </div>

                                <div class="field">
                                    <div class="control">
                                        <button class="button is-success">Продолжить</button>
                                    </div>
                                </div>
                            </form>

                            <hr>

                            <router-link to="/log-in">Нажмите здесь</router-link> если у вас уже есть аккаунт!
                        </div>
                    </div>
                </div>
            </section>
        </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'

export default {
    name: 'SignUp',
    data () {
        return {
            username: '',
            password: '',
            errors: []
        }
    },
    methods: {
        submitForm(e) {
            const formData = {
                username: this.username,
                password: this.password,
            }

            axios
                .post("/api/v1/users/", formData)
                .then(response => {
                    toast({
                            message: 'Аккаунт успешно создан! Введите повторно данные',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 4000,
                            position: 'bottom-right',
                        })

                    this.$router.push('/log-in')
                })
                .catch(error => {
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.errors.push(`${property}: ${error.response.data[property]}`)
                        }

                        console.log(JSON.stringify(error.response.data))
                    } else if (error.message) {
                        console.log(JSON.stringify(error.message))
                    } else {
                        console.log(JSON.stringify(error))
                    }
                })
        }
    }
}
</script>
