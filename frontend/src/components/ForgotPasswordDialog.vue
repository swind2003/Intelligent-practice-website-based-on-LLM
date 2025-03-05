<template>
  <!-- 对话框过渡动画包装器 -->
  <Transition name="dialog">
    <!-- 找回密码对话框遮罩层，点击空白处关闭对话框 -->
    <div class="forgot-overlay" v-if="visible" @click.self="closeDialog">
      <!-- 找回密码对话框主体 -->
      <div class="forgot-dialog">
        <!-- 对话框头部区域 -->
        <div class="dialog-header">
          <!-- 标题 -->
          <h2>找回密码</h2>
          <!-- 关闭按钮 -->
          <button class="close-btn" @click="closeDialog">×</button>
        </div>
        
        <!-- 对话框内容区域 -->
        <div class="dialog-body">
          <!-- 邮箱输入框组 -->
          <div class="input-item">
            <!-- 邮箱输入框 -->
            <input 
              type="email" 
              v-model="formData.email"
              placeholder="请输入注册邮箱"
              @focus="handleFocus"
              @blur="handleBlur"
            >
            <!-- 邮箱图标 -->
            <img src="../assets/email.png" alt="email" class="icon email-icon">
          </div>

          <!-- 验证码输入框组 -->
          <div class="input-item verification">
            <!-- 验证码输入容器 -->
            <div class="verification-container">
              <!-- 验证码输入框 -->
              <input 
                type="text" 
                v-model="formData.verificationCode"
                placeholder="请输入验证码"
                @focus="handleFocus"
                @blur="handleBlur"
              >
              <!-- 验证码图标 -->
              <img src="../assets/verify.png" alt="verify" class="icon verify-icon">
              <!-- 获取验证码按钮 -->
              <button 
                class="verify-btn"
                @click="sendVerificationCode"
                :disabled="cooldown > 0"
              >
                {{ cooldown > 0 ? `${cooldown}s` : '获取验证码' }}
              </button>
            </div>
          </div>

          <!-- 新密码输入框组 -->
          <div class="input-item">
            <!-- 新密码输入框 -->
            <input 
              type="password" 
              v-model="formData.newPassword"
              placeholder="新密码(8-16位字母与数字组合密码)"
              @focus="handleFocus"
              @blur="handleBlur"
            >
            <!-- 新密码图标 -->
            <img src="../assets/passport.png" alt="password" class="icon password-icon">
          </div>

          <!-- 确认新密码输入框组 -->
          <div class="input-item">
            <!-- 确认新密码输入框 -->
            <input 
              type="password" 
              v-model="formData.confirmPassword"
              placeholder="请再次输入新密码"
              @focus="handleFocus"
              @blur="handleBlur"
            >
            <!-- 确认新密码图标 -->
            <img src="../assets/confirm.png" alt="password" class="icon password-icon">
          </div>

          <!-- 重置密码按钮 -->
          <button class="reset-btn" @click="handleReset">重置密码</button>
        </div>
      </div>
    </div>
  </Transition>
  <!-- 消息提示弹窗 -->
  <MessageDialog 
    v-model:visible="showMessage"
    :title="messageConfig.title"
    :message="messageConfig.message"
    @confirm="handleMessageConfirm"
  />
</template>

<script>
import Axios from 'axios'
import CryptoJS from 'crypto-js'
import MessageDialog from './MessageDialog.vue'

// 创建一个 Axios 实例，配置基础URL
const api = Axios.create({
  baseURL: 'http://127.0.0.1:5000'
});

export default {
  // 组件名称
  name: 'ForgotPasswordDialog',

  // 组件属性定义
  props: {
    // 控制对话框显示/隐藏的属性
    visible: {
      type: Boolean,
      default: false
    }
  },

  // 组件数据
  data() {
    return {
      // 表单数据对象
      formData: {
        // 邮箱
        email: '',
        // 验证码
        verificationCode: '',
        // 新密码
        newPassword: '',
        // 确认新密码
        confirmPassword: ''
      },
      // 验证码倒计时
      cooldown: 0,
      // 输入框焦点状态
      isInputFocused: false,
      // 当前获得焦点的输入框数量
      focusCount: 0,
      // 控制消息提示弹窗显示
      showMessage: false,
      // 消息对话框配置
      messageConfig: {
        title: '操作成功',
        message: '密码重置成功!',
        type: 'success'
      }
    }
  },

  // 组件方法
  methods: {
    // 关闭对话框
    closeDialog() {
      this.$emit('update:visible', false)
    },

    // 处理输入框获得焦点
    handleFocus() {
      this.focusCount++
      this.isInputFocused = true
    },

    // 处理输入框失去焦点
    handleBlur() {
      this.focusCount--
      if (this.focusCount === 0) {
        this.isInputFocused = false
      }
    },

    // 发送验证码
    async sendVerificationCode() {
      // 验证邮箱格式 (前端基本验证)
      if (!this.validateEmail()) {
        this.showErrorMessage('邮箱格式错误', '请输入有效的邮箱地址');
        return;
      }
      
      try {
        // 创建FormData对象
        const formData = new FormData();
        formData.append('user_mail', this.formData.email);
        
        // 调用发送验证码API
        const response = await api.post('/send_email/', formData);
        
        if (response.data.code === 200) {
          // 显示发送成功提示,由于不能关闭对话框，所以类型为error
          this.showErrorMessage('验证码已发送', '请查看您的邮箱', 'error');
          
          // 启动倒计时
          this.cooldown = 60;
          const timer = setInterval(() => {
            this.cooldown--;
            if (this.cooldown <= 0) {
              clearInterval(timer);
            }
          }, 1000);
        } else {
          // 显示后端返回的错误信息
          this.showErrorMessage('发送失败', response.data.message);
        }
      } catch (error) {
        console.error('发送验证码出错:', error);
        // 网络错误或其他异常
        this.showErrorMessage('发送失败', '未知错误');
      }
    },
    
    // 验证邮箱格式
    validateEmail() {
      const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
      return emailRegex.test(this.formData.email);
    },
    
    // 验证密码格式
    validatePassword() {
      // 8-16位字母与数字组合
      const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,16}$/;
      return passwordRegex.test(this.formData.newPassword);
    },
    
    // 验证两次密码是否一致
    validatePasswordsMatch() {
      return this.formData.newPassword === this.formData.confirmPassword;
    },
    
    // 处理消息对话框确认
    handleMessageConfirm() {
      // 关闭消息对话框
      this.showMessage = false;
      
      // 只有在成功消息时才关闭忘记密码窗口
      if (this.messageConfig.type === 'success') {
        // 清空表单数据
        this.resetFormData();
        this.closeDialog();
      }
    },
    
    // 重置表单数据
    resetFormData() {
      this.formData = {
        email: '',
        verificationCode: '',
        newPassword: '',
        confirmPassword: ''
      };
    },
    
    // 显示错误消息
    showErrorMessage(title, message, type = 'error') {
      this.messageConfig = {
        title: title,
        message: message,
        type: type
      };
      this.showMessage = true;
    },

    // 密码加密方法
    encryptPassword(password) {
      return CryptoJS.SHA256(password).toString();
    },

    // 处理重置密码
    async handleReset() {
      // 1. 验证表单数据完整性 (前端基本验证)
      if (!this.formData.email || !this.formData.verificationCode || 
          !this.formData.newPassword || !this.formData.confirmPassword) {
        this.showErrorMessage('信息不完整', '请填写所有必填项');
        return;
      }
      
      // 2. 验证邮箱格式 (前端基本验证)
      if (!this.validateEmail()) {
        this.showErrorMessage('邮箱格式错误', '请输入有效的邮箱地址');
        return;
      }
      
      // 3. 验证密码格式 (前端基本验证)
      if (!this.validatePassword()) {
        this.showErrorMessage('密码格式错误', '密码必须为8-16位字母与数字组合');
        return;
      }
      
      // 4. 验证两次密码是否一致 (前端基本验证)
      if (!this.validatePasswordsMatch()) {
        this.showErrorMessage('密码不一致', '两次输入的密码不一致，请重新输入');
        return;
      }
      
      try {
        // 创建FormData对象
        const formData = new FormData();
        formData.append('user_mail', this.formData.email);
        formData.append('verification_code', this.formData.verificationCode);
        // 加密密码后再发送
        const encryptedPassword = this.encryptPassword(this.formData.newPassword);
        formData.append('new_password', encryptedPassword);
        
        // 调用重置密码API
        const response = await api.post('/reset_password/', formData);
        
        if (response.data.code === 200) {
          // 重置成功
          this.messageConfig = {
            title: '密码重置成功',
            message: response.data.message,
            type: 'success'
          };
          this.showMessage = true;
        } else {
          // 显示后端返回的错误信息
          this.showErrorMessage('重置失败', response.data.message);
        }
      } catch (error) {
        console.error('重置密码出错:', error);
        // 网络错误或其他异常
        this.showErrorMessage('重置失败', '未知错误');
      }
    }
  },

  components: {
    MessageDialog
  }
}
</script>

<style scoped>
/* 动画效果相关样式 */
.dialog-enter-active,
.dialog-leave-active {
  /* 设置所有属性的过渡动画为0.3秒，使用ease缓动函数 */
  transition: all 0.3s ease;
}

/* 定义对话框进入和离开时的初始/结束状态 */
.dialog-enter-from,
.dialog-leave-to {
  /* 设置透明度为0，实现淡入淡出效果 */
  opacity: 0;
  /* 设置初始缩放比例为0.8，实现缩放效果 */
  transform: scale(0.8);
}

/* 遮罩层样式 */
.forgot-overlay {
  /* 固定定位，覆盖整个视口 */
  position: fixed;
  /* 顶部对齐 */
  top: 0;
  /* 左侧对齐 */
  left: 0;
  /* 宽度铺满 */
  width: 100%;
  /* 高度铺满 */
  height: 100%;
  /* 半透明黑色背景 */
  background: rgba(22, 20, 77, 0.7);
  /* 背景模糊效果 */
  backdrop-filter: blur(5px);
  /* 弹性布局 */
  display: flex;
  /* 水平居中 */
  justify-content: center;
  /* 垂直居中 */
  align-items: center;
  /* 确保遮罩层在最上层 */
  z-index: 1000;
  /* 添加圆角 */
  border-radius: 20px;
}

/* 找回密码对话框主体样式 */
.forgot-dialog {
  /* 设置对话框宽度 */
  width: 400px;
  /* 内边距 */
  padding: 30px;
  /* 渐变背景 */
  background: linear-gradient(to bottom, rgba(50, 68, 141, 1), rgba(140, 196, 250, 0.3));
  /* 圆角边框 */
  border-radius: 20px;
  /* 阴影效果 */
  box-shadow: 0 8px 32px rgba(0, 14, 66, 0.35);
  /* 边框样式 */
  border: 2px solid rgba(161, 176, 235, 0.8);
  /* 变换原点居中 */
  transform-origin: center;
  /* 显示动画 */
  animation: dialogShow 0.3s ease;
}

/* 定义对话框显示动画 */
@keyframes dialogShow {
  from {
    /* 初始透明 */
    opacity: 0;
    /* 初始缩小 */
    transform: scale(0.8);
  }
  to {
    /* 最终不透明 */
    opacity: 1;
    /* 最终原始大小 */
    transform: scale(1);
  }
}

/* 对话框头部布局 */
.dialog-header {
  /* 弹性布局 */
  display: flex;
  /* 两端对齐 */
  justify-content: space-between;
  /* 垂直居中 */
  align-items: center;
  /* 底部间距 */
  margin-bottom: 30px;
}

/* 对话框标题样式 */
.dialog-header h2 {
  /* 移除默认外边距 */
  margin: 0;
  /* 字体大小 */
  font-size: 24px;
  /* 文字颜色 */
  color: rgb(244, 236, 184);
  /* 文字阴影 */
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* 关闭按钮基础样式 */
.close-btn {
  /* 移除背景 */
  background: none;
  /* 移除边框 */
  border: none;
  /* 字体大小 */
  font-size: 28px;
  /* 鼠标指针样式 */
  cursor: pointer;
  /* 按钮颜色 */
  color: rgb(244, 236, 184);
  /* 过渡动画 */
  transition: all 0.3s ease;
}

/* 关闭按钮悬停效果 */
.close-btn:hover {
  /* 旋转90度 */
  transform: rotate(90deg);
  /* 悬停时的颜色 */
  color: rgb(231, 218, 133);
}

/* 输入框容器样式 */
.input-item {
  /* 相对定位，用于图标定位 */
  position: relative;
  /* 底部间距 */
  margin-bottom: 25px;
}

/* 输入框基础样式 */
.input-item input {
  /* 宽度铺满 */
  width: 100%;
  /* 内边距，右侧留出图标空间 */
  padding: 12px 40px 12px 15px;
  /* 边框样式 */
  border: 2px solid rgba(224, 224, 224, 0.5);
  /* 圆角 */
  border-radius: 8px;
  /* 字体大小 */
  font-size: 16px;
  /* 移除焦点轮廓 */
  outline: none;
  /* 半透明白色背景 */
  background: rgba(255, 255, 255, 0.9);
  /* 过渡动画 */
  transition: all 0.3s ease;
  /* 添加右侧内边距，为图标留出空间 */
  padding-right: 40px !important;
}

/* 输入框焦点状态样式 */
.input-item input:focus {
  /* 焦点时的边框颜色 */
  border-color: #52bfc7;
  /* 焦点时的阴影效果 */
  box-shadow: 0 0 10px rgba(82, 191, 199, 0.3);
}

/* 验证码区域布局 */
.verification-container {
  /* 弹性布局 */
  display: flex;
  /* 元素间距 */
  gap: 10px;
}

/* 验证码输入框样式 */
.verification-container input {
  /* 占据剩余空间 */
  flex: 1;
}

/* 验证按钮基础样式 */
.verify-btn {
  /* 水平内边距 */
  padding: 0 15px;
  /* 背景色 */
  background: rgb(106, 132, 212);
  /* 文字颜色 */
  color: rgb(244, 236, 184);
  /* 移除边框 */
  border: none;
  /* 圆角 */
  border-radius: 8px;
  /* 鼠标指针样式 */
  cursor: pointer;
  /* 文字不换行 */
  white-space: nowrap;
  /* 过渡动画 */
  transition: all 0.3s ease;
}

/* 验证按钮悬停效果 */
.verify-btn:not(:disabled):hover {
  /* 悬停时的背景色 */
  background: #3b5998;
  /* 微微上浮 */
  transform: translateY(-1px);
}

/* 验证按钮禁用状态 */
.verify-btn:disabled {
  /* 禁用时的背景色 */
  background: rgba(106, 132, 212, 0.5);
  /* 禁用时的鼠标指针 */
  cursor: not-allowed;
}

/* 图标基础样式 */
.icon {
  /* 绝对定位 */
  position: absolute;
  /* 右侧距离 */
  right: 15px;
  /* 垂直居中 */
  top: 50%;
  /* 精确垂直居中 */
  transform: translateY(-50%);
  /* 图标宽度 */
  width: 24px;
  /* 图标高度 */
  height: 24px;
  /* 透明度 */
  opacity: 0.8;
  /* 过渡动画 */
  transition: all 0.3s ease;
  /* 验证码图标位置调整 */
  &.verify-icon {
    right: calc(100px + 20px);
    /* 添加过渡效果 */
    transition: right 0.3s ease;
  }
}

/* 禁用状态下验证码图标位置调整 */
.verification-container:has(button:disabled) .verify-icon {
  right: calc(55px + 20px);
}

/* 图标悬停效果 */
.icon:hover {
  /* 上移动画 */
  transform: translateY(-8px);
  /* 完全不透明 */
  opacity: 1;
}

/* 输入框焦点时图标效果 */
.input-item input:focus ~ .icon {
  /* 上移并放大 */
  transform: translateY(-12px) scale(1.2);
  /* 完全不透明 */
  opacity: 1;
}

/* 重置按钮基础样式 */
.reset-btn {
  /* 宽度铺满 */
  width: 100%;
  /* 按钮高度 */
  height: 50px;
  /* 内边距 */
  padding: 12px;
  /* 背景色 */
  background: rgb(106, 132, 212);
  /* 文字颜色 */
  color: rgb(244, 236, 184);
  /* 移除边框 */
  border: none;
  /* 圆角 */
  border-radius: 8px;
  /* 字体大小 */
  font-size: 16px;
  /* 字体粗细 */
  font-weight: 500;
  /* 鼠标指针样式 */
  cursor: pointer;
  /* 过渡动画 */
  transition: all 0.3s ease;
  /* 阴影效果 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  /* 文字阴影 */
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* 重置按钮悬停效果 */
.reset-btn:hover {
  /* 悬停时的背景色 */
  background: #3b5998;
  /* 增强阴影 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  /* 微微上浮 */
  transform: translateY(-1px);
  /* 增加亮度 */
  filter: brightness(1.1);
}

/* 占位符文本样式 */
::placeholder {
  /* 占位符文字颜色 */
  color: #999;
}

/* 自动填充输入框背景样式 */
input:-webkit-autofill {
  /* 覆盖浏览器默认的自动填充背景色 */
  -webkit-box-shadow: 0 0 0 30px white inset;
}
</style> 