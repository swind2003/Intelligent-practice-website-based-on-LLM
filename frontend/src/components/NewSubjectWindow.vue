<template>
  <!-- 新增学科窗口的主容器 -->
  <div class="new-subject-window" @click="clearSelection">
    <!-- 页面头部区域 -->
    <div class="header">
      <!-- 标题 -->
      <h1 class="title">新增学科</h1>
      <!-- 描述文本 -->
      <div class="description">在此页面添加新的学科，设置学科名称和描述</div>
    </div>

    <!-- 加载提示 -->
    <div class="loading-container" v-if="loading">
      <!-- 加载动画 -->
      <div class="spinner"></div>
      <!-- 加载文本 -->
      <span>正在加载学科数据...</span>
    </div>

    <!-- 已有学科卡片部分 -->
    <div class="feature-section" v-if="!loading">
      <!-- 学科列表标题 -->
      <h2 class="section-title">学科列表</h2>
      
      <!-- 卡片网格布局 -->
      <div class="card-grid">
        <!-- 添加学科按钮 -->
        <div class="feature-card add-card" @click.stop="openCreateSubjectForm">
          <!-- 添加图标 -->
          <div class="add-icon">
            <span class="plus-icon">+</span>
          </div>
          <!-- 添加文本 -->
          <div class="add-text">点击创建新学科</div>
        </div>
        
        <!-- 循环渲染学科卡片 -->
        <div 
          v-for="(feature, index) in features" 
          :key="index"
          class="feature-card"
          :class="{ 'selected': selectedFeatures.includes(feature.id) }"
          @click.stop="batchMode ? toggleBatchSelect(feature.id) : toggleFeature(feature.id)"
          :style="selectedFeatures.includes(feature.id) ? { borderColor: feature.color, boxShadow: `0 8px 16px ${feature.color}33, inset 0 0 8px ${feature.color}20` } : {}"
        >
          <!-- 卡片图标 -->
          <div class="card-icon" :style="{ background: feature.color }">
            <img :src="feature.icon" alt="图标" class="icon-image">
          </div>
          <!-- 卡片内容区域 -->
          <div class="card-content">
            <!-- 卡片标题 -->
            <h3 class="card-title">{{ feature.name }}</h3>
            <!-- 卡片描述 -->
            <p class="card-description">{{ feature.description }}</p>
            
            <!-- 卡片操作区域 -->
            <div class="card-actions">
              <!-- 编辑按钮 -->
              <button class="action-button" @click.stop="editSubject(feature.id)">
                <img :src="EditIcon" alt="编辑" class="action-icon">
                编辑学科
              </button>
              <!-- 分隔线 -->
              <div class="action-divider"></div>
              <!-- 删除按钮 -->
              <button class="action-button" @click.stop="deleteSubject(feature.id)">
                <img :src="DeleteIcon" alt="删除" class="action-icon">
                删除学科
              </button>
            </div>
          </div>
          <!-- 选中标记 -->
          <div v-if="selectedFeatures.includes(feature.id)" class="selection-mark" :style="{ backgroundColor: feature.color }"></div>
        </div>
      </div>
    </div>

    <!-- 批量删除按钮 -->
    <div class="batch-delete-btn" v-if="!batchMode" @click.stop="enterBatchMode">
      <!-- 删除图标 -->
      <img :src="DeleteIcon" alt="批量删除" class="batch-icon">
      <!-- 按钮文本 -->
      <span>批量删除</span>
    </div>

    <!-- 批量删除提示栏 -->
    <div class="batch-delete-bar" v-if="batchMode">
      <!-- 批量删除消息 -->
      <div class="batch-message">
        <!-- 删除图标 -->
        <img :src="DeleteIcon" alt="批量删除" class="batch-icon">
        <!-- 选择提示 -->
        <span>已选择 {{ selectedFeatures.length }} 个学科，请确认是否删除</span>
      </div>
      <!-- 批量操作按钮 -->
      <div class="batch-actions">
        <!-- 取消按钮 -->
        <button class="batch-action-btn cancel-btn" @click.stop="cancelBatchDelete">
          取消删除
        </button>
        <!-- 确认按钮 -->
        <button class="batch-action-btn confirm-btn" @click.stop="showBatchConfirmDialog" :disabled="selectedFeatures.length === 0">
          确认删除
        </button>
      </div>
    </div>

    <!-- 删除确认对话框 -->
    <div class="confirm-dialog" v-if="showConfirmDialog">
      <div class="confirm-dialog-content">
        <!-- 对话框标题 -->
        <div class="confirm-dialog-header">
          <h3>删除确认</h3>
        </div>
        <!-- 对话框内容 -->
        <div class="confirm-dialog-body">
          <!-- 单个删除提示 -->
          <p v-if="deleteMode === 'single'">确定要删除这个学科吗？此操作不可恢复。</p>
          <!-- 批量删除提示 -->
          <p v-else>确定要删除选中的 {{ selectedFeatures.length }} 个学科吗？此操作不可恢复。</p>
        </div>
        <!-- 对话框底部按钮 -->
        <div class="confirm-dialog-footer">
          <!-- 取消按钮 -->
          <button class="dialog-btn cancel-btn" @click="cancelDelete">取消</button>
          <!-- 确认删除按钮 -->
          <button class="dialog-btn confirm-btn" @click="executeDelete">确认删除</button>
        </div>
      </div>
    </div>

    <!-- 创建学科表单对话框 -->
    <div class="form-dialog" v-if="showCreateForm">
      <div class="form-dialog-content">
        <!-- 表单对话框标题 -->
        <div class="form-dialog-header">
          <h3>创建新学科</h3>
        </div>
        <!-- 表单对话框内容 -->
        <div class="form-dialog-body">
          <!-- 学科名称输入组 -->
          <div class="form-group">
            <label for="subject-name">学科名称</label>
            <input 
              type="text" 
              id="subject-name" 
              v-model="subjectForm.name" 
              placeholder="请输入学科名称"
              @click.stop
            >
          </div>
          <!-- 学科描述输入组 -->
          <div class="form-group">
            <label for="subject-description">学科描述</label>
            <textarea 
              id="subject-description" 
              v-model="subjectForm.description" 
              placeholder="请输入学科描述"
              rows="5"
              @click.stop
            ></textarea>
          </div>
        </div>
        <!-- 表单对话框底部按钮 -->
        <div class="form-dialog-footer">
          <!-- 取消按钮 -->
          <button class="dialog-btn cancel-btn" @click.stop="cancelCreateForm">取消</button>
          <!-- 创建按钮 -->
          <button 
            class="dialog-btn confirm-btn create-btn" 
            @click.stop="submitCreateForm"
            :disabled="!subjectForm.name"
          >
            创建
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// 导入图标
import FishIcon from '../assets/base_icon.svg'
import EditIcon from '../assets/edit.svg'
import DeleteIcon from '../assets/delete.svg'
import axios from 'axios'

// 配置axios的baseURL
axios.defaults.baseURL = 'http://127.0.0.1:5000'

export default {
  // 组件名称
  name: 'NewSubjectWindow',
  // 组件数据
  data() {
    return {
      // 学科表单数据
      subjectName: '',
      // 学科描述
      subjectDescription: '',
      // 已选择的学科ID数组
      selectedFeatures: [],
      // 批量删除模式标志
      batchMode: false,
      // 导入的图标
      EditIcon: EditIcon,
      DeleteIcon: DeleteIcon,
      
      // 删除确认对话框相关
      showConfirmDialog: false,
      // 删除模式：'single'单个删除或'batch'批量删除
      deleteMode: 'single', 
      // 待删除的单个学科ID
      pendingDeleteId: null, 
      
      // 新增属性
      // 加载状态
      loading: false, 
      
      // 学科列表（从API获取）
      features: [],
      
      // 创建学科表单相关
      // 表单显示状态
      showCreateForm: false,
      // 表单数据
      subjectForm: {
        // 学科名称
        name: '',
        // 学科描述
        description: ''
      },
    }
  },
  // 组件挂载完成后执行
  mounted() {
    // 页面加载时获取学科数据
    this.fetchSubjects()
  },
  // 组件方法
  methods: {
    // 获取学科数据
    async fetchSubjects() {
      // 设置加载状态为true
      this.loading = true
      try {
        // 发送GET请求获取学科列表
        const response = await axios.get('/admin/get_subjects/')
        
        // 请求成功
        if (response.data.code === 200) {
          // 转换后端数据为前端展示格式
          this.features = response.data.data.map(subject => ({
            // 学科ID
            id: subject.id,
            // 学科名称
            name: subject.name,
            // 学科描述，如果没有则显示"暂无描述"
            description: subject.description || '暂无描述',
            // 学科图标
            icon: FishIcon,
            // 随机生成一个颜色
            color: this.getRandomColor() 
          }))
          
          // 显示成功消息
          this.$message.success(response.data.message)
        } else {
          // 显示错误消息
          this.$message.error(`获取学科失败: ${response.data.message}`)
        }
      } catch (error) {
        // 捕获并记录错误
        console.error('获取学科数据失败:', error)
        // 显示错误消息
        this.$message.error(`获取学科失败: ${error.message || '服务器错误'}`)
      } finally {
        // 无论成功失败，都将加载状态设为false
        this.loading = false
      }
    },
    
    // 生成随机颜色
    getRandomColor() {
      // 预定义颜色数组
      const colors = [
        'rgb(33, 150, 243)', // 蓝色
        'rgb(102, 205, 170)',// 中碧绿
        'rgb(240, 230, 140)',// 卡其色
        'rgb(156, 39, 176)', // 紫色
        'rgb(233, 30, 99)',  // 粉色
        'rgb(244, 67, 54)',  // 红色
        'rgb(0, 188, 212)',  // 青色
        'rgb(255, 87, 34)',  // 橙色
        'rgb(0, 206, 209)',  // 深松石绿
        'rgb(205, 92, 92)',  // 印度红
        'rgb(221, 160, 221)',// 李紫
        'rgb(240, 128, 128)',// 浅珊瑚红
        'rgb(255, 182, 193)',// 浅粉
        'rgb(255, 218, 185)',// 粉扑桃色
        'rgb(106, 90, 205)', // 岩蓝
        'rgb(72, 61, 139)',  // 深岩蓝
      ]
      // 随机返回一个颜色
      return colors[Math.floor(Math.random() * colors.length)]
    },
    
    // 清空所有选择
    clearSelection() {
      // 如果不是批量模式，清空选择
      if (!this.batchMode) {
        this.selectedFeatures = [];
      }
    },
    
    // 切换学科选择状态
    toggleFeature(featureId) {
      // 如果当前选中的就是点击的学科，则取消选择
      if (this.selectedFeatures.includes(featureId)) {
        this.selectedFeatures = [];
      } else {
        // 否则，清空之前的选择，只选择当前点击的学科
        this.selectedFeatures = [featureId];
      }
    },
    
    // 进入批量删除模式
    enterBatchMode() {
      // 设置批量模式为true
      this.batchMode = true;
      // 清空之前的选择
      this.selectedFeatures = []; 
    },
    
    // 批量选择模式下的切换选择
    toggleBatchSelect(featureId) {
      // 查找学科ID在选中列表中的索引
      const index = this.selectedFeatures.indexOf(featureId);
      if (index === -1) {
        // 如果不在选中列表中，添加
        this.selectedFeatures.push(featureId);
      } else {
        // 如果已选中，则移除
        this.selectedFeatures.splice(index, 1);
      }
    },
    
    // 取消批量删除
    cancelBatchDelete() {
      // 退出批量模式
      this.batchMode = false;
      // 清空选择
      this.selectedFeatures = [];
    },
    
    // 显示批量删除确认对话框
    showBatchConfirmDialog() {
      // 如果没有选中项，直接返回
      if (this.selectedFeatures.length === 0) return;
      // 设置删除模式为批量
      this.deleteMode = 'batch';
      // 显示确认对话框
      this.showConfirmDialog = true;
    },
    
    // 取消删除操作
    cancelDelete() {
      // 隐藏确认对话框
      this.showConfirmDialog = false;
      // 清空待删除ID
      this.pendingDeleteId = null;
    },
    
    // 执行删除操作
    async executeDelete() {
      // 根据删除模式执行不同的删除方法
      if (this.deleteMode === 'single') {
        // 执行单个删除
        await this.executeSingleDelete();
      } else {
        // 执行批量删除
        await this.executeBatchDelete();
      }
      
      // 关闭确认对话框
      this.showConfirmDialog = false;
      // 清空待删除ID
      this.pendingDeleteId = null;
    },
    
    // 执行单个学科删除
    async executeSingleDelete() {
      // 如果没有待删除ID，直接返回
      if (!this.pendingDeleteId) return;
      
      try {
        // 调用后端删除API
        const response = await axios.delete(`/admin/delete_subject/${this.pendingDeleteId}`);
        
        // 请求成功
        if (response.data.code === 200) {
          // 从前端移除已删除的学科
          this.features = this.features.filter(
            feature => feature.id !== this.pendingDeleteId
          );
          
          // 显示成功提示
          this.$message.success(response.data.message);
        } else {
          // 显示错误消息
          this.$message.error(response.data.message);
        }
        
      } catch (error) {
        // 处理错误
        console.error('删除学科失败:', error);
        
        // 获取错误信息
        const errorMessage = error.response?.data?.message || '删除失败，请重试';
        // 显示错误消息
        this.$message.error(`错误: ${errorMessage}`);
      }
    },
    
    // 执行批量删除
    async executeBatchDelete() {
      // 如果没有选中项，直接返回
      if (this.selectedFeatures.length === 0) return;
      
      try {
        // 调用后端批量删除API
        const response = await axios.post('/admin/batch_delete_subjects/', {
          ids: this.selectedFeatures
        });
        
        // 请求成功
        if (response.data.code === 200) {
          // 从前端移除已删除的学科
          this.features = this.features.filter(
            feature => !this.selectedFeatures.includes(feature.id)
          );
          
          // 显示成功提示
          this.$message.success(response.data.message);
        } else {
          // 显示错误消息
          this.$message.error(response.data.message);
        }
        
        // 退出批量删除模式
        this.batchMode = false;
        // 清空选择
        this.selectedFeatures = [];
        
      } catch (error) {
        // 处理错误
        console.error('批量删除失败:', error);
        
        // 获取错误信息
        const errorMessage = error.response?.data?.message || '删除失败，请重试';
        // 显示错误消息
        this.$message.error(`错误: ${errorMessage}`);
      }
    },
    
    // 删除单个学科
    deleteSubject(subjectId) {
      // 设置待删除ID并显示确认对话框
      this.pendingDeleteId = subjectId;
      // 设置删除模式为单个
      this.deleteMode = 'single';
      // 显示确认对话框
      this.showConfirmDialog = true;
    },
    
    // 打开创建学科表单
    openCreateSubjectForm() {
      // 清空表单数据
      this.subjectForm.name = ''
      this.subjectForm.description = ''
      // 显示表单
      this.showCreateForm = true
    },
    
    // 取消创建表单
    cancelCreateForm() {
      // 隐藏创建表单
      this.showCreateForm = false
    },
    
    // 提交创建学科表单
    async submitCreateForm() {
      // 验证学科名称不能为空
      if (!this.subjectForm.name) {
        this.$message.error('学科名称不能为空');
        return
      }
      
      try {
        // 调用后端创建学科API
        const response = await axios.post('/admin/create_subject/', {
          name: this.subjectForm.name,
          description: this.subjectForm.description
        })
        
        // 请求成功
        if (response.data.code === 200) {
          // 显示成功消息
          this.$message.success(response.data.message);
          
          // 关闭表单
          this.showCreateForm = false
          
          // 重新加载学科列表
          this.fetchSubjects()
        } else {
          // 显示错误消息
          this.$message.error(response.data.message);
        }
      } catch (error) {
        // 记录错误
        console.error('创建学科失败:', error)
        // 显示错误消息
        this.$message.error(`创建学科失败: ${error.message || '服务器错误'}`);
      }
    },
    
    // 编辑单个学科
    editSubject(subjectId) {
      // 记录编辑操作
      console.log('编辑学科:', subjectId);
      // 编辑功能将在后续开发中实现
    },
  },
  // 添加公开方法，供父组件调用
  public: {
    // 重新加载学科数据
    reloadSubjects() {
      this.fetchSubjects()
    }
  }
}
</script>

<style scoped>
/* 新增学科窗口的主容器样式 */
.new-subject-window {
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
  /* 设置底部外边距为30px */
  margin-bottom: 30px;
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

/* 学科部分的容器样式 */
.feature-section {
  /* 设置底部外边距为40px */
  margin-bottom: 40px;
}

/* 部分标题样式 */
.section-title {
  /* 设置字体大小为20px */
  font-size: 20px;
  /* 设置底部外边距为20px */
  margin-bottom: 20px;
  /* 设置字体颜色为深灰色 */
  color: #333;
}

/* 卡片网格布局样式 */
.card-grid {
  /* 使用网格布局 */
  display: grid;
  /* 设置网格列宽，自动填充，最小宽度350px，最大宽度1fr */
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  /* 设置网格间距为20px */
  gap: 20px;
}

/* 学科卡片样式 */
.feature-card {
  /* 使用弹性布局 */
  display: flex;
  /* 设置背景颜色为白色 */
  background: white;
  /* 设置边框圆角为12px */
  border-radius: 12px;
  /* 隐藏溢出内容 */
  overflow: hidden;
  /* 添加阴影效果 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  /* 添加过渡效果，持续0.3秒，平滑过渡 */
  transition: all 0.3s ease;
  /* 设置鼠标指针为手型 */
  cursor: pointer;
  /* 设置边框为2px宽，透明色 */
  border: 2px solid transparent;
  /* 设置固定高度 */
  height: 210px;
}

/* 学科卡片悬停效果 */
.feature-card:hover {
  /* 向上移动5px */
  transform: translateY(-5px);
  /* 增强阴影效果 */
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

/* 被选中的学科卡片样式 */
.feature-card.selected {
  /* 移除固定的边框颜色，现在通过内联样式设置 */
  /* border-color: #4a80f5; */
  /* 移除固定的阴影效果，现在通过内联样式设置 */
  /* box-shadow: 0 8px 16px rgba(74, 128, 245, 0.2); */
  /* 添加轻微缩放效果 */
  transform: scale(1.02);
  /* 移除固定的内部发光效果，现在通过内联样式设置 */
  /* box-shadow: 0 8px 16px rgba(74, 128, 245, 0.2), inset 0 0 8px rgba(74, 128, 245, 0.1); */
  /* 添加过渡效果 */
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  /* 设置文字颜色加深 */
  color: #2c3e50;
  /* 添加选中标记 */
  position: relative;
}

/* 添加选中标记样式 */
.selection-mark {
  /* 设置绝对定位 */
  position: absolute;
  /* 设置顶部位置为-1px */
  top: -1px;
  /* 设置右侧位置为-1px */
  right: -1px;
  /* 设置宽度为24px */
  width: 24px;
  /* 设置高度为24px */
  height: 24px;
  /* 边框圆角为50%，形成圆形 */
  border-radius: 50%;
  /* 设置边框为2px实线白色 */
  border: 2px solid white;
  /* 添加阴影效果 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  /* 设置背景图片为SVG勾选图标 */
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white'%3E%3Cpath d='M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z'/%3E%3C/svg%3E");
  /* 设置背景图片大小为16px */
  background-size: 16px;
  /* 设置背景图片位置为居中 */
  background-position: center;
  /* 设置背景图片不重复 */
  background-repeat: no-repeat;
}

/* 移除之前的选中标记样式，因为已经用新的组件替代 */
.feature-card.selected::after {
  content: none;
}

/* 卡片图标容器样式 */
.card-icon {
  /* 使用弹性布局 */
  display: flex;
  /* 垂直居中对齐 */
  align-items: center;
  /* 水平居中对齐 */
  justify-content: center;
  /* 设置宽度为70px */
  width: 70px;
  /* 设置内边距为15px */
  padding: 15px;
}

/* 图标图片样式 */
.icon-image {
  /* 设置宽度为40px */
  width: 40px;
  /* 设置高度为40px */
  height: 40px;
}

/* 卡片内容区域样式 */
.card-content {
  /* 设置弹性增长系数为1，占据剩余空间 */
  flex: 1;
  /* 设置内边距为20px */
  padding: 20px;
  /* 设置左侧边框为1px实线浅灰色 */
  border-left: 1px solid #eee;
  /* 设置相对定位，用于绝对定位子元素 */
  position: relative;
  /* 设置弹性布局 */
  display: flex;
  /* 设置方向为纵向 */
  flex-direction: column;
  /* 设置内容区域高度为100% */
  height: 100%;
}

/* 卡片标题样式 */
.card-title {
  /* 设置字体大小为18px */
  font-size: 18px;
  /* 设置字体粗细为600 */
  font-weight: 600;
  /* 设置底部外边距为8px */
  margin-bottom: 8px;
  /* 设置字体颜色为深灰色 */
  color: #333;
}

/* 卡片描述文本样式 */
.card-description {
  /* 设置字体大小为14px */
  font-size: 14px;
  /* 设置字体颜色为中灰色 */
  color: #666;
  /* 设置底部外边距为15px */
  margin-bottom: 15px;
  /* 启用垂直滚动 */
  overflow-y: auto;
  /* 设置最大高度 */
  max-height: 90px;
  /* 添加内边距，防止文字靠近滚动条 */
  padding-right: 5px;
  /* 设置弹性增长 */
  flex-grow: 1;
}

/* 设置滚动条样式 */
.card-description::-webkit-scrollbar {
  /* 设置滚动条宽度为4px */
  width: 4px;
}

.card-description::-webkit-scrollbar-track {
  /* 设置滚动条轨道背景为浅灰色 */
  background: #f1f1f1;
  /* 设置滚动条轨道边框圆角为2px */
  border-radius: 2px;
}

.card-description::-webkit-scrollbar-thumb {
  /* 设置滚动条滑块背景为灰色 */
  background: #c0c6d0;
  /* 设置滚动条滑块边框圆角为2px */
  border-radius: 2px;
}

.card-description::-webkit-scrollbar-thumb:hover {
  /* 设置滚动条滑块悬停时背景为深灰色 */
  background: #a0a6b0;
}

/* 卡片操作区域样式 */
.card-actions {
  /* 使用弹性布局 */
  display: flex;
  /* 设置上边框为1px实线浅灰色 */
  border-top: 1px solid #eee;
  /* 设置上内边距为15px */
  padding-top: 15px;
  /* 设置底部位置固定 */
  position: absolute;
  /* 设置底部位置为0 */
  bottom: 0;
  /* 设置左侧位置为0 */
  left: 0;
  /* 设置右侧位置为0 */
  right: 0;
  /* 设置内边距 */
  padding: 15px 20px;
  /* 确保在最上层 */
  z-index: 2;
  /* 设置背景色，防止透视 */
  background: white;
}

/* 操作按钮样式 */
.action-button {
  /* 设置弹性增长系数为1，平均分配空间 */
  flex: 1;
  /* 移除背景 */
  background: none;
  /* 移除边框 */
  border: none;
  /* 设置内边距为8px */
  padding: 8px;
  /* 设置字体颜色为蓝色 */
  color: #4a80f5;
  /* 设置字体大小为14px */
  font-size: 14px;
  /* 设置鼠标指针为手型 */
  cursor: pointer;
  /* 添加过渡效果，持续0.2秒 */
  transition: all 0.2s;
  /* 使用弹性布局 */
  display: flex;
  /* 水平居中对齐 */
  justify-content: center;
  /* 垂直居中对齐 */
  align-items: center;
  /* 设置间距 */
  gap: 5px;
}

/* 操作图标样式 */
.action-icon {
  /* 设置宽度为16px */
  width: 16px;
  /* 设置高度为16px */
  height: 16px;
}

/* 操作按钮悬停效果 */
.action-button:hover {
  /* 设置悬停时字体颜色为深蓝色 */
  color: #2c5cc5;
  /* 设置悬停时背景为淡蓝色 */
  background: rgba(74, 128, 245, 0.1);
  /* 添加阴影效果 */
  box-shadow: 0 2px 8px rgba(74, 128, 245, 0.2);
  /* 添加边框圆角 */
  border-radius: 4px;
  /* 添加字体加粗效果 */
  font-weight: 500;
  /* 确保过渡效果平滑 */
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 操作区域分隔线样式 */
.action-divider {
  /* 设置宽度为1px */
  width: 1px;
  /* 设置背景颜色为浅灰色 */
  background: #eee;
}

/* 添加卡片样式 */
.add-card {
  /* 使用弹性布局 */
  display: flex;
  /* 设置弹性方向为纵向 */
  flex-direction: column;
  /* 垂直居中对齐 */
  align-items: center;
  /* 水平居中对齐 */
  justify-content: center;
  /* 设置背景颜色为浅灰色 */
  background-color: #f5f7fa;
  /* 设置边框为2px虚线灰色 */
  border: 2px dashed #c0c6d0;
  /* 设置鼠标指针为手型 */
  cursor: pointer;
  /* 添加过渡效果，持续0.3秒，平滑过渡 */
  transition: all 0.3s ease;
  /* 设置内边距，上下30px，左右20px */
  padding: 30px 20px;
}

/* 添加卡片悬停效果 */
.add-card:hover {
  /* 设置悬停时背景颜色为更浅的灰色 */
  background-color: #edf1f7;
  /* 向上移动5px */
  transform: translateY(-5px);
}

/* 添加图标容器样式 */
.add-icon {
  /* 使用弹性布局 */
  display: flex;
  /* 垂直居中对齐 */
  align-items: center;
  /* 水平居中对齐 */
  justify-content: center;
  /* 设置宽度为60px */
  width: 60px;
  /* 设置高度为60px */
  height: 60px;
  /* 设置边框圆角为50%，形成圆形 */
  border-radius: 50%;
  /* 设置背景颜色为浅灰色 */
  background-color: #f0f2f5;
  /* 设置底部外边距为15px */
  margin-bottom: 15px;
}

/* 加号图标样式 */
.plus-icon {
  /* 设置字体大小为36px */
  font-size: 36px;
  /* 设置字体颜色为灰色 */
  color: #8c9bae;
  /* 设置底部内边距为6px，调整垂直位置 */
  padding-bottom: 6px;
}

/* 添加文本样式 */
.add-text {
  /* 设置字体大小为14px */
  font-size: 14px;
  /* 设置字体颜色为灰色 */
  color: #8c9bae;
  /* 设置文本居中对齐 */
  text-align: center;
}

/* 批量删除按钮样式 */
.batch-delete-btn {
  /* 设置固定定位 */
  position: fixed;
  /* 设置底部位置为30px */
  bottom: 30px;
  /* 设置右侧位置为30px */
  right: 30px;
  /* 使用弹性布局 */
  display: flex;
  /* 垂直居中对齐 */
  align-items: center;
  /* 设置元素间距为8px */
  gap: 8px;
  /* 设置背景颜色为蓝色 */
  background-color: #4a80f5;
  /* 设置字体颜色为白色 */
  color: white;
  /* 设置内边距，上下12px，左右20px */
  padding: 12px 20px;
  /* 设置边框圆角为50px */
  border-radius: 50px;
  /* 添加阴影效果 */
  box-shadow: 0 4px 12px rgba(74, 128, 245, 0.3);
  /* 设置鼠标指针为手型 */
  cursor: pointer;
  /* 添加过渡效果，持续0.3秒，平滑过渡 */
  transition: all 0.3s ease;
  /* 设置层级为100 */
  z-index: 100;
}

.batch-delete-btn:hover {
  /* 设置悬停时背景颜色为深蓝色 */
  background-color: #3a6ad8;
  /* 向上移动3px */
  transform: translateY(-3px);
  /* 增强阴影效果 */
  box-shadow: 0 6px 15px rgba(74, 128, 245, 0.4);
}

.batch-icon {
  /* 设置宽度为20px */
  width: 20px;
  /* 设置高度为20px */
  height: 20px;
  /* 设置滤镜，使图标变为白色 */
  filter: brightness(0) invert(1);
}

/* 批量删除提示栏样式 */
.batch-delete-bar {
  /* 设置固定定位 */
  position: fixed;
  /* 设置底部位置为10px */
  bottom: 10px;
  /* 设置右侧位置为3% */
  right: 3%;
  /* 设置宽度为80% */
  width: 80%;
  /* 设置背景颜色为白色 */
  background-color: white;
  /* 添加阴影效果 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  /* 设置内边距，上下15px，左右20px */
  padding: 15px 20px;
  /* 使用弹性布局 */
  display: flex;
  /* 两端对齐 */
  justify-content: space-between;
  /* 垂直居中对齐 */
  align-items: center;
  /* 设置层级为100 */
  z-index: 100;
  /* 设置边框圆角为8px */
  border-radius: 8px;
  /* 设置边框为1px实线浅灰色 */
  border: 1px solid #eaeaea;
}

.batch-message {
  /* 使用弹性布局 */
  display: flex;
  /* 垂直居中对齐 */
  align-items: center;
  /* 设置元素间距为10px */
  gap: 10px;
  /* 设置字体颜色为深灰色 */
  color: #333;
  /* 设置字体大小为14px */
  font-size: 14px;
  /* 设置最大宽度为250px */
  max-width: 250px;
}

.batch-message .batch-icon {
  /* 移除滤镜效果 */
  filter: none;
  /* 设置透明度为0.7 */
  opacity: 0.7;
}

.batch-actions {
  /* 使用弹性布局 */
  display: flex;
  /* 设置元素间距为10px */
  gap: 10px;
}

.batch-action-btn {
  /* 设置内边距，上下8px，左右15px */
  padding: 8px 15px;
  /* 设置边框圆角为4px */
  border-radius: 4px;
  /* 移除边框 */
  border: none;
  /* 设置字体粗细为500 */
  font-weight: 500;
  /* 设置字体大小为13px */
  font-size: 13px;
  /* 设置鼠标指针为手型 */
  cursor: pointer;
  /* 添加过渡效果，持续0.2秒，平滑过渡 */
  transition: all 0.2s ease;
}

.cancel-btn {
  /* 设置背景颜色为浅灰色 */
  background-color: #f0f0f0;
  /* 设置字体颜色为灰色 */
  color: #555;
}

.cancel-btn:hover {
  /* 设置悬停时背景颜色为深灰色 */
  background-color: #e0e0e0;
}

.confirm-btn {
  /* 设置背景颜色为蓝色 */
  background-color: #4a80f5;
  /* 设置字体颜色为白色 */
  color: white;
}

.confirm-btn:hover {
  /* 设置悬停时背景颜色为深蓝色 */
  background-color: #3a6ad8;
}

.confirm-btn:disabled {
  /* 设置禁用时背景颜色为灰色 */
  background-color: #a0a0a0;
  /* 设置鼠标指针为禁止 */
  cursor: not-allowed;
}

/* 确认对话框样式 */
.confirm-dialog {
  /* 固定定位 */
  position: fixed;
  /* 顶部对齐 */
  top: 0;
  /* 左侧对齐 */
  left: 0;
  /* 右侧对齐 */
  right: 0;
  /* 底部对齐 */
  bottom: 0;
  /* 半透明黑色背景 */
  background-color: rgba(0, 0, 0, 0.5);
  /* 弹性布局 */
  display: flex;
  /* 水平居中 */
  justify-content: center;
  /* 垂直居中 */
  align-items: center;
  /* 设置层级 */
  z-index: 1000;
}

.confirm-dialog-content {
  /* 白色背景 */
  background-color: white;
  /* 圆角边框 */
  border-radius: 8px;
  /* 设置宽度 */
  width: 400px;
  /* 添加阴影效果 */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.confirm-dialog-header {
  /* 内边距 */
  padding: 15px 20px;
  /* 底部边框 */
  border-bottom: 1px solid #eaeaea;
}

.confirm-dialog-header h3 {
  /* 移除外边距 */
  margin: 0;
  /* 设置字体大小 */
  font-size: 18px;
  /* 设置字体颜色 */
  color: #333;
}

.confirm-dialog-body {
  /* 内边距 */
  padding: 20px;
}

.confirm-dialog-body p {
  /* 移除外边距 */
  margin: 0;
  /* 设置字体颜色 */
  color: #555;
  /* 设置字体大小 */
  font-size: 15px;
  /* 设置行高 */
  line-height: 1.5;
}

.confirm-dialog-footer {
  /* 内边距 */
  padding: 15px 20px;
  /* 弹性布局 */
  display: flex;
  /* 靠右对齐 */
  justify-content: flex-end;
  /* 设置间距 */
  gap: 10px;
  /* 顶部边框 */
  border-top: 1px solid #eaeaea;
}

.dialog-btn {
  /* 内边距 */
  padding: 8px 16px;
  /* 圆角边框 */
  border-radius: 4px;
  /* 移除边框 */
  border: none;
  /* 字体粗细 */
  font-weight: 500;
  /* 字体大小 */
  font-size: 14px;
  /* 鼠标指针样式 */
  cursor: pointer;
  /* 过渡效果 */
  transition: all 0.2s ease;
}

.dialog-btn.cancel-btn {
  /* 背景颜色 */
  background-color: #f0f0f0;
  /* 字体颜色 */
  color: #555;
}

.dialog-btn.cancel-btn:hover {
  /* 悬停时背景颜色 */
  background-color: #e0e0e0;
}

.dialog-btn.confirm-btn {
  /* 背景颜色 */
  background-color: #f44336;
  /* 字体颜色 */
  color: white;
}

.dialog-btn.confirm-btn:hover {
  /* 悬停时背景颜色 */
  background-color: #d32f2f;
}

/* 加载提示容器样式 */
.loading-container {
  /* 弹性布局 */
  display: flex;
  /* 垂直方向排列 */
  flex-direction: column;
  /* 水平居中 */
  align-items: center;
  /* 垂直居中 */
  justify-content: center;
  /* 内边距 */
  padding: 50px 0;
  /* 字体颜色 */
  color: #666;
}

/* 加载动画样式 */
.spinner {
  /* 宽度 */
  width: 40px;
  /* 高度 */
  height: 40px;
  /* 底部外边距 */
  margin-bottom: 10px;
  /* 边框 */
  border: 4px solid rgba(74, 128, 245, 0.2);
  /* 圆形边框 */
  border-radius: 50%;
  /* 顶部边框颜色 */
  border-top-color: #4a80f5;
  /* 旋转动画 */
  animation: spin 1s linear infinite;
}

@keyframes spin {
  /* 起始状态 */
  0% { transform: rotate(0deg); }
  /* 结束状态 */
  100% { transform: rotate(360deg); }
}

/* 创建学科表单对话框样式 */
.form-dialog {
  /* 固定定位 */
  position: fixed;
  /* 顶部对齐 */
  top: 0;
  /* 左侧对齐 */
  left: 0;
  /* 右侧对齐 */
  right: 0;
  /* 底部对齐 */
  bottom: 0;
  /* 半透明背景 */
  background-color: rgba(0, 0, 0, 0.5);
  /* 弹性布局 */
  display: flex;
  /* 水平居中 */
  justify-content: center;
  /* 垂直居中 */
  align-items: center;
  /* 层级 */
  z-index: 1000;
}

.form-dialog-content {
  /* 背景颜色 */
  background-color: white;
  /* 圆角边框 */
  border-radius: 8px;
  /* 宽度 */
  width: 500px;
  /* 阴影效果 */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.form-dialog-header {
  /* 内边距 */
  padding: 15px 20px;
  /* 底部边框 */
  border-bottom: 1px solid #eaeaea;
}

.form-dialog-header h3 {
  /* 移除外边距 */
  margin: 0;
  /* 字体大小 */
  font-size: 18px;
  /* 字体颜色 */
  color: #333;
}

.form-dialog-body {
  /* 内边距 */
  padding: 20px;
}

.form-group {
  /* 底部外边距 */
  margin-bottom: 15px;
}

.form-group label {
  /* 块级显示 */
  display: block;
  /* 底部外边距 */
  margin-bottom: 5px;
  /* 字体粗细 */
  font-weight: 500;
  /* 字体颜色 */
  color: #333;
}

.form-group input,
.form-group textarea {
  /* 宽度 */
  width: 100%;
  /* 内边距 */
  padding: 10px;
  /* 边框 */
  border: 1px solid #ddd;
  /* 圆角边框 */
  border-radius: 4px;
  /* 字体大小 */
  font-size: 14px;
}

.form-group input:focus,
.form-group textarea:focus {
  /* 移除默认轮廓 */
  outline: none;
  /* 聚焦时边框颜色 */
  border-color: #4a80f5;
  /* 聚焦时阴影效果 */
  box-shadow: 0 0 0 2px rgba(74, 128, 245, 0.2);
}

.form-dialog-footer {
  /* 内边距 */
  padding: 15px 20px;
  /* 弹性布局 */
  display: flex;
  /* 靠右对齐 */
  justify-content: flex-end;
  /* 间距 */
  gap: 10px;
  /* 顶部边框 */
  border-top: 1px solid #eaeaea;
}

.create-btn {
  /* 背景颜色 */
  background-color: #4a80f5;
}

.create-btn:hover {
  /* 悬停时背景颜色 */
  background-color: #3a6ad8;
}

.create-btn:disabled {
  /* 禁用时背景颜色 */
  background-color: #a0a0a0;
  /* 禁用时鼠标指针样式 */
  cursor: not-allowed;
}
</style> 