<template>
  <div class="edit-subject-window">
    <!-- 页面头部区域 -->
    <div class="header">
      <!-- 标题 -->
      <h1 class="title">编辑学科</h1>
      <!-- 描述文本 -->
      <div class="description">在此页面搜索并管理已有学科</div>
    </div>

    <!-- 搜索区域 -->
    <div class="search-container" :class="{ 'active': searchCompleted }">
      <div class="search-box" :class="{ 'active': searchCompleted }">
        <!-- 应用图标 -->
        <img src="../assets/icon.png" alt="logo" class="app-icon">
        <!-- 搜索输入框 -->
        <input 
          type="text" 
          class="search-input" 
          placeholder="输入需要管理的学科名称" 
          v-model="searchQuery"
          @keyup.enter="searchSubject"
        >
        <!-- 搜索按钮 -->
        <button class="search-button" @click="searchSubject">
          <img :src="SearchIcon" alt="搜索" class="search-icon">
        </button>
      </div>
    </div>

    <!-- 管理学科组件 -->
    <div class="manage-container" v-if="searchCompleted && subjectId">
      <AdminManage :subjectId="subjectId" />
    </div>
  </div>
</template>

<script>
import SearchIcon from '../assets/search.svg'
import AdminManage from './AdminManage.vue'
import axios from 'axios'

// 配置axios的baseURL
axios.defaults.baseURL = 'http://127.0.0.1:5000'

export default {
  name: 'EditSubjectWindow',
  components: {
    AdminManage
  },
  data() {
    return {
      searchQuery: '',
      SearchIcon: SearchIcon,
      searchCompleted: false,
      subjectId: null,
      isSearching: false
    }
  },
  methods: {
    // 搜索学科的方法
    async searchSubject() {
      // 验证搜索内容是否为空
      if (!this.searchQuery.trim()) {
        this.$message.warning('请输入搜索内容')
        return
      }
      
      // 如果正在搜索中，则不重复发送请求
      if (this.isSearching) {
        return
      }
      
      // 设置搜索中状态
      this.isSearching = true
      
      // 显示搜索中消息
      this.$message.info(`正在搜索: ${this.searchQuery}`)
      
      try {
        // 调用后端API搜索学科
        const response = await axios.get('/admin/search_subject/', {
          params: { name: this.searchQuery }
        })
        
        // 根据业务状态码处理响应
        if (response.data.code === 200) {
          // 设置搜索完成状态
          this.searchCompleted = true
          // 设置学科ID
          this.subjectId = response.data.data.id
          // 显示成功消息
          this.$message.success(response.data.message || '搜索成功')
        } else if (response.data.code === 404) {
          // 学科不存在
          this.$message.error(response.data.message || '未找到匹配的学科')
          // 重置搜索完成状态
          this.searchCompleted = false
          this.subjectId = null
        } else {
          // 其他错误
          this.$message.error(response.data.message || '搜索失败')
          // 重置搜索完成状态
          this.searchCompleted = false
          this.subjectId = null
        }
      } catch (error) {
        console.error('搜索学科时出错:', error)
        // 显示错误消息
        this.$message.error('搜索失败，请重试')
        // 重置搜索完成状态
        this.searchCompleted = false
        this.subjectId = null
      } finally {
        // 无论成功还是失败，都重置搜索中状态
        this.isSearching = false
      }
    }
  }
}
</script>

<style scoped>
/* 编辑学科窗口的主容器样式 */
.edit-subject-window {
  /* 设置容器宽度为100% */
  width: 100%;
  /* 设置最小高度为视口高度 */
  min-height: 100vh;
  /* 设置内边距，上下30px，左右50px */
  padding: 30px 50px;
  /* 设置背景颜色为淡蓝色 */
  background-color: rgb(230, 238, 252);
}

/* 页面头部区域样式 */
.header {
  /* 添加边框 */
  border: 1px solid #d0e0ff;
  /* 添加圆角 */
  border-radius: 8px;
  /* 添加内边距 */
  padding: 20px;
  /* 改变内部背景颜色 */
  background-color: rgba(240, 248, 255, 0.7);
  /* 添加阴影效果 */
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

/* 标题样式 */
.title {
  /* 设置字体大小为28px */
  font-size: 28px;
  /* 设置字体粗细为粗体 */
  font-weight: bold;
  /* 设置字体颜色为深灰色 */
  color: #333;
  /* 设置底部外边距为10px */
  margin-bottom: 10px;
}

/* 描述文本样式 */
.description {
  /* 设置字体大小为16px */
  font-size: 16px;
  /* 设置字体颜色为中灰色 */
  color: #666;
}

/* 搜索容器样式 */
.search-container {
  /* 弹性布局 */
  display: flex;
  /* 居中对齐 */
  justify-content: center;
  /* 上边距宽， 下边距窄 */
  /* 默认是这样，等搜索出来后，搜索框会移动到上面，用padding-top实现 */
  padding-top: 280px;
  padding-bottom: 30px;
  /* 添加过渡效果 */
  transition: padding-top 0.5s ease;
}

/* 搜索完成时的搜索容器样式 */
.search-container.active {
  /* 搜索完成后，搜索框移动到上面 */
  padding-top: 30px;
}

/* 搜索框样式 */
.search-box {
  /* 弹性布局 */
  display: flex;
  /* 居中对齐 */
  align-items: center;
  /* 背景色 */
  background-color: white;
  /* 圆角边框 */
  border-radius: 50px;
  /* 阴影效果 */
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  /* 内边距 */
  padding: 8px 15px;
  /* 宽度 */
  width: 80%;
  max-width: 600px;
  /* 边框 */
  border: 2px solid #e0e8f7;
  /* 过渡效果 */
  transition: all 0.5s ease;
  /* 默认放大1.2倍，搜索成功后变成1.0倍 */
  transform: scale(1.2);
}

/* 搜索完成时的搜索框样式 */
.search-box.active {
  /* 搜索完成后恢复正常大小 */
  transform: scale(1);
}

/* 搜索框悬停效果 */
.search-box:hover {
  /* 阴影增强 */
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
  /* 边框颜色变化 */
  border-color: #c0d0f0;
}

/* 搜索框选中效果 */
.search-box:focus-within {
  /* 阴影效果增强 */
  box-shadow: 0 8px 25px rgba(74, 128, 245, 0.2);
  /* 边框颜色变为主题蓝色 */
  border-color: #4a80f5;
  /* 确保过渡平滑 */
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

/* 应用图标样式 */
.app-icon {
  /* 尺寸 */
  width: 35px;
  height: 35px;
  /* 外边距 */
  margin-right: 12px;
  /* 圆形边框 */
  border-radius: 50%;
  /* 边框 */
  border: 1px solid rgba(0, 0, 0, 0.1);
}

/* 搜索输入框样式 */
.search-input {
  /* 尺寸 */
  flex: 1;
  /* 移除边框 */
  border: none;
  /* 移除轮廓 */
  outline: none;
  /* 字体大小 */
  font-size: 16px;
  /* 字体颜色 */
  color: #333;
}

/* 搜索输入框占位符颜色 */
.search-input::placeholder {
  color: #aaa;
}

/* 搜索按钮样式 */
.search-button {
  /* 背景透明 */
  background: transparent;
  /* 无边框 */
  border: none;
  /* 鼠标样式 */
  cursor: pointer;
  /* 圆形效果 */
  border-radius: 50%;
  /* 尺寸 */
  width: 36px;
  height: 36px;
  /* 弹性布局 */
  display: flex;
  /* 居中对齐 */
  align-items: center;
  justify-content: center;
  /* 过渡效果 */
  transition: background-color 0.3s;
}

/* 搜索按钮悬停效果 */
.search-button:hover {
  background-color: rgba(74, 128, 245, 0.1);
}

/* 搜索图标样式 */
.search-icon {
  width: 20px;
  height: 20px;
}

/* 管理容器样式 */
.manage-container {
  /* 添加显示动画 */
  animation: fadeIn 0.5s ease;
}

/* 淡入动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style> 