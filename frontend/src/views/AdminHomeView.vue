<template>
    <div class="admin-home">
        <AdminNavBar 
          @update-nav="updateNavigation" 
          :activeNav="currentNav"
        />
        <HomeWindow 
          v-if="currentNav === 'home'"
          @update-nav="updateNavigation" 
        />
        <NewSubjectWindow
          v-if="currentNav === 'subject-add'"
          @update-nav="updateNavigation"
        />
        <EditSubjectWindow
          v-if="currentNav === 'subject-edit'"
          @update-nav="updateNavigation"
        />
    </div>
</template>

<script>
import AdminNavBar from '@/components/AdminNavBar.vue'
import HomeWindow from '@/components/HomeWindow.vue'
import NewSubjectWindow from '@/components/NewSubjectWindow.vue'
import EditSubjectWindow from '@/components/EditSubjectWindow.vue'

export default {
  name: 'AdminHomeView',
  components: {
    AdminNavBar,
    HomeWindow,
    NewSubjectWindow,
    EditSubjectWindow
  },
  data() {
    return {
      currentNav: 'home'
    }
  },
  methods: {
    updateNavigation(childKey) {
      this.currentNav = childKey
    }
  },
  created() {
    document.title = '主页 | 月锦鲤'
  }
}
</script>

<style scoped>
.admin-home {
  /* 设置最小高度为视口高度 */
  min-height: 100vh;
  /* 设置背景色 */
  background-color: rgb(230, 238, 252);
  /* 添加渐变效果使背景更有层次感 */
  background-image: linear-gradient(
    135deg,
    rgb(205, 255, 250) 0%,
    rgb(225, 245, 252) 20%,
    rgb(214, 238, 254) 40%,
    rgb(205, 225, 255) 60%,
    rgba(190, 215, 252, 0.95) 80%,
    rgba(180, 210, 250, 0.9) 100%
  );
  /* 确保内容不会被导航栏遮挡 */
  padding-left: 240px;
  /* 添加微妙的内发光效果 */
  position: relative;
  overflow: hidden;
}

/* 添加柔和的光晕效果 */
.admin-home::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(
    circle at 70% 30%,
    rgba(255, 255, 255, 0.15) 0%,
    rgba(230, 240, 255, 0.08) 50%,
    transparent 100%
  );
  pointer-events: none;
}
</style> 