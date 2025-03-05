<template>
  <div class="admin-manage">
    <!-- 学科信息头部 -->
    <div class="subject-header">
      <!-- 学科标题区域 -->
      <div class="subject-title">
        <!-- 显示学科名称 -->
        <h2>{{ subject.name }}</h2>
        <!-- 显示学科描述，如果没有则显示"暂无描述" -->
        <p class="subject-description">{{ subject.description || '暂无描述' }}</p>
      </div>
      <!-- 学科操作按钮区域 -->
      <div class="subject-actions">
        <!-- 编辑学科信息按钮 -->
        <button class="action-button primary-btn">
          <!-- 编辑图标 -->
          <img :src="EditIcon" alt="编辑" class="btn-icon">
          <!-- 按钮文本 -->
          编辑学科信息
        </button>
        <!-- 删除学科按钮 -->
        <button class="action-button danger-btn">
          <!-- 删除图标 -->
          <img :src="DeleteIcon" alt="删除" class="btn-icon">
          <!-- 按钮文本 -->
          删除学科
        </button>
      </div>
    </div>

    <!-- 管理选项卡 -->
    <div class="manage-tabs">
      <!-- 章节管理选项卡 -->
      <div 
        class="tab-item" 
        :class="{ 'active': activeTab === 'chapters' }" 
        @click="activeTab = 'chapters'"
      >
        <!-- 选项卡文本 -->
        章节管理
      </div>
      <!-- 题目管理选项卡 -->
      <div 
        class="tab-item" 
        :class="{ 'active': activeTab === 'questions' }" 
        @click="activeTab = 'questions'"
      >
        <!-- 选项卡文本 -->
        题目管理
      </div>
    </div>

    <!-- 章节管理内容 -->
    <div v-if="activeTab === 'chapters'" class="tab-content chapters-management">
      <!-- 章节列表标题 -->
      <h3 class="section-title">章节列表</h3>
      
      <!-- 章节卡片网格 -->
      <div class="card-grid">
        <!-- 添加章节卡片 -->
        <AddCard 
          addText="点击添加新章节" 
          @click="openCreateChapterForm"
        />
        
        <!-- 章节信息卡片 -->
        <InfoCard
          v-for="chapter in chapters"
          :key="chapter.id"
          :id="chapter.id"
          :title="chapter.name"
          :description="chapter.description"
          :icon="BaseIcon"
          :color="getChapterColor(chapter.id)"
          :selected="selectedChapter === chapter.id"
          :editIcon="EditIcon"
          :deleteIcon="DeleteIcon"
          editBtnText="编辑章节"
          deleteBtnText="删除章节"
          @click="toggleChapter(chapter.id)"
          @edit="editChapter(chapter.id)"
          @delete="deleteChapter(chapter.id)"
        />
      </div>
    </div>

    <!-- 题目管理内容 -->
    <div v-if="activeTab === 'questions'" class="tab-content questions-management">
      <!-- 题目列表头部 -->
      <div class="questions-header">
        <!-- 题目列表标题 -->
        <h3 class="section-title">题目列表</h3>
        
        <!-- 筛选按钮区域 -->
        <div class="filter-section">
          <!-- 筛选按钮 -->
          <button class="filter-btn" @click="showFilter = !showFilter">
            <!-- 筛选图标 -->
            <img :src="FilterIcon" alt="筛选" class="filter-icon">
            <!-- 按钮文本 -->
            筛选
          </button>
        </div>
      </div>
      
      <!-- 筛选面板 -->
      <div class="filter-panel" v-if="showFilter">
        <!-- 筛选表单 -->
        <div class="filter-form">
          <!-- 题目ID筛选组 -->
          <div class="filter-group">
            <!-- 标签 -->
            <label>题目ID</label>
            <!-- 输入框 -->
            <input type="text" v-model="filters.id" placeholder="输入题目ID">
          </div>
          
          <!-- 章节筛选组 -->
          <div class="filter-group">
            <!-- 标签 -->
            <label>章节</label>
            <!-- 下拉选择框 -->
            <select v-model="filters.chapter">
              <!-- 默认选项 -->
              <option value="">全部章节</option>
              <!-- 章节选项列表 -->
              <option v-for="chapter in chapters" :key="chapter.id" :value="chapter.id">
                {{ chapter.name }}
              </option>
            </select>
          </div>
          
          <!-- 题型筛选组 -->
          <div class="filter-group">
            <!-- 标签 -->
            <label>题型</label>
            <!-- 下拉选择框 -->
            <select v-model="filters.type">
              <!-- 默认选项 -->
              <option value="">全部题型</option>
              <!-- 题型选项列表 -->
              <option v-for="type in questionTypes" :key="type.id" :value="type.id">
                {{ type.name }}
              </option>
            </select>
          </div>
          
          <!-- 难度筛选组 -->
          <div class="filter-group">
            <!-- 标签 -->
            <label>难度</label>
            <!-- 下拉选择框 -->
            <select v-model="filters.difficulty">
              <!-- 默认选项 -->
              <option value="">全部难度</option>
              <!-- 难度选项 -->
              <option value="简单">简单</option>
              <!-- 难度选项 -->
              <option value="中等">中等</option>
              <!-- 难度选项 -->
              <option value="困难">困难</option>
            </select>
          </div>
        </div>
      </div>

      <!-- 添加题目按钮容器 -->
      <div class="add-question-container">
        <!-- 添加题目按钮 -->
        <button class="add-question-btn" @click="addQuestion">
          <!-- 添加图标 -->
          <img :src="AddIcon" alt="添加" class="btn-icon">
          <!-- 按钮文本 -->
          添加新题目
        </button>
      </div>
      
      <!-- 题目表格容器 -->
      <div class="questions-table-container">
        <!-- 题目表格 -->
        <table class="questions-table">
          <!-- 表头 -->
          <thead>
            <!-- 表头行 -->
            <tr>
              <!-- ID列标题 -->
              <th>ID</th>
              <!-- 章节列标题 -->
              <th>章节</th>
              <!-- 题型列标题 -->
              <th>题型</th>
              <!-- 难度列标题 -->
              <th>难度</th>
              <!-- 操作列标题 -->
              <th>操作</th>
            </tr>
          </thead>
          <!-- 表格主体 -->
          <tbody>
            <!-- 题目数据行 -->
            <tr v-for="question in filteredQuestions" :key="question.id">
              <!-- ID单元格 -->
              <td>{{ question.id }}</td>
              <!-- 章节名称单元格 -->
              <td>{{ getChapterName(question.chapter_id) }}</td>
              <!-- 题型名称单元格 -->
              <td>{{ getQuestionTypeName(question.question_type_id) }}</td>
              <!-- 难度单元格 -->
              <td>{{ question.difficulty || '未设置' }}</td>
              <!-- 操作按钮单元格 -->
              <td class="action-cell">
                <!-- 编辑按钮 -->
                <button class="table-action-btn edit-btn" @click="editQuestion(question.id)">
                  <!-- 编辑图标 -->
                  <img :src="EditIcon" alt="编辑" class="small-icon">
                </button>
                <!-- 删除按钮 -->
                <button class="table-action-btn delete-btn" @click="deleteQuestion(question.id)">
                  <!-- 删除图标 -->
                  <img :src="DeleteIcon" alt="删除" class="small-icon">
                </button>
              </td>
            </tr>
            <!-- 无数据提示行 -->
            <tr v-if="filteredQuestions.length === 0">
              <!-- 跨列单元格 -->
              <td colspan="5" class="empty-table">暂无符合条件的题目</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 新增章节表单对话框背景 -->
    <div class="modal-backdrop" v-if="showChapterForm" @click="closeChapterForm"></div>
    <!-- 新增章节表单对话框容器 -->
    <div class="modal-container" v-if="showChapterForm">
      <!-- 对话框内容 -->
      <div class="modal-content" @click.stop>
        <!-- 对话框头部 -->
        <div class="modal-header">
          <!-- 对话框标题 -->
          <h3>{{ editingChapter ? '编辑章节' : '创建新章节' }}</h3>
          <!-- 关闭按钮 -->
          <button class="close-button" @click="closeChapterForm">×</button>
        </div>
        <!-- 对话框主体 -->
        <div class="modal-body">
          <!-- 章节名称表单组 -->
          <div class="form-group">
            <!-- 标签 -->
            <label>章节名称</label>
            <!-- 输入框 -->
            <input 
              type="text" 
              v-model="chapterForm.name" 
              placeholder="请输入章节名称"
              :class="{ 'error': chapterFormErrors.name }"
            >
            <!-- 错误信息 -->
            <div class="error-message" v-if="chapterFormErrors.name">{{ chapterFormErrors.name }}</div>
          </div>
          <!-- 章节描述表单组 -->
          <div class="form-group">
            <!-- 标签 -->
            <label>章节描述</label>
            <!-- 文本区域 -->
            <textarea 
              v-model="chapterForm.description" 
              placeholder="请输入章节描述"
              rows="4"
            ></textarea>
          </div>
        </div>
        <!-- 对话框底部 -->
        <div class="modal-footer">
          <!-- 取消按钮 -->
          <button class="cancel-button" @click="closeChapterForm">取消</button>
          <!-- 提交按钮 -->
          <button 
            class="submit-button" 
            :disabled="!chapterForm.name"
            @click="submitChapterForm"
          >
            {{ editingChapter ? '保存修改' : '创建章节' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 确认删除对话框背景 -->
    <div class="modal-backdrop" v-if="showDeleteConfirm" @click="cancelDelete"></div>
    <!-- 确认删除对话框容器 -->
    <div class="modal-container" v-if="showDeleteConfirm">
      <!-- 对话框内容 -->
      <div class="modal-content confirm-modal" @click.stop>
        <!-- 对话框头部 -->
        <div class="modal-header">
          <!-- 对话框标题 -->
          <h3>确认删除</h3>
          <!-- 关闭按钮 -->
          <button class="close-button" @click="cancelDelete">×</button>
        </div>
        <!-- 对话框主体 -->
        <div class="modal-body">
          <!-- 确认信息 -->
          <p>{{ deleteConfirmMessage }}</p>
        </div>
        <!-- 对话框底部 -->
        <div class="modal-footer">
          <!-- 取消按钮 -->
          <button class="cancel-button" @click="cancelDelete">取消</button>
          <!-- 确认删除按钮 -->
          <button class="danger-button" @click="confirmDelete">确认删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// 导入添加卡片组件
import AddCard from './AddCard.vue'
// 导入信息卡片组件
import InfoCard from './InfoCard.vue'
// 导入基础图标
import BaseIcon from '../assets/base_icon.svg'
// 导入编辑图标
import EditIcon from '../assets/edit.svg'
// 导入删除图标
import DeleteIcon from '../assets/delete.svg'
// 导入筛选图标
import FilterIcon from '../assets/filter.svg'
// 导入添加图标
import AddIcon from '../assets/common_add.svg'
// 导入axios用于发送HTTP请求
import axios from 'axios'

export default {
  // 组件名称
  name: 'AdminManage',
  // 注册使用的子组件
  components: {
    // 添加卡片组件
    AddCard,
    // 信息卡片组件
    InfoCard
  },
  // 组件接收的属性
  props: {
    // 学科ID属性
    subjectId: {
      // 类型为数字
      type: Number,
      // 必须传入
      required: true
    }
  },
  // 组件数据
  data() {
    return {
      // 导入的图标
      BaseIcon,
      // 编辑图标
      EditIcon,
      // 删除图标
      DeleteIcon,
      // 筛选图标
      FilterIcon,
      // 添加图标
      AddIcon,
      
      // 学科信息对象
      subject: {},
      
      // 当前激活的标签页
      activeTab: 'chapters',
      
      // 章节列表数组
      chapters: [],
      
      // 选中的章节ID
      selectedChapter: null,
      
      // 题型列表数组
      questionTypes: [],
      
      // 题目列表数组
      questions: [],
      
      // 筛选相关数据
      // 是否显示筛选面板
      showFilter: false,
      // 筛选条件对象
      filters: {
        // 题目ID筛选
        id: '',
        // 章节筛选
        chapter: '',
        // 题型筛选
        type: '',
        // 难度筛选
        difficulty: ''
      },
      
      // 章节表单相关数据
      // 是否显示章节表单
      showChapterForm: false,
      // 正在编辑的章节ID，为null表示新建
      editingChapter: null,
      // 章节表单数据
      chapterForm: {
        // 章节名称
        name: '',
        // 章节描述
        description: ''
      },
      // 章节表单错误信息
      chapterFormErrors: {
        // 名称错误信息
        name: ''
      },
      
      // 删除确认相关数据
      // 是否显示删除确认对话框
      showDeleteConfirm: false,
      // 删除类型：'chapter'或'question'
      deleteType: '',
      // 要删除的项目ID
      deleteId: null,
      // 删除确认提示信息
      deleteConfirmMessage: ''
    }
  },
  // 计算属性
  computed: {
    // 根据筛选条件过滤题目的计算属性
    filteredQuestions() {
      return this.questions.filter(question => {
        // 根据ID筛选
        if (this.filters.id && !question.id.toString().includes(this.filters.id)) {
          return false
        }
        
        // 根据章节筛选
        if (this.filters.chapter && question.chapter_id !== parseInt(this.filters.chapter)) {
          return false
        }
        
        // 根据题型筛选
        if (this.filters.type && question.question_type_id !== parseInt(this.filters.type)) {
          return false
        }
        
        // 根据难度筛选
        if (this.filters.difficulty && question.difficulty !== this.filters.difficulty) {
          return false
        }
        
        // 通过所有筛选条件，返回true
        return true
      })
    }
  },
  // 侦听器
  watch: {
    // 监听学科ID变化，重新加载数据
    subjectId: {
      // 组件创建时立即执行
      immediate: true,
      // 处理函数
      handler(newVal) {
        // 如果有新值，则加载学科数据
        if (newVal) {
          this.loadSubjectData()
        }
      }
    }
  },
  // 方法
  methods: {
    // 加载学科数据的方法
    async loadSubjectData() {
      try {
        // 获取学科信息
        const subjectResponse = await axios.get(`/admin/get_subject/${this.subjectId}`)
        
        // 检查响应状态
        if (subjectResponse.data.code === 200) {
          // 设置学科信息
          this.subject = subjectResponse.data.data
          
          // 获取章节列表
          await this.loadChapters()
          
          // 获取题型列表
          await this.loadQuestionTypes()
          
          // 获取题目列表
          await this.loadQuestions()
        } else {
          // 显示错误消息
          this.$message.error(subjectResponse.data.message)
        }
      } catch (error) {
        // 打印错误日志
        console.error('加载学科数据失败:', error)
        // 显示错误消息
        this.$message.error('加载学科数据失败，请重试')
      }
    },
    
    // 加载章节列表的方法
    async loadChapters() {
      try {
        // 发送请求获取章节列表
        const response = await axios.get(`/admin/get_chapters/${this.subjectId}`)
        
        // 检查响应状态
        if (response.data.code === 200) {
          // 设置章节列表
          this.chapters = response.data.data
        } else {
          // 显示错误消息
          this.$message.error(response.data.message)
        }
      } catch (error) {
        // 打印错误日志
        console.error('加载章节列表失败:', error)
        // 显示错误消息
        this.$message.error('加载章节列表失败，请重试')
      }
    },
    
    // 加载题型列表的方法
    async loadQuestionTypes() {
      try {
        // 发送请求获取题型列表
        const response = await axios.get('/admin/get_question_types/')
        
        // 检查响应状态
        if (response.data.code === 200) {
          // 设置题型列表
          this.questionTypes = response.data.data
        } else {
          // 显示错误消息
          this.$message.error(response.data.message)
        }
      } catch (error) {
        // 打印错误日志
        console.error('加载题型列表失败:', error)
        // 显示错误消息
        this.$message.error('加载题型列表失败，请重试')
      }
    },
    
    // 加载题目列表的方法
    async loadQuestions() {
      try {
        // 发送请求获取题目列表
        const response = await axios.get(`/admin/get_questions/${this.subjectId}`)
        
        // 检查响应状态
        if (response.data.code === 200) {
          // 设置题目列表
          this.questions = response.data.data
        } else {
          // 显示错误消息
          this.$message.error(response.data.message)
        }
      } catch (error) {
        // 打印错误日志
        console.error('加载题目列表失败:', error)
        // 显示错误消息
        this.$message.error('加载题目列表失败，请重试')
      }
    },
    
    // 切换章节选择的方法
    toggleChapter(chapterId) {
      // 如果当前已选中该章节，则取消选择；否则选中该章节
      this.selectedChapter = this.selectedChapter === chapterId ? null : chapterId
    },
    
    // 为章节生成随机颜色的方法
    getChapterColor(chapterId) {
      // 预定义颜色数组
      const colors = [
        'rgb(33, 150, 243)',  // 蓝色
        'rgb(156, 39, 176)',  // 紫色
        'rgb(233, 30, 99)',   // 粉色
        'rgb(244, 67, 54)',   // 红色
        'rgb(0, 188, 212)',   // 青色
        'rgb(255, 87, 34)',   // 橙色
        'rgb(76, 175, 80)',   // 绿色
        'rgb(255, 193, 7)'    // 黄色
      ]
      
      // 使用章节ID作为索引获取颜色
      return colors[chapterId % colors.length]
    },
    
    // 根据章节ID获取章节名称的方法
    getChapterName(chapterId) {
      // 查找对应ID的章节
      const chapter = this.chapters.find(c => c.id === chapterId)
      // 返回章节名称，如果未找到则返回"未知章节"
      return chapter ? chapter.name : '未知章节'
    },
    
    // 根据题型ID获取题型名称的方法
    getQuestionTypeName(typeId) {
      // 查找对应ID的题型
      const type = this.questionTypes.find(t => t.id === typeId)
      // 返回题型名称，如果未找到则返回"未知题型"
      return type ? type.name : '未知题型'
    },
    
    // 打开创建章节表单的方法
    openCreateChapterForm() {
      // 设置为创建模式（非编辑模式）
      this.editingChapter = null
      // 重置表单数据
      this.chapterForm = {
        // 章节名称为空
        name: '',
        // 章节描述为空
        description: ''
      }
      // 重置表单错误信息
      this.chapterFormErrors = {
        // 名称错误信息为空
        name: ''
      }
      // 显示章节表单
      this.showChapterForm = true
    },
    
    // 打开编辑章节表单的方法
    editChapter(chapterId) {
      // 查找要编辑的章节
      const chapter = this.chapters.find(c => c.id === chapterId)
      // 如果找到章节
      if (chapter) {
        // 设置正在编辑的章节ID
        this.editingChapter = chapterId
        // 设置表单数据
        this.chapterForm = {
          // 设置章节名称
          name: chapter.name,
          // 设置章节描述，如果没有则为空字符串
          description: chapter.description || ''
        }
        // 重置表单错误信息
        this.chapterFormErrors = {
          // 名称错误信息为空
          name: ''
        }
        // 显示章节表单
        this.showChapterForm = true
      }
    },
    
    // 关闭章节表单的方法
    closeChapterForm() {
      // 隐藏章节表单
      this.showChapterForm = false
    },
    
    // 提交章节表单的方法
    async submitChapterForm() {
      // 验证表单
      if (!this.chapterForm.name.trim()) {
        // 如果章节名称为空，设置错误信息
        this.chapterFormErrors.name = '章节名称不能为空'
        // 终止提交
        return
      }
      
      try {
        // 声明响应变量
        let response
        
        // 判断是编辑还是创建
        if (this.editingChapter) {
          // 更新章节
          response = await axios.put(`/admin/update_chapter/${this.editingChapter}`, {
            // 章节名称
            name: this.chapterForm.name,
            // 章节描述
            description: this.chapterForm.description
          })
        } else {
          // 创建章节
          response = await axios.post('/admin/create_chapter/', {
            // 学科ID
            subject_id: this.subjectId,
            // 章节名称
            name: this.chapterForm.name,
            // 章节描述
            description: this.chapterForm.description
          })
        }
        
        // 检查响应状态
        if (response.data.code === 200) {
          // 显示成功消息
          this.$message.success(response.data.message)
          // 关闭表单
          this.closeChapterForm()
          // 重新加载章节列表
          this.loadChapters()
        } else {
          // 显示错误消息
          this.$message.error(response.data.message)
          // 如果是名称已存在的错误
          if (response.data.message.includes('已存在')) {
            // 设置表单错误信息
            this.chapterFormErrors.name = '该章节名称已存在'
          }
        }
      } catch (error) {
        // 打印错误日志
        console.error('保存章节失败:', error)
        // 显示错误消息
        this.$message.error('保存章节失败，请重试')
        
        // 检查错误信息
        if (error.response && error.response.data && error.response.data.message) {
          // 如果是名称已存在的错误
          if (error.response.data.message.includes('已存在')) {
            // 设置表单错误信息
            this.chapterFormErrors.name = '该章节名称已存在'
          }
        }
      }
    },
    
    // 删除章节的方法
    deleteChapter(chapterId) {
      // 设置删除类型为章节
      this.deleteType = 'chapter'
      // 设置要删除的章节ID
      this.deleteId = chapterId
      // 设置删除确认信息
      this.deleteConfirmMessage = '确定要删除这个章节吗？该操作不可恢复，章节下的所有题目也将被删除。'
      // 显示删除确认对话框
      this.showDeleteConfirm = true
    },
    
    // 新增题目的方法
    addQuestion() {
      // 待实现：跳转到添加题目页面或打开添加题目对话框
      this.$message.info('添加题目功能待实现')
    },
    
    // 编辑题目的方法
    editQuestion(questionId) {
      // 待实现：跳转到编辑题目页面或打开编辑题目对话框
      this.$message.info(`编辑题目 ${questionId} 功能待实现`)
    },
    
    // 删除题目的方法
    deleteQuestion(questionId) {
      // 设置删除类型为题目
      this.deleteType = 'question'
      // 设置要删除的题目ID
      this.deleteId = questionId
      // 设置删除确认信息
      this.deleteConfirmMessage = '确定要删除这个题目吗？该操作不可恢复。'
      // 显示删除确认对话框
      this.showDeleteConfirm = true
    },
    
    // 取消删除的方法
    cancelDelete() {
      // 隐藏删除确认对话框
      this.showDeleteConfirm = false
      // 重置删除类型
      this.deleteType = ''
      // 重置删除ID
      this.deleteId = null
    },
    
    // 确认删除的方法
    async confirmDelete() {
      try {
        // 声明响应变量
        let response
        
        // 判断删除类型
        if (this.deleteType === 'chapter') {
          // 删除章节
          response = await axios.delete(`/admin/delete_chapter/${this.deleteId}`)
          
          // 检查响应状态
          if (response.data.code === 200) {
            // 显示成功消息
            this.$message.success(response.data.message)
            // 从列表中移除已删除的章节
            this.chapters = this.chapters.filter(c => c.id !== this.deleteId)
            // 如果当前选中的是被删除的章节，则取消选择
            if (this.selectedChapter === this.deleteId) {
              this.selectedChapter = null
            }
          } else {
            // 显示错误消息
            this.$message.error(response.data.message)
          }
        } else if (this.deleteType === 'question') {
          // 删除题目
          response = await axios.delete(`/admin/delete_question/${this.deleteId}`)
          
          // 检查响应状态
          if (response.data.code === 200) {
            // 显示成功消息
            this.$message.success(response.data.message)
            // 从列表中移除已删除的题目
            this.questions = this.questions.filter(q => q.id !== this.deleteId)
          } else {
            // 显示错误消息
            this.$message.error(response.data.message)
          }
        }
        
        // 隐藏删除确认对话框
        this.showDeleteConfirm = false
      } catch (error) {
        // 打印错误日志
        console.error('删除失败:', error)
        // 显示错误消息
        this.$message.error('删除失败，请重试')
      }
    }
  }
}
</script>

<style scoped>
/* 管理组件容器 */
.admin-manage {
  /* 设置宽度为100% */
  width: 100%;
  /* 设置内边距为28px */
  padding: 28px;
  /* 设置线性渐变背景 */
  background: linear-gradient(145deg, #ffffff, #f8f9fa);
  /* 设置圆角为12px */
  border-radius: 12px;
  /* 设置阴影效果 */
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06), 
              0 1px 8px rgba(0, 0, 0, 0.03);
  /* 设置过渡效果 */
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

/* 学科信息头部 */
.subject-header {
  /* 使用弹性布局 */
  display: flex;
  /* 两端对齐 */
  justify-content: space-between;
  /* 顶部对齐 */
  align-items: flex-start;
  /* 底部外边距35px */
  margin-bottom: 35px;
  /* 底部内边距25px */
  padding-bottom: 25px;
  /* 底部边框 */
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

/* 学科标题样式 */
.subject-title h2 {
  /* 设置字体大小为28px */
  font-size: 28px;
  /* 设置外边距 */
  margin: 0 0 12px 0;
  /* 设置文字颜色 */
  color: #303133;
  /* 设置字体粗细 */
  font-weight: 600;
  /* 设置字间距 */
  letter-spacing: -0.5px;
  /* 设置过渡效果 */
  transition: all 0.3s ease;
}

/* 学科描述样式 */
.subject-description {
  /* 设置文字颜色 */
  color: #606266;
  /* 设置外边距 */
  margin: 0;
  /* 设置字体大小 */
  font-size: 16px;
  /* 设置行高 */
  line-height: 1.6;
  /* 设置最大宽度 */
  max-width: 90%;
}

/* 学科操作区域 */
.subject-actions {
  /* 使用弹性布局 */
  display: flex;
  /* 设置间距 */
  gap: 12px;
}

/* 操作按钮样式 */
.action-button {
  /* 使用弹性布局 */
  display: flex;
  /* 垂直居中 */
  align-items: center;
  /* 设置间距 */
  gap: 8px;
  /* 设置内边距 */
  padding: 10px 18px;
  /* 无边框 */
  border: none;
  /* 设置圆角 */
  border-radius: 8px;
  /* 设置鼠标样式 */
  cursor: pointer;
  /* 设置字体大小 */
  font-size: 14px;
  /* 设置字体粗细 */
  font-weight: 500;
  /* 设置过渡效果 */
  transition: all 0.3s ease;
  /* 设置相对定位 */
  position: relative;
  /* 隐藏溢出内容 */
  overflow: hidden;
}

/* 按钮悬停效果前的伪元素 */
.action-button::before {
  /* 设置内容为空 */
  content: '';
  /* 设置绝对定位 */
  position: absolute;
  /* 垂直居中 */
  top: 50%;
  /* 水平居中 */
  left: 50%;
  /* 初始宽度为0 */
  width: 0;
  /* 初始高度为0 */
  height: 0;
  /* 设置背景色 */
  background: rgba(255, 255, 255, 0.1);
  /* 设置圆形 */
  border-radius: 50%;
  /* 设置变换 */
  transform: translate(-50%, -50%);
  /* 设置过渡效果 */
  transition: width 0.6s ease, height 0.6s ease;
  /* 设置层级 */
  z-index: 0;
}

/* 按钮悬停时伪元素的样式 */
.action-button:hover::before {
  /* 设置宽度 */
  width: 300%;
  /* 设置高度 */
  height: 300%;
}

/* 按钮激活状态样式 */
.action-button:active {
  /* 设置缩放效果 */
  transform: scale(0.98);
  /* 设置过渡效果 */
  transition: transform 0.1s ease;
}

/* 按钮图标样式 */
.btn-icon {
  /* 设置宽度 */
  width: 18px;
  /* 设置高度 */
  height: 18px;
  /* 设置层级 */
  z-index: 1;
}

/* 主要按钮样式 */
.primary-btn {
  /* 设置渐变背景 */
  background: linear-gradient(135deg, #4a90e2, #5664bd);
  /* 设置文字颜色 */
  color: white;
  /* 设置阴影 */
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.2);
}

/* 主要按钮悬停样式 */
.primary-btn:hover {
  /* 增强阴影效果 */
  box-shadow: 0 6px 16px rgba(74, 144, 226, 0.3);
}

/* 危险按钮样式 */
.danger-btn {
  /* 设置渐变背景 */
  background: linear-gradient(135deg, #f56c6c, #e74c3c);
  /* 设置文字颜色 */
  color: white;
  /* 设置阴影 */
  box-shadow: 0 4px 12px rgba(245, 108, 108, 0.2);
}

/* 危险按钮悬停样式 */
.danger-btn:hover {
  /* 增强阴影效果 */
  box-shadow: 0 6px 16px rgba(245, 108, 108, 0.3);
}

/* 选项卡导航 */
.manage-tabs {
  /* 使用弹性布局 */
  display: flex;
  /* 设置底部外边距 */
  margin-bottom: 30px;
  /* 设置底部边框 */
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  /* 设置相对定位 */
  position: relative;
}

/* 选项卡项目样式 */
.tab-item {
  /* 设置内边距 */
  padding: 14px 28px;
  /* 设置鼠标样式 */
  cursor: pointer;
  /* 设置字体粗细 */
  font-weight: 500;
  /* 设置文字颜色 */
  color: #909399;
  /* 设置过渡效果 */
  transition: all 0.3s ease;
  /* 设置相对定位 */
  position: relative;
  /* 设置层级 */
  z-index: 1;
  /* 禁止文本选择 */
  user-select: none;
}

/* 激活状态的选项卡样式 */
.tab-item.active {
  /* 设置文字颜色 */
  color: #4a90e2;
  /* 设置字体粗细 */
  font-weight: 600;
}

/* 激活状态选项卡的下划线 */
.tab-item.active::after {
  /* 设置内容为空 */
  content: '';
  /* 设置绝对定位 */
  position: absolute;
  /* 定位到底部 */
  bottom: -2px;
  /* 定位到左侧 */
  left: 0;
  /* 设置宽度 */
  width: 100%;
  /* 设置高度 */
  height: 3px;
  /* 设置渐变背景 */
  background: linear-gradient(90deg, #4a90e2, #5664bd);
  /* 设置上方圆角 */
  border-radius: 3px 3px 0 0;
  /* 设置过渡效果 */
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  /* 设置阴影 */
  box-shadow: 0 -2px 10px rgba(74, 144, 226, 0.2);
}

/* 非激活状态选项卡悬停样式 */
.tab-item:hover:not(.active) {
  /* 设置文字颜色 */
  color: #606266;
}

/* 选项卡激活状态样式 */
.tab-item:active {
  /* 设置缩放效果 */
  transform: scale(0.98);
}

/* 标题样式 */
.section-title {
  /* 设置字体大小 */
  font-size: 20px;
  /* 设置外边距 */
  margin: 0 0 25px 0;
  /* 设置文字颜色 */
  color: #303133;
  /* 设置相对定位 */
  position: relative;
  /* 设置底部内边距 */
  padding-bottom: 10px;
  /* 设置字体粗细 */
  font-weight: 600;
}

/* 标题下划线 */
.section-title::after {
  /* 设置内容为空 */
  content: '';
  /* 设置绝对定位 */
  position: absolute;
  /* 定位到底部 */
  bottom: 0;
  /* 定位到左侧 */
  left: 0;
  /* 设置宽度 */
  width: 40px;
  /* 设置高度 */
  height: 3px;
  /* 设置渐变背景 */
  background: linear-gradient(90deg, #4a90e2, #5664bd);
  /* 设置圆角 */
  border-radius: 3px;
}

/* 章节卡片网格 */
.card-grid {
  /* 使用网格布局 */
  display: grid;
  /* 设置网格列 */
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  /* 设置间距 */
  gap: 25px;
  /* 设置过渡效果 */
  transition: all 0.3s ease;
}

/* 题目管理头部 */
.questions-header {
  /* 使用弹性布局 */
  display: flex;
  /* 两端对齐 */
  justify-content: space-between;
  /* 垂直居中 */
  align-items: center;
  /* 设置底部外边距 */
  margin-bottom: 25px;
}

/* 筛选按钮样式 */
.filter-btn {
  /* 使用弹性布局 */
  display: flex;
  /* 垂直居中 */
  align-items: center;
  /* 设置间距 */
  gap: 8px;
  /* 设置内边距 */
  padding: 10px 18px;
  /* 设置渐变背景 */
  background: linear-gradient(135deg, #f9f9f9, #f2f2f2);
  /* 设置边框 */
  border: 1px solid rgba(0, 0, 0, 0.06);
  /* 设置圆角 */
  border-radius: 8px;
  /* 设置鼠标样式 */
  cursor: pointer;
  /* 设置字体大小 */
  font-size: 14px;
  /* 设置过渡效果 */
  transition: all 0.3s ease;
  /* 设置阴影 */
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

/* 筛选按钮悬停样式 */
.filter-btn:hover {
  /* 设置渐变背景 */
  background: linear-gradient(135deg, #e6f7ff, #e1f0ff);
  /* 设置边框颜色 */
  border-color: rgba(74, 144, 226, 0.3);
  /* 设置文字颜色 */
  color: #4a90e2;
  /* 设置阴影 */
  box-shadow: 0 2px 6px rgba(74, 144, 226, 0.1);
}

/* 筛选图标样式 */
.filter-icon {
  /* 设置宽度 */
  width: 16px;
  /* 设置高度 */
  height: 16px;
  /* 设置过渡效果 */
  transition: transform 0.3s ease;
}

/* 筛选按钮悬停时图标样式 */
.filter-btn:hover .filter-icon {
  /* 设置旋转效果 */
  transform: rotate(90deg);
}

/* 筛选面板样式 */
.filter-panel {
  /* 设置底部外边距 */
  margin-bottom: 25px;
  /* 设置内边距 */
  padding: 20px;
  /* 设置渐变背景 */
  background: linear-gradient(135deg, #f9f9fa, #f5f7fa);
  /* 设置圆角 */
  border-radius: 10px;
  /* 设置边框 */
  border: 1px solid rgba(0, 0, 0, 0.04);
  /* 设置阴影 */
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
  /* 设置动画 */
  animation: slideDown 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  /* 设置相对定位 */
  position: relative;
  /* 隐藏溢出内容 */
  overflow: hidden;
}

/* 定义滑下动画 */
@keyframes slideDown {
  from {
    /* 初始透明度 */
    opacity: 0;
    /* 初始位置 */
    transform: translateY(-20px);
  }
  to {
    /* 最终透明度 */
    opacity: 1;
    /* 最终位置 */
    transform: translateY(0);
  }
}

/* 筛选面板顶部装饰线 */
.filter-panel::before {
  /* 设置内容为空 */
  content: '';
  /* 设置绝对定位 */
  position: absolute;
  /* 定位到顶部 */
  top: 0;
  /* 定位到左侧 */
  left: 0;
  /* 设置宽度 */
  width: 100%;
  /* 设置高度 */
  height: 3px;
  /* 设置渐变背景 */
  background: linear-gradient(90deg, #4a90e2, #5664bd, #4a90e2);
  /* 设置背景大小 */
  background-size: 200% 100%;
  /* 设置动画 */
  animation: gradientMove 3s linear infinite;
}

/* 定义渐变移动动画 */
@keyframes gradientMove {
  0% {
    /* 初始背景位置 */
    background-position: 0% 0%;
  }
  100% {
    /* 最终背景位置 */
    background-position: 100% 0%;
  }
}

/* 筛选表单样式 */
.filter-form {
  /* 使用网格布局 */
  display: grid;
  /* 设置网格列 */
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  /* 设置间距 */
  gap: 20px;
}

/* 筛选组样式 */
.filter-group {
  /* 使用弹性布局 */
  display: flex;
  /* 纵向排列 */
  flex-direction: column;
  /* 设置间距 */
  gap: 8px;
}

/* 筛选组标签样式 */
.filter-group label {
  /* 设置字体大小 */
  font-size: 14px;
  /* 设置文字颜色 */
  color: #606266;
  /* 设置字体粗细 */
  font-weight: 500;
}

/* 筛选组输入框和选择框样式 */
.filter-group input, 
.filter-group select {
  /* 设置内边距 */
  padding: 10px 12px;
  /* 设置边框 */
  border: 1px solid rgba(0, 0, 0, 0.08);
  /* 设置圆角 */
  border-radius: 8px;
  /* 设置字体大小 */
  font-size: 14px;
  /* 设置背景色 */
  background-color: white;
  /* 设置过渡效果 */
  transition: all 0.3s ease;
  /* 设置阴影 */
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
}

/* 筛选组输入框和选择框聚焦样式 */
.filter-group input:focus, 
.filter-group select:focus {
  /* 移除默认轮廓 */
  outline: none;
  /* 设置边框颜色 */
  border-color: #4a90e2;
  /* 设置阴影 */
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
}

/* 添加题目按钮容器 */
.add-question-container {
  /* 设置底部外边距 */
  margin-bottom: 25px;
  /* 使用弹性布局 */
  display: flex;
  /* 右对齐 */
  justify-content: flex-end;
}

/* 添加题目按钮样式 */
.add-question-btn {
  /* 使用弹性布局 */
  display: flex;
  /* 垂直居中 */
  align-items: center;
  /* 设置间距 */
  gap: 8px;
  /* 设置内边距 */
  padding: 12px 20px;
  /* 设置渐变背景 */
  background: linear-gradient(135deg, #4a90e2, #5664bd);
  /* 无边框 */
  border: none;
  /* 设置圆角 */
  border-radius: 8px;
  /* 设置文字颜色 */
  color: white;
  /* 设置鼠标样式 */
  cursor: pointer;
  /* 设置字体大小 */
  font-size: 15px;
  /* 设置字体粗细 */
  font-weight: 500;
  /* 设置过渡效果 */
  transition: all 0.3s ease;
  /* 设置阴影 */
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.2);
  /* 设置相对定位 */
  position: relative;
  /* 隐藏溢出内容 */
  overflow: hidden;
}

/* 添加题目按钮伪元素 */
.add-question-btn::before {
  /* 设置内容为空 */
  content: '';
  /* 设置绝对定位 */
  position: absolute;
  /* 垂直居中 */
  top: 50%;
  /* 水平居中 */
  left: 50%;
  /* 初始宽度为0 */
  width: 0;
  /* 初始高度为0 */
  height: 0;
  /* 设置背景色 */
  background: rgba(255, 255, 255, 0.2);
  /* 设置圆形 */
  border-radius: 50%;
  /* 设置变换 */
  transform: translate(-50%, -50%);
  /* 设置过渡效果 */
  transition: width 0.6s ease, height 0.6s ease;
}

/* 添加题目按钮悬停样式 */
.add-question-btn:hover {
  /* 增强阴影效果 */
  box-shadow: 0 6px 16px rgba(74, 144, 226, 0.3);
  /* 上移效果 */
  transform: translateY(-2px);
}

/* 添加题目按钮悬停时伪元素样式 */
.add-question-btn:hover::before {
  /* 设置宽度 */
  width: 300%;
  /* 设置高度 */
  height: 300%;
}

/* 添加题目按钮激活状态样式 */
.add-question-btn:active {
  /* 设置变换 */
  transform: translateY(0) scale(0.98);
  /* 减弱阴影效果 */
  box-shadow: 0 2px 8px rgba(74, 144, 226, 0.2);
  /* 设置过渡效果 */
  transition: all 0.1s ease;
}

/* 题目表格容器 */
.questions-table-container {
  /* 允许水平滚动 */
  overflow-x: auto;
  /* 设置圆角 */
  border-radius: 10px;
  /* 设置阴影 */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  /* 设置过渡效果 */
  transition: all 0.3s ease;
}

/* 题目表格样式 */
.questions-table {
  /* 设置宽度 */
  width: 100%;
  /* 设置边框折叠模式 */
  border-collapse: separate;
  /* 设置边框间距 */
  border-spacing: 0;
  /* 设置背景色 */
  background: white;
  /* 设置圆角 */
  border-radius: 10px;
  /* 隐藏溢出内容 */
  overflow: hidden;
}

/* 表格单元格样式 */
.questions-table th, 
.questions-table td {
  /* 设置内边距 */
  padding: 14px 20px;
  /* 设置文本左对齐 */
  text-align: left;
  /* 设置底部边框 */
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
  /* 设置过渡效果 */
  transition: all 0.2s ease;
}

/* 表格头部单元格样式 */
.questions-table th {
  /* 设置渐变背景 */
  background: linear-gradient(135deg, #f5f7fa, #f0f2f5);
  /* 设置字体粗细 */
  font-weight: 600;
  /* 设置文字颜色 */
  color: #606266;
  /* 设置粘性定位 */
  position: sticky;
  /* 定位到顶部 */
  top: 0;
  /* 设置层级 */
  z-index: 10;
}

/* 表格行样式 */
.questions-table tr {
  /* 设置相对定位 */
  position: relative;
  /* 设置过渡效果 */
  transition: all 0.2s ease;
}

/* 表格最后一行单元格样式 */
.questions-table tr:last-child td {
  /* 移除底部边框 */
  border-bottom: none;
}

/* 表格行悬停样式 */
.questions-table tr:hover {
  /* 设置背景色 */
  background-color: #f5f7fa;
  /* 设置阴影 */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
  /* 设置层级 */
  z-index: 1;
}

/* 操作单元格样式 */
.action-cell {
  /* 使用弹性布局 */
  display: flex;
  /* 设置间距 */
  gap: 12px;
}

/* 表格操作按钮样式 */
.table-action-btn {
  /* 使用弹性布局 */
  display: flex;
  /* 垂直居中 */
  align-items: center;
  /* 水平居中 */
  justify-content: center;
  /* 设置宽度 */
  width: 34px;
  /* 设置高度 */
  height: 34px;
  /* 无边框 */
  border: none;
  /* 设置圆角 */
  border-radius: 6px;
  /* 设置鼠标样式 */
  cursor: pointer;
  /* 设置过渡效果 */
  transition: all 0.3s ease;
  /* 设置背景色 */
  background-color: white;
  /* 设置相对定位 */
  position: relative;
  /* 隐藏溢出内容 */
  overflow: hidden;
}

/* 表格操作按钮伪元素 */
.table-action-btn::before {
  /* 设置内容为空 */
  content: '';
  /* 设置绝对定位 */
  position: absolute;
  /* 垂直居中 */
  top: 50%;
  /* 水平居中 */
  left: 50%;
  /* 初始宽度为0 */
  width: 0;
  /* 初始高度为0 */
  height: 0;
  /* 设置背景色 */
  background: rgba(255, 255, 255, 0.2);
  /* 设置圆形 */
  border-radius: 50%;
  /* 设置变换 */
  transform: translate(-50%, -50%);
  /* 设置过渡效果 */
  transition: width 0.4s ease, height 0.4s ease;
}

/* 表格操作按钮悬停时伪元素样式 */
.table-action-btn:hover::before {
  /* 设置宽度 */
  width: 120%;
  /* 设置高度 */
  height: 120%;
}

/* 编辑按钮样式 */
.edit-btn {
  /* 设置背景色 */
  background-color: #e6f7ff;
  /* 设置阴影 */
  box-shadow: 0 2px 5px rgba(74, 144, 226, 0.1);
}

/* 编辑按钮悬停样式 */
.edit-btn:hover {
  /* 设置渐变背景 */
  background: linear-gradient(135deg, #e6f7ff, #d1e6ff);
  /* 增强阴影效果 */
  box-shadow: 0 4px 10px rgba(74, 144, 226, 0.15);
  /* 上移效果 */
  transform: translateY(-2px);
}

/* 删除按钮样式 */
.delete-btn {
  /* 设置背景色 */
  background-color: #fff1f0;
  /* 设置阴影 */
  box-shadow: 0 2px 5px rgba(245, 108, 108, 0.1);
}

/* 删除按钮悬停样式 */
.delete-btn:hover {
  /* 设置渐变背景 */
  background: linear-gradient(135deg, #fff1f0, #ffdbd9);
  /* 增强阴影效果 */
  box-shadow: 0 4px 10px rgba(245, 108, 108, 0.15);
  /* 上移效果 */
  transform: translateY(-2px);
}

/* 小图标样式 */
.small-icon {
  /* 设置宽度 */
  width: 16px;
  /* 设置高度 */
  height: 16px;
  /* 设置过渡效果 */
  transition: all 0.3s ease;
}

/* 表格操作按钮悬停时图标样式 */
.table-action-btn:hover .small-icon {
  transform: scale(1.1);
}

/* 空表格样式 */
.empty-table {
  /* 文本居中 */
  text-align: center;
  /* 设置文字颜色 */
  color: #909399;
  /* 设置内边距 */
  padding: 40px 0;
  /* 设置渐变背景 */
  background: linear-gradient(135deg, #f9f9fa, #f5f7fa);
  /* 设置斜体字 */
  font-style: italic;
}

/* 模态框样式 */
.modal-backdrop {
  /* 设置固定定位 */
  position: fixed;
  /* 定位到顶部 */
  top: 0;
  /* 定位到右侧 */
  right: 0;
  /* 定位到底部 */
  bottom: 0;
  /* 定位到左侧 */
  left: 0;
  /* 设置背景颜色 */
  background-color: rgba(0, 0, 0, 0.5);
  /* 设置背景模糊效果 */
  backdrop-filter: blur(3px);
  /* 设置层级 */
  z-index: 999;
  /* 设置动画效果 */
  animation: fadeIn 0.25s ease;
}

/* 淡入动画关键帧 */
@keyframes fadeIn {
  /* 起始状态 */
  from {
    /* 透明度为0 */
    opacity: 0;
  }
  /* 结束状态 */
  to {
    /* 透明度为1 */
    opacity: 1;
  }
}

/* 模态框容器样式 */
.modal-container {
  /* 设置固定定位 */
  position: fixed;
  /* 定位到顶部 */
  top: 0;
  /* 定位到右侧 */
  right: 0;
  /* 定位到底部 */
  bottom: 0;
  /* 定位到左侧 */
  left: 0;
  /* 使用弹性布局 */
  display: flex;
  /* 垂直居中 */
  align-items: center;
  /* 水平居中 */
  justify-content: center;
  /* 设置层级 */
  z-index: 1000;
}

/* 模态框内容样式 */
.modal-content {
  /* 设置宽度 */
  width: 500px;
  /* 设置最大宽度 */
  max-width: 90%;
  /* 设置渐变背景 */
  background: linear-gradient(145deg, #ffffff, #f8f9fa);
  /* 设置圆角 */
  border-radius: 12px;
  /* 设置阴影 */
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1), 0 5px 15px rgba(0, 0, 0, 0.05);
  /* 设置动画效果 */
  animation: modalSlideIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  /* 隐藏溢出内容 */
  overflow: hidden;
  /* 设置变换 */
  transform: translateY(0);
  /* 设置过渡效果 */
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

/* 模态框滑入动画关键帧 */
@keyframes modalSlideIn {
  /* 起始状态 */
  from {
    /* 透明度为0 */
    opacity: 0;
    /* 向下移动并缩小 */
    transform: translateY(30px) scale(0.95);
  }
  /* 结束状态 */
  to {
    /* 透明度为1 */
    opacity: 1;
    /* 恢复原位并恢复大小 */
    transform: translateY(0) scale(1);
  }
}

/* 确认模态框样式 */
.confirm-modal {
  /* 设置宽度 */
  width: 400px;
}

/* 模态框头部样式 */
.modal-header {
  /* 使用弹性布局 */
  display: flex;
  /* 两端对齐 */
  justify-content: space-between;
  /* 垂直居中 */
  align-items: center;
  /* 设置内边距 */
  padding: 18px 24px;
  /* 设置底部边框 */
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
  /* 设置渐变背景 */
  background: linear-gradient(135deg, #f9fafc, #f5f7fa);
}

/* 模态框标题样式 */
.modal-header h3 {
  /* 设置外边距为0 */
  margin: 0;
  /* 设置字体大小 */
  font-size: 20px;
  /* 设置文字颜色 */
  color: #303133;
  /* 设置字体粗细 */
  font-weight: 600;
}

/* 关闭按钮样式 */
.close-button {
  /* 无边框 */
  border: none;
  /* 无背景 */
  background: none;
  /* 设置字体大小 */
  font-size: 24px;
  /* 设置鼠标样式 */
  cursor: pointer;
  /* 设置文字颜色 */
  color: #909399;
  /* 设置过渡效果 */
  transition: all 0.3s ease;
  /* 设置宽度 */
  width: 36px;
  /* 设置高度 */
  height: 36px;
  /* 使用弹性布局 */
  display: flex;
  /* 垂直居中 */
  align-items: center;
  /* 水平居中 */
  justify-content: center;
  /* 设置圆角 */
  border-radius: 50%;
}

/* 关闭按钮悬停样式 */
.close-button:hover {
  /* 设置文字颜色 */
  color: #303133;
  /* 设置背景颜色 */
  background-color: rgba(0, 0, 0, 0.05);
  /* 设置旋转效果 */
  transform: rotate(90deg);
}

/* 模态框主体样式 */
.modal-body {
  /* 设置内边距 */
  padding: 24px;
}

/* 表单组样式 */
.form-group {
  /* 设置底部外边距 */
  margin-bottom: 20px;
}

/* 表单标签样式 */
.form-group label {
  /* 设置为块级元素 */
  display: block;
  /* 设置底部外边距 */
  margin-bottom: 8px;
  /* 设置字体粗细 */
  font-weight: 500;
  /* 设置文字颜色 */
  color: #606266;
  /* 设置字体大小 */
  font-size: 15px;
}

/* 表单输入框和文本域样式 */
.form-group input, 
.form-group textarea {
  /* 设置宽度为100% */
  width: 100%;
  /* 设置内边距 */
  padding: 12px 15px;
  /* 设置边框 */
  border: 1px solid rgba(0, 0, 0, 0.08);
  /* 设置圆角 */
  border-radius: 8px;
  /* 设置字体大小 */
  font-size: 15px;
  /* 设置背景颜色 */
  background: white;
  /* 设置过渡效果 */
  transition: all 0.3s ease;
  /* 设置阴影 */
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
}

/* 表单输入框和文本域焦点样式 */
.form-group input:focus, 
.form-group textarea:focus {
  /* 移除默认轮廓 */
  outline: none;
  /* 设置边框颜色 */
  border-color: #4a90e2;
  /* 设置阴影 */
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
}

/* 错误表单样式 */
.form-group .error {
  /* 设置边框颜色 */
  border-color: #f56c6c;
  /* 设置背景颜色 */
  background-color: #fff8f8;
}

/* 错误信息样式 */
.error-message {
  /* 设置顶部外边距 */
  margin-top: 6px;
  /* 设置文字颜色 */
  color: #f56c6c;
  /* 设置字体大小 */
  font-size: 13px;
  /* 使用弹性布局 */
  display: flex;
  /* 垂直居中 */
  align-items: center;
  /* 设置间距 */
  gap: 6px;
}

/* 错误信息前的图标 */
.error-message::before {
  /* 设置内容 */
  content: '!';
  /* 使用内联弹性布局 */
  display: inline-flex;
  /* 垂直居中 */
  align-items: center;
  /* 水平居中 */
  justify-content: center;
  /* 设置宽度 */
  width: 16px;
  /* 设置高度 */
  height: 16px;
  /* 设置背景颜色 */
  background-color: #f56c6c;
  /* 设置文字颜色 */
  color: white;
  /* 设置圆角 */
  border-radius: 50%;
  /* 设置字体大小 */
  font-size: 12px;
  /* 设置字体粗细 */
  font-weight: bold;
}

/* 模态框底部样式 */
.modal-footer {
  /* 设置内边距 */
  padding: 18px 24px;
  /* 使用弹性布局 */
  display: flex;
  /* 靠右对齐 */
  justify-content: flex-end;
  /* 设置间距 */
  gap: 12px;
  /* 设置顶部边框 */
  border-top: 1px solid rgba(0, 0, 0, 0.04);
  /* 设置渐变背景 */
  background: linear-gradient(135deg, #f9fafc, #f5f7fa);
}

/* 取消、提交和危险按钮共同样式 */
.cancel-button, .submit-button, .danger-button {
  /* 设置内边距 */
  padding: 10px 20px;
  /* 设置圆角 */
  border-radius: 8px;
  /* 设置字体大小 */
  font-size: 15px;
  /* 设置字体粗细 */
  font-weight: 500;
  /* 设置鼠标样式 */
  cursor: pointer;
  /* 设置过渡效果 */
  transition: all 0.3s ease;
  /* 设置相对定位 */
  position: relative;
  /* 隐藏溢出内容 */
  overflow: hidden;
}

/* 按钮悬停效果前的伪元素 */
.cancel-button::before, .submit-button::before, .danger-button::before {
  /* 设置内容为空 */
  content: '';
  /* 设置绝对定位 */
  position: absolute;
  /* 垂直居中 */
  top: 50%;
  /* 水平居中 */
  left: 50%;
  /* 初始宽度为0 */
  width: 0;
  /* 初始高度为0 */
  height: 0;
  /* 设置背景色 */
  background: rgba(255, 255, 255, 0.1);
  /* 设置圆形 */
  border-radius: 50%;
  /* 设置变换 */
  transform: translate(-50%, -50%);
  /* 设置过渡效果 */
  transition: width 0.6s ease, height 0.6s ease;
  /* 设置层级 */
  z-index: 0;
}

/* 按钮悬停时伪元素的样式 */
.cancel-button:hover::before, .submit-button:hover::before, .danger-button:hover::before {
  /* 设置宽度 */
  width: 300%;
  /* 设置高度 */
  height: 300%;
}

/* 取消按钮样式 */
.cancel-button {
  /* 设置边框 */
  border: 1px solid rgba(0, 0, 0, 0.08);
  /* 设置背景颜色 */
  background: white;
  /* 设置文字颜色 */
  color: #606266;
  /* 设置阴影 */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.03);
}

/* 取消按钮悬停样式 */
.cancel-button:hover {
  /* 设置背景颜色 */
  background-color: #f5f7fa;
  /* 设置阴影 */
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05);
}

/* 提交按钮样式 */
.submit-button {
  /* 无边框 */
  border: none;
  /* 设置渐变背景 */
  background: linear-gradient(135deg, #4a90e2, #5664bd);
  /* 设置文字颜色 */
  color: white;
  /* 设置阴影 */
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.2);
}

/* 提交按钮悬停样式 */
.submit-button:hover {
  /* 增强阴影效果 */
  box-shadow: 0 6px 16px rgba(74, 144, 226, 0.3);
  /* 上移效果 */
  transform: translateY(-2px);
}

/* 按钮激活状态样式 */
.submit-button:active, .cancel-button:active, .danger-button:active {
  /* 设置缩放效果 */
  transform: scale(0.98);
  /* 设置过渡效果 */
  transition: transform 0.1s ease;
}

/* 禁用的提交按钮样式 */
.submit-button:disabled {
  /* 设置渐变背景 */
  background: linear-gradient(135deg, #cbd2e0, #c0c4cc);
  /* 设置鼠标样式 */
  cursor: not-allowed;
  /* 移除阴影 */
  box-shadow: none;
  /* 移除变换 */
  transform: none;
}

/* 危险按钮样式 */
.danger-button {
  /* 无边框 */
  border: none;
  /* 设置渐变背景 */
  background: linear-gradient(135deg, #f56c6c, #e74c3c);
  /* 设置文字颜色 */
  color: white;
  /* 设置阴影 */
  box-shadow: 0 4px 12px rgba(245, 108, 108, 0.2);
}

/* 危险按钮悬停样式 */
.danger-button:hover {
  /* 增强阴影效果 */
  box-shadow: 0 6px 16px rgba(245, 108, 108, 0.3);
  /* 上移效果 */
  transform: translateY(-2px);
}

/* 添加响应式设计 */
@media (max-width: 768px) {
  /* 学科头部在小屏幕上的样式 */
  .subject-header {
    /* 改为纵向排列 */
    flex-direction: column;
    /* 设置间距 */
    gap: 20px;
  }
  
  /* 学科描述在小屏幕上的样式 */
  .subject-description {
    /* 设置最大宽度 */
    max-width: 100%;
  }
  
  /* 筛选表单在小屏幕上的样式 */
  .filter-form {
    /* 改为单列布局 */
    grid-template-columns: 1fr;
  }
  
  /* 卡片网格在小屏幕上的样式 */
  .card-grid {
    /* 改为单列布局 */
    grid-template-columns: 1fr;
  }
  
  /* 模态框内容在小屏幕上的样式 */
  .modal-content {
    /* 设置宽度 */
    width: 95%;
    /* 移除最大宽度限制 */
    max-width: none;
  }
}
</style> 