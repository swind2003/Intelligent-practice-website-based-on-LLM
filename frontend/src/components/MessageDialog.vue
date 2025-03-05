<template>
  <!-- 消息弹窗过渡动画包装器 -->
  <Transition name="message-dialog">
    <div class="message-overlay" v-if="visible" @click.self="closeDialog">
      <!-- 消息弹窗主体 -->
      <div class="message-dialog">
        <!-- 弹窗头部 -->
        <div class="dialog-header">
          <!-- 标题 -->
          <h3>{{ title }}</h3>
          <!-- 关闭按钮 -->
          <button class="close-btn" @click="closeDialog">×</button>
        </div>
        
        <!-- 消息内容 -->
        <div class="message-content">
          <slot>{{ message }}</slot>
        </div>

        <!-- 按钮区域 -->
        <div class="dialog-footer">
          <button class="confirm-btn" @click="handleConfirm">{{ confirmText }}</button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script>
export default {
  name: 'MessageDialog',
  props: {
    // 控制弹窗显示/隐藏
    visible: {
      type: Boolean,
      default: false
    },
    // 弹窗标题
    title: {
      type: String,
      default: '提示'
    },
    // 消息内容
    message: {
      type: String,
      default: ''
    },
    // 确认按钮文本
    confirmText: {
      type: String,
      default: '确认'
    }
  },
  methods: {
    // 关闭弹窗
    closeDialog() {
      this.$emit('update:visible', false)
      this.$emit('close')
    },
    // 确认按钮点击处理
    handleConfirm() {
      this.$emit('confirm')
      this.closeDialog()
    }
  }
}
</script>

<style scoped>
/* 消息弹窗动画 */
.message-dialog-enter-active,
.message-dialog-leave-active {
  transition: all 0.3s ease;
}

.message-dialog-enter-from,
.message-dialog-leave-to {
  opacity: 0;
  transform: scale(0.8);
}

/* 遮罩层样式 */
.message-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(46, 43, 138, 0.7);
  backdrop-filter: blur(5px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1001;
  border-radius: 20px;
}

/* 消息弹窗主体 */
.message-dialog {
  width: 300px;
  padding: 20px;
  background: linear-gradient(to bottom, rgba(50, 68, 141, 1), rgba(140, 196, 250, 0.3));
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 14, 66, 0.35);
  border: 2px solid rgba(161, 176, 235, 0.8);
  animation: dialogShow 0.3s ease;
}

/* 弹窗头部 */
.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

/* 标题样式 */
.dialog-header h3 {
  margin: 0;
  color: rgb(244, 236, 184);
  font-size: 18px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* 关闭按钮 */
.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  color: rgb(244, 236, 184);
  cursor: pointer;
  transition: all 0.3s ease;
}

/* 关闭按钮悬停效果 */
.close-btn:hover {
  transform: rotate(90deg);
  color: rgb(231, 218, 133);
}

/* 消息内容区域 */
.message-content {
  padding: 10px 0;
  color: rgb(244, 236, 184);
  font-size: 16px;
  text-align: center;
  min-height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 按钮区域 */
.dialog-footer {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

/* 确认按钮 */
.confirm-btn {
  width: 100px;
  height: 36px;
  background: rgb(106, 132, 212);
  color: rgb(244, 236, 184);
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* 确认按钮悬停效果 */
.confirm-btn:hover {
  background: #3b5998;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transform: translateY(-1px);
  filter: brightness(1.1);
}

/* 弹窗显示动画 */
@keyframes dialogShow {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style> 