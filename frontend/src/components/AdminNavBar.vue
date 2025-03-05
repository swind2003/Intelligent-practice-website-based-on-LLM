<template>
  <div class="admin-navbar">
    <!-- 顶部标题区域 -->
    <div class="navbar-header">
      <img src="../assets/icon.png" alt="logo" class="header-logo">
      <span class="header-title">月锦鲤</span>
    </div>
    
    <!-- 分隔线 -->
    <div class="divider"></div>

    <!-- 导航菜单区域 -->
    <div class="nav-menu">
      <!-- 首页导航项 -->
      <NavItem
        label="首页"
        itemKey="home"
        :isParent="false"
        :isChildActive="activeChild === 'home'"
        :icon="HomeIcon"
        @click="handleNavClick('home')"
      />

      <!-- 学科管理导航项 -->
      <NavItem
        label="学科管理"
        itemKey="subject"
        :isParent="true"
        :hasChildren="true"
        :isParentActive="activeParent === 'subject'"
        :icon="SubjectIcon"
      >
        <template #children>
          <NavItem
            label="新增学科"
            itemKey="subject-add"
            :isChildActive="activeChild === 'subject-add'"
            @click="handleNavClick('subject-add', 'subject')"
            :icon="BuildIcon"
          />
          <NavItem
            label="编辑学科"
            itemKey="subject-edit"
            :isChildActive="activeChild === 'subject-edit'"
            @click="handleNavClick('subject-edit', 'subject')"
            :icon="EditIcon"
          />
        </template>
      </NavItem>
    </div>

    <!-- 底部用户信息浮窗 -->
    <div class="user-info-float">
      <img :src="UserIcon" alt="user" class="user-icon">
      <span class="user-text">{{ userType }}: {{ userMail.split('@')[0] }}</span>
    </div>
  </div>
</template>

<script>
import NavItem from './NavItem.vue'
import HomeIcon from '../assets/shouye.svg'
import SubjectIcon from '../assets/subject.svg'
import UserIcon from '../assets/user.svg'
import EditIcon from '../assets/edit.svg'
import BuildIcon from '../assets/build.svg'

export default {
  name: 'AdminNavBar',
  
  components: {
    NavItem
  },

  props: {
    // 从父组件接收当前激活的导航项
    activeNav: {
      type: String,
      default: 'home'
    }
  },

  data() {
    return {
      // 当前激活的父级导航项
      activeParent: '',
      // 当前激活的子级导航项
      activeChild: 'home',
      HomeIcon: HomeIcon,
      SubjectIcon: SubjectIcon,
      UserIcon: UserIcon,
      EditIcon: EditIcon,
      BuildIcon: BuildIcon,
      userMail: 'loading...', // 临时占位，后续从后端获取
      userType: 'loading...', // 临时占位，后续从后端获取
    }
  },

  watch: {
    // 监听父组件传递的activeNav变化
    activeNav: {
      handler(newNav) {
        // 更新内部激活状态
        this.updateActiveState(newNav);
      },
      immediate: true // 组件创建时立即执行一次
    }
  },

  mounted() {
    this.fetchUserInfo()
  },

  methods: {
    // 根据导航值更新内部激活状态
    updateActiveState(navValue) {
      // 设置当前激活的子导航项
      this.activeChild = navValue;
      
      // 根据子导航项确定父导航项
      if (navValue.startsWith('subject-')) {
        this.activeParent = 'subject';
      } else {
        this.activeParent = '';
      }
    },

    // 处理导航项点击
    handleNavClick(childKey, parentKey = null) {
      // 更新激活状态
      this.activeChild = childKey
      this.activeParent = parentKey
      
      // 向父组件发送导航状态变化的事件
      this.$emit('update-nav', childKey)
    },

    async fetchUserInfo() {
      try {
        // 从localStorage中获取登录时保存的用户信息
        const user_mail = sessionStorage.getItem('userMail');
        const user_type = parseInt(sessionStorage.getItem('userType'));

        if (user_mail && user_type) {
          this.userMail = user_mail;
          // 根据userType设置用户类型显示名称
          if (user_type === 1) {
            this.userType = '管理员';
          } else if (user_type === 2) {
            this.userType = '用户';
          } else {
            this.userType = user_type; // 使用原始值
          }
        } else {
          // 如果本地存储中没有用户信息，可能用户未登录
          console.warn('未找到用户信息，用户可能未登录');
          this.userMail = 'unknown';
          this.userType = '未知';
        }
      } catch (error) {
        console.error('获取用户信息失败:', error);
        this.userMail = 'unknown';
        this.userType = '未知';
      }
    }
  }
}
</script>

<style scoped>
/* 管理员导航栏的基本样式 */
.admin-navbar {
  /* 将导航栏固定在左侧 */
  position: fixed;
  /* 定位到左边缘 */
  left: 0;
  /* 定位到顶部 */
  top: 0;
  /* 延伸到底部 */
  bottom: 0;
  /* 设置导航栏宽度为240像素 */
  width: 240px;
  /* 设置从上到下的渐变背景色 */
  background: linear-gradient(to bottom, rgb(64, 85, 167), rgba(51, 147, 147, 0.5));
  /* 添加右侧阴影效果 */
  box-shadow: 4px 0 8px rgba(0, 14, 66, 0.25);
  /* 内容溢出时显示垂直滚动条 */
  overflow-y: auto;
  /* 确保导航栏显示在其他内容之上 */
  z-index: 1000;
  /* 设置内部填充为5像素 */
  padding: 5px;
  /* 添加边框样式 */
  border-right: 4px solid rgba(244, 236, 184, 0.3);
  /* 添加右侧边框渐变效果 */
  border-image: linear-gradient(
    to bottom,
    rgba(127, 164, 227, 0.6),
    rgba(127, 239, 247, 0.3)
  ) 1;
  /* 添加内部发光效果 */
  box-shadow: 
    4px 0 8px rgba(0, 14, 66, 0.25),
    inset 0 0 15px rgba(244, 236, 184, 0.1);
}

/* 导航栏头部区域样式 */
.navbar-header {
  /* 使用弹性布局 */
  display: flex;
  /* 垂直居中对齐 */
  align-items: center;
  /* 靠左对齐 */
  justify-content: flex-start;
  /* 设置内部填充 */
  padding: 15px 55px;
  /* 设置元素间距为4像素 */
  gap: 4px;
}

/* Logo图标样式 */
.header-logo {
  /* 设置Logo宽度为35像素 */
  width: 35px;
  /* 设置Logo高度为35像素 */
  height: 35px;
  /* 添加米黄色圆形边框 */
  border: 2px solid rgba(243, 232, 134, 0.8);
  /* 设置圆形边框 */
  border-radius: 50%;
  /* 添加平滑过渡效果 */
  transition: all 0.3s ease;
}

/* Logo悬停效果 */
.header-logo:hover {
  /* 改变边框颜色 */
  border-color: rgb(127, 239, 247);
  /* 添加旋转效果 */
  transform: rotate(7deg);
  /* 添加发光效果 */
  box-shadow: 0 0 15px rgba(255, 255, 255, 0.3);
}

/* 标题文字样式 */
.header-title {
  /* 设置字体大小为24像素 */
  font-size: 24px;
  /* 设置字体粗细为粗体 */
  font-weight: bold;
  /* 设置文字颜色为米黄色 */
  color: rgb(244, 236, 184);
  /* 添加文字阴影效果 */
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* 分隔线样式 */
.divider {
  /* 设置分隔线高度为3像素 */
  height: 3px;
  /* 设置渐变背景 */
  background: linear-gradient(
    to right,
    transparent,
    rgba(244, 236, 184, 0.5),
    transparent
  );
  /* 设置上下外边距 */
  margin: 4px 0 20px;
}

/* 导航菜单容器样式 */
.nav-menu {
  /* 使用弹性布局 */
  display: flex;
  /* 设置垂直方向排列 */
  flex-direction: column;
  /* 设置项目间距为8像素 */
  gap: 8px;
  /* 添加底部内边距，为用户信息浮窗留出空间 */
  padding-bottom: 60px;
}

/* 自定义滚动条样式 */
.admin-navbar::-webkit-scrollbar {
  /* 设置滚动条宽度为6像素 */
  width: 6px;
}

/* 滚动条轨道样式 */
.admin-navbar::-webkit-scrollbar-track {
  /* 设置轨道背景色 */
  background: rgba(0, 0, 0, 0.1);
}

/* 滚动条滑块样式 */
.admin-navbar::-webkit-scrollbar-thumb {
  /* 设置滑块背景色 */
  background: rgba(244, 236, 184, 0.3);
  /* 添加圆角效果 */
  border-radius: 3px;
}

/* 滚动条滑块悬停样式 */
.admin-navbar::-webkit-scrollbar-thumb:hover {
  /* 设置悬停时的背景色 */
  background: rgba(244, 236, 184, 0.5);
}

/* 用户信息浮窗容器 */
.user-info-float {
  /* 固定定位在导航栏底部 */
  position: fixed;
  bottom: 0;
  left: 0;
  width: 240px;
  /* 设置内边距 */
  padding: 15px 20px;
  /* 使用毛玻璃效果 */
  backdrop-filter: blur(8px);
  background: rgba(51, 123, 129, 0.7);
  /* 添加上边框 */
  border-top: 4px solid rgba(127, 239, 247, 0.5);
  /* 添加右侧边框 */
  border-right: 4px solid rgba(139, 204, 214, 0.5);
  /* 确保显示在导航项之上 */
  z-index: 1001;
  /* 使用弹性布局 */
  display: flex;
  /* 垂直居中对齐 */
  align-items: center;
  /* 水平居中对齐 */
  justify-content: center;
  gap: 8px;
  /* 添加阴影 */
  box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.1);
}

/* 用户图标样式 */
.user-icon {
  width: 24px;
  height: 24px;
  /* 设置图标颜色 */
  filter: invert(95%) sepia(8%) saturate(10%) hue-rotate(332deg) brightness(150%) contrast(100%);
  /* 添加过渡效果 */
  transition: transform 0.3s ease;
}

/* 用户图标悬停效果 */
.user-icon:hover {
  transform: scale(1.1) rotate(15deg);
}

/* 用户文本样式 */
.user-text {
  color: rgb(244, 236, 184);
  font-size: 14px;
  font-weight: 500;
  /* 文字阴影 */
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  /* 防止文本溢出 */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style> 