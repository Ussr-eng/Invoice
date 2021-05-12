<template>

    <div class="page-invoices">
        <nav class="breadcrumb" aria-label="breadcrumbs">
            <ul>
                <li><router-link :to="{ name: 'Dashboard' }">Dashboard</router-link></li>
                <li class="is-active"><router-link :to="{ name: 'Invoices' }" aria-current="true">Clients</router-link></li>
            </ul>
        </nav>
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Invoices</h1>
                <div class="buttons">
                    <router-link :to="{ name: 'AddInvoice' }" class="button is-success is-rounded">Add invoice</router-link>
                </div>
            </div>
            <div class="column is-12">
                <table class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Client</th>
                            <th>Amount</th>
                            <th>Due date</th>
                            <th>Is paid</th>
                            <th>Details</th>
                            <th>Delete</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr
                            v-for="invoice in invoices"
                            v-bind:key="invoice.id"
                        >
                            <td>{{ invoice.invoice_number }}</td>
                            <td>{{ invoice.client_name }}</td>
                            <td>{{ invoice.gross_amount }}</td>
                            <td>{{ invoice.get_due_date_formatted }}</td>
                            <td>{{ getStatusLabel(invoice) }}</td>
                            <td><router-link :to="{ name: 'Invoice', params: { id: invoice.id }}" class="button is-link is-outlined">Details</router-link></td>
                            <td><button v-on:click="invoiceDelete(invoice)" class="button is-danger is-outlined">Delete</button></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

</template>

<script>
    import axios from 'axios'

    export default {
        name: 'Invoices',
        data() {
            return {
                invoices: []
            }
        },
        mounted() {
            this.getInvoices()
        },
        methods: {
            getInvoices() {
                axios
                    .get('/api/v1/invoices/')
                    .then(response => {
                        for (let i = 0; i < response.data.length; i++) {
                            this.invoices.push(response.data[i])
                        }
                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })
            },
            invoiceDelete(invoice) {

                axios
                    .delete(`/api/v1/invoices/${invoice.id}`)
                    .then(response => {
                        console.log(response.data)
                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })
                this.timer = setTimeout(() => {
                    axios
                        .get('/api/v1/invoices/')
                        .then(response => {
                            if (response.data.length == 0) {
                                this.invoices = []
                            } else {
                                for (let i = 0; i < response.data.length; i++) {
                                    this.invoices = []
                                    this.invoices.push(response.data[i])
                                }
                            }

                        })
                        .catch(error => {
                            console.log(JSON.stringify(error))
                        })
                }, 300)
            },
            getStatusLabel(invoice) {
                if (invoice.is_paid) {
                    return 'Yes'
                } else {
                    return 'No'
                }
            }
        }
    }
</script>