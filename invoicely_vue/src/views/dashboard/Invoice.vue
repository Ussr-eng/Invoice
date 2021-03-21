<template>

    <div class="page-invoices">
        <nav class="breadcrumb" aria-label="breadcrumbs">
            <ul>
                <li><router-link :to="{ name: 'Dashboard' }">Dashboard</router-link></li>
                <li><router-link :to="{ name: 'Invoices' }">Clients</router-link></li>
                <li class="is-active"><router-link :to="{ name: 'Invoice', params: { id: invoice.id } }" aria-current="true">{{ invoice.client_name }}</router-link></li>
            </ul>
        </nav>
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Invoice - {{ invoice.invoice_number }}</h1>



                <button @click="getPdf()" class="button is-link is-outlined">Download PDF</button>
            </div>

            <div class="column is-4 mb-4">
                <div class="box">

                    <h3 class="is-size-4 mb-4">Client</h3>

                    <p><strong>{{ invoice.client_name }}</strong></p>

                    <p v-if="invoice.client_address1">{{ invoice.client_address1 }}</p>
                    <p v-if="invoice.client_address2">{{ invoice.client_address2 }}</p>
                    <p v-if="invoice.client_zipcode || invoice.client_place">{{ invoice.client_zipcode }} {{ invoice.client_place }}</p>
                    <p v-if="invoice.client_country">{{ invoice.client_country }}</p>
                </div>
            </div>

            <div class="column is-9">
                <h3 class="is-size-4 mb-4">Items</h3>
                <div class="table-container">
                    <table class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth">
                        <thead>
                            <tr>
                                <th>title</th>
                                <th>quantity</th>
                                <th>vat rate</th>
                                <th>total</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr
                                v-for="item in items"
                                v-bind:key="item.id"
                            >
                                <td>{{ item.title }}</td>
                                <td>{{ item.quantity }}</td>
                                <td>{{ item.vat_rate }}%</td>
                                <td>{{ getItemTotal(item) }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="column is-6">
                <div class="box">
                    <h3 class="is-size-4 mb-5">Summary</h3>

                    <div class="columns">
                        <div class="column is-6">
                            <p><strong>Net amount</strong>: {{ invoice.net_amount }}</p>
                            <p><strong>Vat amount</strong>: {{ invoice.vat_amount }}</p>
                            <p><strong>Gross amount</strong>: {{ invoice.gross_amount }}</p>
                            <p><strong>Bank account</strong>: {{ invoice.bankaccount }}</p>
                        </div>

                        <div class="column is-6">
                            <p><strong>Our reference</strong>: {{ invoice.sender_reference }}</p>
                            <p><strong>Client reference</strong>: {{ invoice.client_contact_reference }}</p>
                            <p><strong>Due date</strong>: {{ invoice.get_due_date_formatted }}</p>
                            <p><strong>Status</strong>: {{ getStatusLabel() }}</p>
                            <p><strong>Invoice type</strong>: {{ getInvoiceType() }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>


</template>

<script>

    import axios from 'axios'

    const fileDownload = require('js-file-download')

    export default {
        name: 'Invoice',
        data() {
            return {
                invoice: {},
                items: []
            }
        },
        async mounted () {
            await this.getInvoice()
            await this.getItems()
        },
        methods: {
            getInvoice() {
                const invoiceId = this.$route.params.id
                console.log(invoiceId)

                axios
                    .get(`/api/v1/invoices/${invoiceId}`)
                    .then(response => {
                        console.log(response)
                        this.invoice = response.data
                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })
            },
            getItems() {
                const invoiceId = this.$route.params.id

                axios
                    .get(`/api/v1/items/?invoice_id=${invoiceId}`)
                    .then(response => {
                        this.items = response.data
                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })
            },
            getPdf() {
                const invoiceId = this.$route.params.id

                axios
                    .get(`/api/v1/invoices/${invoiceId}/generate_pdf`, {
                        responseType: 'blob',
                    }).then(response => {
                        fileDownload(response.data, `invoice_${invoiceId}.pdf`);
                    }).catch(error => {
                        console.log(error);
                    })
            },
            getStatusLabel() {
                if (this.invoice.is_paid) {
                    return 'Is paid'
                } else {
                    return 'Is not paid'
                }
            },
            getInvoiceType() {
                if (this.invoice.invoice_type === 'credit_note') {
                    return 'Credit note'
                } else {
                    return 'Invoice'
                }
            },
            getItemTotal(item) {
                const unit_price = item.unit_price
                const quantity = item.quantity

                const total = item.net_amount + (item.net_amount * (item.vat_rate/100))

                return parseFloat(total).toFixed(1)
            }
        }
    }

</script>