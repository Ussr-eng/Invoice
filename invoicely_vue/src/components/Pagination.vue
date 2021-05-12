<template>
    <nav class="pagination is-centered" role="navigation" aria-label="pagination">
        <ul class="pagination-list">
            <li
                v-for="p in quantity_page"
                :key="p"
            >
                <a class="pagination-link" :class="{ active: currentPage === p }" @click="changePage(p)">{{p}}</a>

            </li>
        </ul>
    </nav>
</template>

<script>

    export default{
        name: "Pagination",
        props: [ 'quantity_page' ],
        data() {
            return {
                currentPage: 1
            }
        },
        methods: {
            changePage(pageNumber) {
                this.currentPage = pageNumber
                this.$emit('page-changed', pageNumber)
            }
        }
    }

</script>

<style scoped>
    .active {
        background-color: #1da1f2;
    }
</style>