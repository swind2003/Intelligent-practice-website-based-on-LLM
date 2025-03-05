<template>
  <div class="login-page">
    <!-- 背景层容器 - 包含月亮、鱼和云层 -->
    <div class="background-layers">
      <!-- 月亮背景层 - 最底层，静态背景 -->
      <div class="bg-layer moon"></div>
      <!-- 鱼背景层 - 中间层，带有游动动画 -->
      <div class="bg-layer fish"></div>
      <!-- 云背景层 - 最上层，带有飘动动画 -->
      <div class="bg-layer cloud"></div>
    </div>
    <!-- 登录框容器 - 位于右侧的登录组件 -->
    <div class="login-container">
      <LoginList />
    </div>
  </div>
</template>

<script>
// 导入登录框组件
import LoginList from '@/components/LoginList.vue'

export default {
  name: 'LoginView',
  components: {
    LoginList
  },
}
</script>

<style scoped>
/* 登录页面容器样式 */
.login-page {
  width: 100%;
  height: 100vh;
  position: relative;
  overflow: hidden;
}

/* 背景层容器样式 */
.background-layers {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

/* 背景层基础样式 */
.bg-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: 120% auto;
  background-position: 85% 30%;
  background-repeat: no-repeat;
}

/* 月亮背景层样式 */
.moon {
  background-image: url('@/assets/login_bg_moon.png');
  z-index: 1;
}

/* 鱼背景层样式及动画 */
.fish {
  background-image: url('@/assets/login_bg_fish.png');
  z-index: 2;
  animation: fishSwim 16s infinite ease-in-out;
}

/* 云背景层样式及动画 */
.cloud {
  background-image: url('@/assets/login_bg_cloud.png');
  z-index: 3;
  animation: cloudMove 16s infinite ease-in-out;
}

/* 鱼的游动动画 - 绕圆心旋转 */
@keyframes fishSwim {
  0% {
    transform: rotate(0deg) translateX(+35px) rotate(0deg);
  }
  100% {
    transform: rotate(+360deg) translateX(+35px) rotate(-360deg);
  }
}

/* 云的飘动动画 - 上下移动并放大 */
@keyframes cloudMove {
  0% {
    transform: translateY(0) scale(1);
  }
  50% {
    transform: translateY(-37px) scale(1.1);
  }
  100% {
    transform: translateY(0) scale(1);
  }
}

/* 登录框容器样式 */
.login-container {
  position: relative;
  z-index: 4;
  top: 50%;
  right: 5%;
  transform: translateY(-50%);
  display: flex;
  justify-content: flex-end;
  align-items: center;
}
</style> 