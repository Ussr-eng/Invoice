<template>
    <div class="page-login">
        <section class="hero is-fullheight is-light-grey is-bold">
            <div class="hero-body">
                <div class="container">
                    <div class="login-form-wrapper">
                        <div class="animated preFadeInLeft fadeInLeft">
                            <div class="auth-card">
                                <div class="auth-card-header header-primary">
                                    <h1 class="has-text-centered">Log in</h1>
                                </div>

                                <form @submit.prevent="submitForm">
                                    <div class="field mb-5">
                                        <label>Username</label>
                                        <div class="control">
                                            <input type="email" name="username" class="input" v-model="username" placeholder="Username">
                                            <div class="form-icon">
                                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-user"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                                            </div>
                                        </div>
                                    </div>

                                    <div class="field">
                                        <label>Password</label>
                                        <div class="control">
                                            <input type="password" name="password" class="input" v-model="password" placeholder="Password">
                                            <div class="form-icon">
                                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-lock"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
                                            </div>
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

                                    <router-link to="/sign-up">Click here</router-link> to sign up!

                                    <div class="field">
                                        <div class="control">
                                            <button class="button is-success">Log in</button>
                                        </div>
                                    </div>


                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>


<script>
    import axios from 'axios'

    export default {
        name: 'LogIn',
        data() {
            return {
                username: '',
                password: '',
                errors: []
            }
        },
        methods: {
            async submitForm(e) {
                axios.defaults.headers.common["Authorization"] = ""

                localStorage.removeItem("token")

                const formData = {
                    username: this.username,
                    password: this.password,
                }

                await axios
                    .post("/api/v1/token/login/", formData)
                    .then(response => {

                        const token = response.data.auth_token

                        this.$store.commit('setToken', token)

                        axios.defaults.headers.common["Authorization"] = "Token " + token

                        localStorage.setItem("token", token)

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
                axios
                    .get("/api/v1/users/me")
                    .then(response => {

                        console.log(response)
                        this.$store.commit('setUser', {'username': response.data.username, 'id': response.data.id})

                        localStorage.setItem('username', response.data.username)
                        localStorage.setItem('userId', response.data.id)

                        this.$router.push('/dashboard')

                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })
            }
        }

    }
</script>