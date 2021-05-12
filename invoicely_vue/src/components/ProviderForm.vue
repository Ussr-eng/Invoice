<template>
    <div class="columns">
        <div class="column is-4">
            <div class="field">
                <label>Название товара:</label>
                <div class="control">
                    <input type="text" class="input is-rounded" v-model="product.title">
                </div>
            </div>
        </div>

        <div class="column is-4">
            <div class="field">
                <label>Дроп цена:</label>
                <div class="control">
                    <input type="number" class="input is-rounded" v-model="product.drop_price">
                </div>
            </div>
        </div>

        <div class="column is-4">
            <div class="field">
                <label>Розничная цена:</label>
                <div class="control">
                    <input type="number" class="input is-rounded" v-model="product.sale_price">
                </div>
            </div>
        </div>
    </div>

</template>

<script>

    export default {
        name: 'ProviderForm',
        props: {
            initialProduct: Object
        },
        data() {
            return {
                product: this.initialProduct
            }
        },
    }

</script>