<template>
  <div class="student-home">
    <!-- 暂时为空的学生首页容器 -->
    <h1>学生首页</h1>
  </div>
</template>

<script>
export default {
  name: 'StudentHomeView',
  created() {
    document.title = '主页 | 月锦鲤'
  }
}
</script>

<style scoped>
.student-home {
  width: 100%;
  height: 100vh;
  background: #f5f7fa;
}
</style> 