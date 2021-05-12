<template>

    <div class="columns is-multiline">
        <div class="column is-6">
          <section class="hero is-medium mt-6">
            <div class="hero-body has-text-centered">
                <div class="container ">
                    <h1 class="title ml-5">Вас приветствует ЛимонДроп</h1>
                    <h2 class="subtitle ">Бесплатная система учета для дропшиперов</h2>
                </div>
            </div>
           </section>
        </div>
        <div class="column is-4 has-text-right-centered">
            <img src="@/assets/Delivery_app_PNG.png">
        </div>
    </div>


<div class="container">
    <div class="columns">
        <div class="column is-11 is-offset-1">
            <div class="columns is-align-items mt-6">
                <div class="column is-8">
                    <figure class="image">
                        <img src="@/assets/Screenshot_20210512_001833.png">
                    </figure>
                </div>

                <div class="column is-3 text mb-2">
                    <h2 class="subtitle is-size-3">Автоматическая смена статусов</h2>

                    <p>Ранее вам приходилось вручную отслеживать заказы, что занимало большое количество времени. Теперь же наша система автоматически сгенерирует правильный статус.</p>
                </div>
            </div>


            <div class="columns is-align-items mt-6">

                <div class="column is-3 text">
                    <h2 class="subtitle is-size-3">Контроль прибыли и убытков </h2>

                    <p>Финансовая грамотность - важная составляющая в любом бизнесе. Одна из функций нашего сервиса позволит вам контролировать свою прибыль, проводить анализ затрат и планировать будущую деятельность.</p>
                </div>

                <div class="column is-8">

                        <img src="@/assets/Screenshot_20210512_002237.png">
                </div>
            </div>

            <div class="columns is-align-items mt-6">
                <div class="column is-8">
                    <figure class="image">
                        <img src="@/assets/Screenshot_20210511_210956.png">
                    </figure>
                </div>

                <div class="column is-3 text mt-3">
                    <h2 class="subtitle is-size-3">Развернутая статистика</h2>

                    <p>В СРМ системе ЛимонДроп вы можете в любой момент изучить статистику ваших заказов. Например, с помощью таблицы «Статистика по поставщикам», вы увидите подробные данные по каждому поставщику, что позволит проанализировать сотрудничество с каждым из них.</p>
                </div>
            </div>



        </div>
    </div>
            <div class="columns is-align-items-center mt-6">
                <div class="column is-4 is-offset-4 has-text-centered mt-6" v-if="$store.state.isAuthenticated">
                    <h2 class="subtitle">Развивай свой бизнес вместе с ЛимонДроп!</h2>

                    <router-link :to="{ name: 'MainPage' }" class="button is-success is-large ">get started!</router-link>
                </div>
                <div class="column is-4 is-offset-4 has-text-centered mt-6" v-else>
                    <h2 class="subtitle">Развивай свой бизнес вместе с ЛимонДроп!</h2>

                    <router-link :to="{ name: 'SignUp' }" class="button is-success is-large ">get started!</router-link>
                </div>
            </div>
        </div>

</template>

<script>
export default {
  name: 'Home',
  components: {
  }
}
</script>
