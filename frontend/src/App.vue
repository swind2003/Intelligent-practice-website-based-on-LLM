<script>
// 根组件定义
export default {
  name: 'App'
}
</script>

<template>
  <!-- 路由视图出口 - 根据当前路由显示对应的组件 -->
  <router-view></router-view>
</template>

<style>
/* 全局样式重置 - 移除默认边距和设置盒模型 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 根元素和body样式 - 确保页面占满整个视口 */
html, body {
  width: 100%;
  height: 100%;
}
</style>
