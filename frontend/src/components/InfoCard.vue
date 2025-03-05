<template>
  <!-- 信息卡片组件 -->
  <div 
    class="feature-card"
    :class="{ 'selected': selected }"
    @click.stop="$emit('click')"
    :style="cardStyle"
  >
    <!-- 卡片图标 -->
    <div class="card-icon" :style="iconStyle">
      <img :src="icon" :alt="iconAlt" class="icon-image">
    </div>
    <!-- 卡片内容区域 -->
    <div class="card-content">
      <!-- 卡片标题 -->
      <h3 class="card-title" :style="titleStyle">{{ title }}</h3>
      <!-- 卡片描述 -->
      <p class="card-description">{{ description }}</p>
      
      <!-- 卡片操作区域 -->
      <div class="card-actions">
        <!-- 编辑按钮 -->
        <button class="action-button" @click.stop="$emit('edit')" :style="actionButtonStyle">
          <img :src="editIcon" :alt="editBtnText" class="action-icon">
          {{ editBtnText }}
        </button>
        <!-- 分隔线 -->
        <div class="action-divider"></div>
        <!-- 删除按钮 -->
        <button class="action-button delete-button" @click.stop="$emit('delete')">
          <img :src="deleteIcon" :alt="deleteBtnText" class="action-icon">
          {{ deleteBtnText }}
        </button>
      </div>
    </div>
    <!-- 选中标记 -->
    <div v-if="selected" class="selection-mark" :style="{ backgroundColor: color }"></div>
  </div>
</template>

<script>
export default {
  // 组件名称
  name: 'InfoCard',
  // 组件接收的属性
  props: {
    // 卡片ID，可以是数字或字符串类型
    id: {
      type: [Number, String],
      required: true
    },
    // 卡片标题，必须提供
    title: {
      type: String,
      required: true
    },
    // 卡片描述，如果未提供则默认显示"暂无描述"
    description: {
      type: String,
      default: '暂无描述'
    },
    // 卡片图标的URL地址，必须提供
    icon: {
      type: String,
      required: true
    },
    // 图标的替代文本，用于无法显示图片时
    iconAlt: {
      type: String,
      default: '图标'
    },
    // 卡片的主题颜色，默认为蓝色
    color: {
      type: String,
      default: 'rgb(33, 150, 243)'
    },
    // 是否被选中状态，默认为未选中
    selected: {
      type: Boolean,
      default: false
    },
    // 编辑按钮的图标URL，必须提供
    editIcon: {
      type: String,
      required: true
    },
    // 删除按钮的图标URL，必须提供
    deleteIcon: {
      type: String,
      required: true
    },
    // 编辑按钮显示的文本，默认为"编辑"
    editBtnText: {
      type: String,
      default: '编辑'
    },
    // 删除按钮显示的文本，默认为"删除"
    deleteBtnText: {
      type: String,
      default: '删除'
    }
  },
  // 计算属性
  computed: {
    // 动态计算卡片样式，根据是否被选中状态改变边框颜色和阴影
    cardStyle() {
      // 如果卡片被选中
      if (this.selected) {
        // 返回带有特定边框颜色和阴影的样式对象
        return { 
          borderColor: this.color, 
          boxShadow: `0 8px 20px ${this.color}20` 
        }
      }
      // 如果未选中，返回空对象
      return {}
    },
    // 动态计算图标容器的样式，根据选中状态改变背景色
    iconStyle() {
      // 返回背景样式对象
      return { 
        // 如果被选中，使用渐变背景；否则使用纯色背景
        background: this.selected ? 
          `linear-gradient(135deg, ${this.color}, ${this.adjustColor(this.color, -20)})` :
          this.color 
      }
    },
    // 动态计算标题样式，选中时改变颜色
    titleStyle() {
      // 如果卡片被选中
      if (this.selected) {
        // 返回带有特定文本颜色的样式对象
        return { color: this.color }
      }
      // 如果未选中，返回空对象
      return {}
    },
    // 动态计算操作按钮的样式，设置CSS变量用于按钮颜色
    actionButtonStyle() {
      // 返回包含CSS变量的样式对象
      return { 
        // 设置按钮基本颜色
        '--button-color': this.color,
        // 设置按钮悬停时的颜色（稍暗）
        '--button-hover-color': this.adjustColor(this.color, -20)
      }
    }
  },
  // 组件方法
  methods: {
    // 调整颜色亮度的辅助方法
    // color: 原始颜色值
    // amount: 亮度调整量，正值变亮，负值变暗
    adjustColor(color, amount) {
      // 处理 rgb 格式的颜色
      if (color.startsWith('rgb')) {
        // 使用正则表达式提取RGB值
        const rgbMatch = color.match(/\d+/g);
        // 如果成功提取到至少3个数值（R,G,B）
        if (rgbMatch && rgbMatch.length >= 3) {
          // 调整红色值并确保在0-255范围内
          const r = Math.max(0, Math.min(255, parseInt(rgbMatch[0]) + amount));
          // 调整绿色值并确保在0-255范围内
          const g = Math.max(0, Math.min(255, parseInt(rgbMatch[1]) + amount));
          // 调整蓝色值并确保在0-255范围内
          const b = Math.max(0, Math.min(255, parseInt(rgbMatch[2]) + amount));
          // 返回新的RGB颜色字符串
          return `rgb(${r}, ${g}, ${b})`;
        }
      }
      // 如果无法处理颜色格式，返回原始颜色
      return color;
    }
  },
  // 声明组件可以触发的事件
  emits: ['click', 'edit', 'delete']
}
</script>

<style scoped>
/* 信息卡片样式 */
.feature-card {
  /* 使用弹性布局 */
  display: flex;
  /* 设置背景颜色为白色 */
  background: linear-gradient(135deg, #ffffff, #f8f9fa);
  /* 设置边框圆角为16px */
  border-radius: 16px;
  /* 隐藏溢出内容 */
  overflow: hidden;
  /* 添加阴影效果 */
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04), 
              0 1px 2px rgba(0, 0, 0, 0.02);
  /* 添加过渡效果，持续0.4秒，平滑过渡 */
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  /* 设置鼠标指针为手型 */
  cursor: pointer;
  /* 设置边框为2px宽，透明色 */
  border: 2px solid transparent;
  /* 设置固定高度 */
  height: 210px;
  /* 设置相对定位 */
  position: relative;
  /* 设置初始位置 */
  top: 0;
  /* 设置宽度 */
  width: 100%;
}

/* 卡片悬停效果 */
.feature-card:hover {
  /* 向上移动8px */
  top: -8px;
  /* 增强阴影效果 */
  box-shadow: 0 12px 24px rgba(0, 60, 255, 0.06), 
              0 4px 8px rgba(0, 0, 0, 0.03);
  /* 添加边框效果 */
  border-color: rgba(74, 144, 226, 0.3);
}

/* 卡片点击效果 */
.feature-card:active {
  /* 缩小效果 */
  transform: scale(0.98);
  /* 减少阴影 */
  box-shadow: 0 4px 8px rgba(0, 60, 255, 0.08);
  /* 立即过渡 */
  transition: all 0.1s;
}

/* 被选中的卡片样式 */
.feature-card.selected {
  /* 添加轻微缩放效果 */
  transform: scale(1.02);
  /* 添加过渡效果 */
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  /* 设置文字颜色加深 */
  color: #2c3e50;
  /* 添加选中标记 */
  position: relative;
  /* 改变边框状态 */
  border-width: 2px;
  /* 添加阴影光晕 */
  box-shadow: 0 12px 28px rgba(74, 144, 226, 0.08), 
              0 8px 16px rgba(74, 144, 226, 0.06);
}

/* 添加选中标记样式 */
.selection-mark {
  /* 设置绝对定位 */
  position: absolute;
  /* 设置顶部位置为-1px */
  top: -8px;
  /* 设置右侧位置为-1px */
  right: -8px;
  /* 设置宽度为26px */
  width: 26px;
  /* 设置高度为26px */
  height: 26px;
  /* 边框圆角为50%，形成圆形 */
  border-radius: 50%;
  /* 设置边框为2px实线白色 */
  border: 2px solid white;
  /* 添加阴影效果 */
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  /* 设置背景图片为SVG勾选图标 */
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white'%3E%3Cpath d='M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z'/%3E%3C/svg%3E");
  /* 设置背景图片大小为16px */
  background-size: 16px;
  /* 设置背景图片位置为居中 */
  background-position: center;
  /* 设置背景图片不重复 */
  background-repeat: no-repeat;
  /* 添加动画 */
  animation: pop-in 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
  /* 添加 z-index 确保在顶层 */
  z-index: 2;
}

/* 弹出动画 */
@keyframes pop-in {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  80% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
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
  /* 添加过渡效果 */
  transition: all 0.3s ease;
}

/* 选中状态图标容器 */
.feature-card.selected .card-icon {
  /* 增加明亮度 */
  filter: brightness(1.05);
}

/* 图标图片样式 */
.icon-image {
  /* 设置宽度为40px */
  width: 40px;
  /* 设置高度为40px */
  height: 40px;
  /* 添加过渡效果 */
  transition: all 0.3s ease;
  /* 添加滤镜使图标更加明亮 */
  filter: drop-shadow(0 2px 3px rgba(0, 0, 0, 0.08));
}

/* 悬停时图标效果 */
.feature-card:hover .icon-image {
  /* 轻微放大效果 */
  transform: scale(1.05);
}

/* 卡片内容区域样式 */
.card-content {
  /* 设置弹性增长系数为1，占据剩余空间 */
  flex: 1;
  /* 设置内边距为20px */
  padding: 20px;
  /* 设置左侧边框为1px实线淡色 */
  border-left: 1px solid rgba(0, 0, 0, 0.03);
  /* 设置相对定位，用于绝对定位子元素 */
  position: relative;
  /* 设置弹性布局 */
  display: flex;
  /* 设置方向为纵向 */
  flex-direction: column;
  /* 设置内容区域高度为100% */
  height: 100%;
}

/* 选中状态内容区域 */
.feature-card.selected .card-content {
  /* 添加淡色背景 */
  background: linear-gradient(to bottom right, rgba(74, 144, 226, 0.02), rgba(74, 144, 226, 0.04));
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
  color: #2c3e50;
  /* 添加过渡效果 */
  transition: all 0.3s ease;
}

/* 悬停时标题效果 */
.feature-card:hover .card-title {
  /* 添加颜色过渡 */
  color: rgb(74, 144, 226);
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
  padding-right: 8px;
  /* 设置弹性增长 */
  flex-grow: 1;
  /* 添加行高 */
  line-height: 1.5;
}

/* 设置滚动条样式 */
.card-description::-webkit-scrollbar {
  /* 设置滚动条宽度为3px */
  width: 3px;
}

.card-description::-webkit-scrollbar-track {
  /* 设置滚动条轨道背景为浅灰色 */
  background: rgba(241, 241, 241, 0.5);
  /* 设置滚动条轨道边框圆角为1.5px */
  border-radius: 1.5px;
}

.card-description::-webkit-scrollbar-thumb {
  /* 设置滚动条滑块背景为灰色 */
  background: rgba(192, 198, 208, 0.7);
  /* 设置滚动条滑块边框圆角为1.5px */
  border-radius: 1.5px;
}

.card-description::-webkit-scrollbar-thumb:hover {
  /* 设置滚动条滑块悬停时背景为深灰色 */
  background: rgba(160, 166, 176, 0.9);
}

/* 卡片操作区域样式 */
.card-actions {
  /* 使用弹性布局 */
  display: flex;
  /* 设置上边框为1px实线浅色 */
  border-top: 1px solid rgba(0, 0, 0, 0.03);
  /* 设置底部位置固定 */
  position: absolute;
  /* 设置底部位置为0 */
  bottom: 0;
  /* 设置左侧位置为0 */
  left: 0;
  /* 设置右侧位置为0 */
  right: 0;
  /* 设置内边距 */
  padding: 12px 20px;
  /* 确保在最上层 */
  z-index: 2;
  /* 设置背景色，防止透视 */
  background: rgba(255, 255, 255, 0.96);
  /* 添加过渡 */
  transition: background 0.3s ease;
}

/* 选中状态操作区域 */
.feature-card.selected .card-actions {
  /* 添加淡色背景 */
  background: linear-gradient(to right, rgba(74, 144, 226, 0.02), rgba(74, 144, 226, 0.04));
}

/* 操作按钮样式 */
.action-button {
  /* 设置弹性增长系数为1，平均分配空间 */
  flex: 1;
  /* 移除背景 */
  background: none;
  /* 移除边框 */
  border: none;
  /* 设置内边距 */
  padding: 8px 10px;
  /* 设置字体颜色为动态变量 */
  color: var(--button-color, #4a90e2);
  /* 设置字体大小为14px */
  font-size: 14px;
  /* 设置鼠标指针为手型 */
  cursor: pointer;
  /* 添加过渡效果 */
  transition: all 0.2s ease;
  /* 使用弹性布局 */
  display: flex;
  /* 水平居中对齐 */
  justify-content: center;
  /* 垂直居中对齐 */
  align-items: center;
  /* 设置间距 */
  gap: 6px;
  /* 设置圆角 */
  border-radius: 6px;
}

/* 删除按钮特殊颜色 */
.delete-button {
  /* 设置删除按钮颜色 */
  color: #f56c6c;
}

/* 删除按钮悬停效果 */
.delete-button:hover {
  /* 设置悬停时字体颜色为深红色 */
  color: #e74c3c !important;
  /* 设置悬停时背景为淡红色 */
  background: rgba(231, 76, 60, 0.06) !important;
}

/* 操作图标样式 */
.action-icon {
  /* 设置宽度为16px */
  width: 16px;
  /* 设置高度为16px */
  height: 16px;
  /* 添加过渡 */
  transition: all 0.2s;
}

/* 操作按钮悬停效果 */
.action-button:hover {
  /* 设置悬停时字体颜色为深蓝色 */
  color: var(--button-hover-color, #2c5cc5);
  /* 设置悬停时背景为淡蓝色 */
  background: rgba(74, 144, 226, 0.06);
  /* 添加阴影效果 */
  box-shadow: 0 1px 4px rgba(74, 144, 226, 0.1);
  /* 添加字体加粗效果 */
  font-weight: 500;
}

/* 操作按钮悬停时图标效果 */
.action-button:hover .action-icon {
  /* 轻微放大效果 */
  transform: scale(1.05);
}

/* 操作区域分隔线样式 */
.action-divider {
  /* 设置宽度为1px */
  width: 1px;
  /* 设置背景颜色为浅灰色渐变 */
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.02), rgba(0, 0, 0, 0.05), rgba(0, 0, 0, 0.02));
  /* 设置外边距 */
  margin: 0 8px;
}
</style> 