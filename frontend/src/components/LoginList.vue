<template>
  <!-- 登录框主体 -->
  <div class="login-box" :class="{ 'active': isInputFocused }">
    <!-- Logo区域 -->
    <div class="logo">
      <img src="../assets/icon.png" alt="logo" />
    </div>
    
    <!-- 输入框组 -->
    <div class="input-group">
      <!-- 邮箱输入框 -->
      <div class="input-item">
        <input 
          type="text" 
          v-model="formData.email"
          placeholder="请输入邮箱"
          @focus="handleFocus"
          @blur="handleBlur"
        >
        <img src="../assets/email.png" alt="email" class="icon email-icon">
      </div>
      
      <!-- 密码输入框 -->
      <div class="input-item">
        <input 
          type="password" 
          v-model="formData.password"
          placeholder="请输入密码"
          @focus="handleFocus"
          @blur="handleBlur"
        >
        <img src="../assets/passport.png" alt="password" class="icon password-icon">
      </div>
    </div>

    <!-- 链接区域：注册和找回密码 -->
    <div class="links">
      <a href="#" class="register" @click.prevent="showRegister = true">注册账号</a>
      <a href="#" class="forgot" @click.prevent="showForgot = true">找回密码</a>
    </div>

    <!-- 登录按钮 -->
    <button class="login-btn" @click="handleLogin">登录</button>
    <RegisterDialog v-model:visible="showRegister" />
    <ForgotPasswordDialog v-model:visible="showForgot" />
    <MessageDialog 
      v-model:visible="showMessage"
      :title="messageConfig.title"
      :message="messageConfig.message"
      @confirm="handleMessageConfirm"
    />
  </div>
</template>

<script>
import RegisterDialog from './RegisterDialog.vue'
import ForgotPasswordDialog from './ForgotPasswordDialog.vue'
import MessageDialog from './MessageDialog.vue'
import Axios from 'axios'
import CryptoJS from 'crypto-js'

// 创建一个 Axios 实例，配置基础URL
const api = Axios.create({
  baseURL: 'http://127.0.0.1:5000'
});

export default {
  // 组件名称
  name: 'LoginList',
  // 先声明组件
  components: {
    RegisterDialog,
    ForgotPasswordDialog,
    MessageDialog
  },
  // 组件数据
  data() {
    return {
      // 控制输入框是否处于焦点状态
      isInputFocused: false,
      // 记录当前获得焦点的输入框数量
      focusCount: 0,
      // 控制注册对话框显示
      showRegister: false,
      // 控制忘记密码对话框显示
      showForgot: false,
      // 表单数据对象
      formData: {
        // 邮箱
        email: '',
        // 密码
        password: ''
      },
      // 控制消息提示弹窗显示
      showMessage: false,
      // 消息对话框配置
      messageConfig: {
        title: '操作提示',
        message: '',
        type: 'info'
      }
    }
  },
  // 组件方法
  methods: {
    // 处理输入框获得焦点事件
    handleFocus() {
      // 获得焦点的输入框数量加1
      this.focusCount++
      // 设置输入框为焦点状态,触发样式变化
      this.isInputFocused = true
    },
    
    // 处理输入框失去焦点事件
    handleBlur() {
      // 获得焦点的输入框数量减1
      this.focusCount--
      // 当没有输入框处于焦点状态时,取消焦点样式
      if (this.focusCount === 0) {
        this.isInputFocused = false
      }
    },
    
    // 显示消息提示
    showErrorMessage(title, message, type = 'error') {
      this.messageConfig = {
        title: title,
        message: message,
        type: type
      };
      this.showMessage = true;
    },
    
    // 处理消息对话框确认
    handleMessageConfirm() {
      // 关闭消息对话框
      this.showMessage = false;
    },
    
    // 验证邮箱格式
    validateEmail() {
      const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
      return emailRegex.test(this.formData.email);
    },
    
    // 密码加密方法
    encryptPassword(password) {
      return CryptoJS.SHA256(password).toString();
    },
    
    // 处理登录
    async handleLogin() {
      // 1. 验证表单数据完整性 (前端基本验证)
      if (!this.formData.email || !this.formData.password) {
        this.showErrorMessage('信息不完整', '请填写邮箱和密码');
        return;
      }
      
      // 2. 验证邮箱格式 (前端基本验证)
      if (!this.validateEmail()) {
        this.showErrorMessage('邮箱格式错误', '请输入有效的邮箱地址');
        return;
      }
      
      try {
        // 创建FormData对象
        const formData = new FormData();
        formData.append('user_mail', this.formData.email);
        // 加密密码后再发送
        const encryptedPassword = this.encryptPassword(this.formData.password);
        formData.append('user_password', encryptedPassword);
        
        // 调用登录API - 使用配置好的api实例
        const response = await api.post('/login/', formData);
        
        if (response.data.code === 200) {
          // 登录成功
          this.showErrorMessage('登录成功', '正在跳转...', 'success');
          
          // 临时存储用户信息到sessionStorage
          sessionStorage.setItem('userId', response.data.user_id);
          sessionStorage.setItem('userType', response.data.user_type);
          sessionStorage.setItem('userMail', response.data.user_mail);

          // 延迟跳转，等待消息关闭
          setTimeout(() => {
            // 根据用户类型跳转到不同页面
            if (response.data.user_type === 1) {
              // 管理员
              this.$router.push('/admin');
            } else {
              // 普通用户
              this.$router.push('/user');
            }
          }, 500);
        } else {
          // 登录失败，直接显示后端返回的错误信息
          this.showErrorMessage('登录失败', response.data.message);
        }
      } catch (error) {
        console.error('登录出错:', error);
        // 网络错误或其他异常
        this.showErrorMessage('登录失败', '网络错误，请稍后重试');
      }
    }
  }
}
</script>

<style scoped>
/* 登录框样式 - 设置登录框的基本样式和渐变背景 */
.login-box {
  /* 设置登录框宽度 */
  width: 400px;
  /* 设置内部填充 */
  padding: 30px;
  /* 设置渐变背景 */
  background: linear-gradient(to bottom, rgba(50, 68, 141, 1), rgba(140, 196, 250, 0.3));
  /* 设置圆角 */
  border-radius: 20px;
  /* 添加阴影效果 - 使登录框具有立体感 */
  box-shadow: 0 8px 16px rgba(0, 14, 66, 0.25);
  /* 添加描边效果 */
  border: 2px solid rgba(161, 176, 235, 0.8);
  /* 添加过渡效果 */
  transition: all 0.3s ease;
  /* 设置变形原点为中心 */
  transform-origin: center;
  /* 大小调整 */
  transform: scale(0.9);
}

/* 登录框激活状态 */
.login-box.active {
  /* 放大效果 */
  transform: scale(0.92);
  /* 设置圆角 */
  border-radius: 35px;
  /* 增强阴影效果 */
  box-shadow: 0 12px 24px rgba(0, 14, 66, 0.3);
  /* 改变边框颜色 */
  border-color: rgba(74, 203, 194, 0.8);
  /* 改变渐变背景 */
  background: linear-gradient(to bottom, rgba(50, 67, 134, 1), rgba(78, 97, 174, 0.8), rgba(150, 206, 255, 0.5));
}

/* Logo样式 - 设置Logo区域的布局 */
.logo {
  /* 居中对齐 */
  text-align: center;
  /* 设置底部间距 */
  margin-bottom: 30px;
}

/* Logo图片样式 - 设置Logo图片的尺寸和边框效果 */
.logo img {
  /* 设置图片宽度 */
  width: 100px;
  /* 设置图片高度 */
  height: 100px;
  /* 添加圆形边框 */
  border: 3px solid rgba(243, 232, 134, 0.8);
  /* 添加圆角使图片呈现为圆形 */
  border-radius: 50%;
  /* 添加过渡效果 */
  transition: all 0.3s ease;
  /* 添加阴影效果 */
  box-shadow: 0 0 15px rgba(255, 255, 255, 0.3);
}

/* Logo图片悬停效果 */
.logo img:hover {
  /* 悬停时边框颜色加深 */
  border-color: rgb(127, 239, 247);
  /* 悬停时增加阴影效果 */
  box-shadow: 0 0 25px rgba(255, 255, 255, 0.5);
  /* 悬停时稍微放大 */
  transform: scale(1.05);
  /* 添加轻微旋转效果 */
  transform: rotate(7deg);
}

/* 输入框组样式 - 设置输入框组的间距 */
.input-group {
  /* 设置底部间距 */
  margin-bottom: 30px;
}

/* 单个输入框容器样式 - 设置每个输入框的布局 */
.input-item {
  /* 设置相对定位，用于图标定位 */
  position: relative;
  /* 设置底部间距 */
  margin-bottom: 30px;
}

/* 输入框样式 - 设置输入框的外观 */
.input-item input {
  /* 设置输入框宽度 */
  width: 100%;
  /* 设置内部填充 */
  padding: 12px 40px 12px 15px;
  /* 设置边框 */
  border: 2px solid #e0e0e0;
  /* 设置圆角 */
  border-radius: 8px;
  /* 设置字体大小 */
  font-size: 16px;
  /* 移除焦点轮廓 */
  outline: none;
  /* 添加边框颜色过渡效果 - 使交互更流畅 */
  transition: border-color 0.3s;
  /* 添加右侧内边距，为图标留出空间 */
  padding-right: 40px !important;
}

/* 输入框获得焦点时的样式 - 设置输入框激活状态 */
.input-item input:focus {
  /* 设置焦点时的边框颜色 */
  border-color: #52bfc7;
}

/* 输入框图标样式 - 设置图标的位置和外观 */
.icon {
  /* 绝对定位 */
  position: absolute;
  /* 设置右侧距离 */
  right: 15px;
  /* 垂直居中 */
  top: 50%;
  /* 精确垂直居中 */
  transform: translateY(-50%);
  width: 24px;
  height: 24px;
  opacity: 0.8;
  transition: all 0.3s ease;
}

/* 图标悬停效果 */
.icon:hover {
  transform: translateY(-8px);
  opacity: 1;
}

/* 输入框获得焦点时图标效果 */
.input-item input:focus ~ .icon {
  transform: translateY(-12px) scale(1.2);
  opacity: 1;
}

/* 链接区域样式 - 设置链接区域的布局 */
.links {
  /* 使用弹性布局 */
  display: flex;
  /* 两端对齐 */
  justify-content: space-between;
  /* 设置底部间距 */
  margin-bottom: 30px;
  /* 设置左右填充 */
  padding: 0 20px;
}

/* 链接样式 - 设置链接的外观 */
.links a {
  /* 设置链接颜色 */
  color: #1b5dce;
  /* 移除下划线 */
  text-decoration: none;
  /* 设置字体大小 */
  font-size: 16px;
  /* 添加字体粗细 */
  font-weight: 500;
  /* 添加内边距使点击区域更大 */
  padding: 5px 10px;
  /* 添加圆角 */
  border-radius: 4px;
  /* 添加过渡效果 */
  transition: all 0.3s ease;
  /* 添加背景色 */
  background-color: transparent;
}

/* 链接悬停效果 - 设置鼠标悬停时的样式 */
.links a:hover {
  /* 改变背景色 */
  background-color: rgba(30, 96, 211, 0.1);
  /* 改变文字颜色 */
  color: rgb(231, 218, 133);
  /* 增加阴影效果 */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  /* 添加轻微缩放效果 */
  transform: scale(1.05);
  /* 增加亮度 */
  filter: brightness(1.1);
}

/* 登录按钮样式 - 设置按钮的外观 */
.login-btn {
  /* 设置按钮宽度为100% */
  width: 100%;
  /* 设置按钮高度 */
  height: 50px;
  /* 设置内部填充 */
  padding: 12px;
  /* 设置背景色 */
  background: rgb(106, 132, 212);
  /* 设置文字颜色 */
  color: rgb(244, 236, 184);
  /* 移除边框 */
  border: none;
  /* 设置圆角 */
  border-radius: 8px;
  /* 设置字体大小 */
  font-size: 16px;
  /* 设置字体粗细 */
  font-weight: 500;
  /* 设置鼠标指针样式 */
  cursor: pointer;
  /* 添加过渡效果 */
  transition: all 0.3s ease;
  /* 添加阴影效果 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  /* 设置文字阴影 */
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* 登录按钮悬停效果 - 设置鼠标悬停时的样式 */
.login-btn:hover {
  /* 设置悬停时的背景色 */
  background: #3b5998;
  /* 增加阴影效果 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  /* 添加轻微缩放效果 */
  transform: translateY(-1px);
  /* 增加亮度 */
  filter: brightness(1.1);
  /* 添加文字发光效果 */
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* 输入框占位符样式 - 设置占位符文字的颜色 */
::placeholder {
  /* 设置占位符颜色 */
  color: #999;
}

/* 去除输入框自动填充时的默认背景色 - 修复Chrome浏览器的自动填充样式问题 */
input:-webkit-autofill {
  /* 使用内阴影覆盖默认的黄色背景 */
  -webkit-box-shadow: 0 0 0 30px white inset;
}
</style>