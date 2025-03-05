import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { installMessageService } from './utils/messageService'

const app = createApp(App)

app.use(router)
app.use(installMessageService)

app.mount('#app')
