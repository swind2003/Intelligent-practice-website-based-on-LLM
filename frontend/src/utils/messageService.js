import { createApp, h } from 'vue';
import MessageNotification from '@/components/MessageNotification.vue';

// 创建一个消息服务实例
const MessageService = {
  // 存储消息实例和应用实例
  instance: null,
  app: null,
  
  // 初始化消息组件
  init() {
    // 创建消息容器
    const mountNode = document.createElement('div');
    document.body.appendChild(mountNode);
    
    // 创建应用实例
    this.app = createApp({
      data() {
        return {
          message: '',
          type: 'info',
          show: false,
          duration: 3000
        };
      },
      render() {
        // 渲染消息组件
        return h(MessageNotification, {
          message: this.message,
          type: this.type,
          show: this.show,
          duration: this.duration,
          onClose: () => {
            this.show = false;
          }
        });
      }
    });
    
    // 挂载应用
    this.instance = this.app.mount(mountNode);
  },
  
  // 显示消息
  show(message, type = 'info', duration = 3000) {
    // 如果实例不存在，则初始化
    if (!this.instance) {
      this.init();
    }
    
    // 设置消息内容和类型
    this.instance.message = message;
    this.instance.type = type;
    this.instance.duration = duration;
    
    // 显示消息
    this.instance.show = true;
    
    // 返回一个Promise，在消息关闭后解析
    return new Promise(resolve => {
      setTimeout(() => {
        resolve();
      }, duration);
    });
  },
  
  // 成功消息
  success(message, duration) {
    return this.show(message, 'success', duration);
  },
  
  // 错误消息
  error(message, duration) {
    return this.show(message, 'error', duration);
  },
  
  // 警告消息
  warning(message, duration) {
    return this.show(message, 'warning', duration);
  },
  
  // 信息消息
  info(message, duration) {
    return this.show(message, 'info', duration);
  }
};

// 导出消息服务
export default MessageService;

// 安装到Vue上
export const installMessageService = {
  install(app) {
    // 将消息服务挂载到app全局属性上
    app.config.globalProperties.$message = {
      show: MessageService.show.bind(MessageService),
      success: MessageService.success.bind(MessageService),
      error: MessageService.error.bind(MessageService),
      warning: MessageService.warning.bind(MessageService),
      info: MessageService.info.bind(MessageService)
    };
  }
}; 