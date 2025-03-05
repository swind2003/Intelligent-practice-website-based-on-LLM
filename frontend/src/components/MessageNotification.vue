<template>
  <!-- 消息提示框 -->
  <div v-if="show" :class="['message-box', type]">
    <!-- 消息内容 -->
    <span>{{ message }}</span>
    <!-- 关闭按钮 -->
    <button class="close-btn" @click="closeMessage">×</button>
  </div>
</template>

<script>
export default {
  name: 'MessageNotification',
  props: {
    // 消息内容
    message: {
      type: String,
      default: ''
    },
    // 消息类型：'success'成功或'error'错误
    type: {
      type: String,
      default: 'success',
      validator: (value) => ['success', 'error', 'warning', 'info'].includes(value)
    },
    // 显示状态
    show: {
      type: Boolean,
      default: false
    },
    // 自动关闭时间（毫秒），设为0表示不自动关闭
    duration: {
      type: Number,
      default: 3000
    }
  },
  data() {
    return {
      // 消息自动关闭定时器
      messageTimeout: null
    }
  },
  watch: {
    // 监听显示状态变化
    show(newVal) {
      if (newVal && this.duration > 0) {
        this.startTimer();
      }
    },
    // 监听持续时间变化
    duration(val) {
      if (this.show && val > 0) {
        this.startTimer();
      }
    }
  },
  methods: {
    // 开始定时器
    startTimer() {
      // 清除之前的定时器
      if (this.messageTimeout) {
        clearTimeout(this.messageTimeout);
      }
      
      // 设置新的定时器
      if (this.duration > 0) {
        this.messageTimeout = setTimeout(() => {
          this.closeMessage();
        }, this.duration);
      }
    },
    // 关闭消息提示
    closeMessage() {
      // 清除定时器
      if (this.messageTimeout) {
        clearTimeout(this.messageTimeout);
      }
      // 触发关闭事件
      this.$emit('close');
    }
  },
  // 组件销毁前清除定时器
  beforeDestroy() {
    if (this.messageTimeout) {
      clearTimeout(this.messageTimeout);
    }
  }
}
</script>

<style scoped>
/* 消息提示框样式 */
.message-box {
  /* 固定定位 */
  position: fixed;
  /* 顶部距离 */
  top: 20px;
  /* 右侧距离 */
  right: 20px;
  /* 内边距 */
  padding: 15px 20px;
  /* 圆角边框 */
  border-radius: 6px;
  /* 阴影效果 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  /* 弹性布局 */
  display: flex;
  /* 垂直居中 */
  align-items: center;
  /* 两端对齐 */
  justify-content: space-between;
  /* 最小宽度 */
  min-width: 300px;
  /* 层级 */
  z-index: 1000;
  /* 滑入动画 */
  animation: slideIn 0.3s ease;
}

.message-box.success {
  /* 背景颜色 */
  background-color: #e6f7e6;
  /* 左侧边框 */
  border-left: 4px solid #52c41a;
  /* 字体颜色 */
  color: #52c41a;
}

.message-box.error {
  /* 背景颜色 */
  background-color: #fff1f0;
  /* 左侧边框 */
  border-left: 4px solid #f5222d;
  /* 字体颜色 */
  color: #f5222d;
}

.message-box.warning {
  /* 背景颜色 */
  background-color: #fffbe6;
  /* 左侧边框 */
  border-left: 4px solid #faad14;
  /* 字体颜色 */
  color: #faad14;
}

.message-box.info {
  /* 背景颜色 */
  background-color: #e6f4ff;
  /* 左侧边框 */
  border-left: 4px solid #1890ff;
  /* 字体颜色 */
  color: #1890ff;
}

.close-btn {
  /* 无背景 */
  background: none;
  /* 无边框 */
  border: none;
  /* 字体大小 */
  font-size: 18px;
  /* 鼠标指针样式 */
  cursor: pointer;
  /* 透明度 */
  opacity: 0.7;
  /* 过渡效果 */
  transition: opacity 0.2s;
}

.close-btn:hover {
  /* 悬停时透明度 */
  opacity: 1;
}

@keyframes slideIn {
  /* 起始状态 */
  from {
    /* 水平位移 */
    transform: translateX(100%);
    /* 透明度 */
    opacity: 0;
  }
  /* 结束状态 */
  to {
    /* 水平位移 */
    transform: translateX(0);
    /* 透明度 */
    opacity: 1;
  }
}
</style> 