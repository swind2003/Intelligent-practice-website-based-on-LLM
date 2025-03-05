<template>
  <div class="home-window">
    <!-- 功能卡片容器 -->
    <div class="function-cards">
      <!-- 新建学科卡片 -->
      <div class="function-card">
        <div class="card-content">
          <!-- 图标 -->
          <img :src="BuildIcon" alt="新建学科" class="card-icon">
          <!-- 标题 -->
          <h2 class="card-title">新建学科</h2>
          <!-- 描述文本 -->
          <p class="card-description">
            结合业务需求，创建新的学科类型
          </p>
          <!-- 操作按钮 -->
          <div class="card-actions">
            <span class="action-btn" @click="navigateTo('subject-add')">立即新建</span>
            <span class="action-link">查看教程</span>
          </div>
        </div>
      </div>

      <!-- 题库管理卡片 -->
      <div class="function-card">
        <div class="card-content">
          <!-- 图标 -->
          <img :src="SubjectIcon" alt="题库管理" class="card-icon">
          <!-- 标题 -->
          <h2 class="card-title">题库管理</h2>
          <!-- 描述文本 -->
          <p class="card-description">
            基于已有学科，支持题目管理、批量导入等多种功能
          </p>
          <!-- 操作按钮 -->
          <div class="card-actions">
            <span class="action-btn" @click="navigateTo('subject-edit')">立即管理</span>
            <span class="action-link">查看教程</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SubjectIcon from '../assets/database.svg'
import BuildIcon from '../assets/build.svg'

export default {
  name: 'HomeWindow',
  data() {
    return {
      SubjectIcon,
      BuildIcon
    }
  },
  methods: {
    navigateTo(childKey) {
      // 通知父组件更新导航状态
      this.$emit('update-nav', childKey)
    }
  }
}
</script>

<style scoped>
.home-window {
  /* 铺满整个主视口区域 */
  width: 100%;
  height: 100vh;
  /* 居中布局 */
  display: flex;
  justify-content: center;
  align-items: center;
}

.function-cards {
  /* 卡片容器布局 */
  display: flex;
  gap: 40px;
  /* 容器最大宽度 */
  max-width: 1200px;
  /* 容器内边距 */
  padding: 20px;
}

.function-card {
  /* 卡片基础样式 */
  width: 400px;
  height: 300px;
  /* 背景和边框 */
  background: linear-gradient(
    135deg,
    rgba(254, 246, 246, 0.95),
    rgba(215, 226, 249, 0.9)
  );
  border: 1px solid rgba(190, 210, 255, 0.3);
  border-radius: 12px;
  /* 阴影效果 */
  box-shadow: 
    0 4px 20px rgba(100, 140, 255, 0.08),
    inset 0 0 20px rgba(255, 255, 255, 0.5);
  /* 过渡效果 */
  transition: all 0.3s ease;
  /* 鼠标样式 */
  cursor: pointer;
  /* 溢出隐藏 */
  overflow: hidden;
  /* 相对定位 */
  position: relative;
}

.function-card:hover {
  /* 悬停效果 */
  transform: translateY(-5px);
  box-shadow: 
    0 8px 30px rgba(100, 140, 255, 0.12),
    inset 0 0 25px rgba(255, 255, 255, 0.6);
  border-color: rgba(160, 190, 255, 0.5);
  background: linear-gradient(
    135deg,
    rgba(253, 243, 243, 0.97),
    rgba(223, 236, 250, 0.92)
  );
}

.card-content {
  /* 内容布局 */
  padding: 30px;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.card-icon {
  /* 图标样式 */
  width: 60px;
  height: 60px;
  margin-bottom: 20px;
  /* 图标颜色 */
  filter: invert(40%) sepia(60%) saturate(450%) hue-rotate(210deg) brightness(95%) contrast(95%);
  /* 添加发光效果 */
  filter: drop-shadow(0 0 2px rgba(91, 117, 255, 0.2));
}

.card-title {
  /* 标题样式 */
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin: 0 0 15px 0;
}

.card-description {
  /* 描述文本样式 */
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin: 0 0 25px 0;
  flex-grow: 1;
}

.card-actions {
  /* 按钮容器样式 */
  display: flex;
  gap: 20px;
  align-items: center;
}

.action-btn {
  /* 主按钮样式 */
  padding: 8px 20px;
  background: linear-gradient(135deg, #5B75FF, #4159DB);
  color: white;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(75, 97, 227, 0.2);
}

.action-btn:hover {
  /* 主按钮悬停效果 */
  background: linear-gradient(135deg, #6B83FF, #4E64E6);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(75, 97, 227, 0.3);
}

.action-link {
  /* 次要链接样式 */
  color: #5B75FF;
  font-size: 14px;
  text-decoration: none;
  position: relative;
}

.action-link::after {
  /* 下划线效果 */
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 1px;
  background: #5B75FF;
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.action-link:hover::after {
  /* 下划线悬停效果 */
  transform: scaleX(1);
}
</style> 