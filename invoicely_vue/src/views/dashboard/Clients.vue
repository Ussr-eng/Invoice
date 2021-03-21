<template>
    <div class="page-clients">
        <nav class="breadcrumb" aria-label="breadcrumbs">
            <ul>
                <li><router-link :to="{ name: 'Dashboard' }">Dashboard</router-link></li>
                <li class="is-active"><router-link :to="{ name: 'Clients' }" aria-current="true">Clients</router-link></li>
            </ul>
        </nav>

        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">All Clients</h1>

                <router-link :to="{ name: 'AddClient' }" class="button is-primary is-outlined mt-4">Add client</router-link>
            </div>

            <div
                class="column is-3"
                v-for="client in clients"
                v-bind:key="client.id"
            >
                <div class="box">
                    <h3 class="is-size-4 mb-4">{{ client.name }}</h3>

                    <router-link :to="{ name: 'Client', params: { id: client.id } }" class="button is-light">Details</router-link>
                    <router-link :to="{ name: 'EditClient', params: { id: client.id } }" class="button is-light ml-3">Edit</router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

    import axios from 'axios'
    export default {
        name: 'Clients',
        data() {
            return {
                clients: []
            }
        },
        mounted() {
            this.getClients()
        },
        methods: {
            getClients() {
                axios
                    .get('/api/v1/clients/')
                    .then(response => {
                        for (let i = 0; i < response.data.length; i++) {
                            this.clients.push(response.data[i])
                        }
                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })
            }
        }
    }
</script>