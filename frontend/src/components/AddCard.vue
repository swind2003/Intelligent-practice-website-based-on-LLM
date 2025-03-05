<template>
  <!-- 添加卡片组件 -->
  <div class="add-card" @click="$emit('click')">
    <div class="card-content">
      <!-- 加号图标 -->
      <div class="add-icon">
        <span class="plus-icon">+</span>
      </div>
      <!-- 添加文本 -->
      <div class="add-text">
        {{ addText }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AddCard',
  props: {
    // 添加按钮文本
    addText: {
      type: String,
      default: '点击添加'
    }
  },
  emits: ['click']
}
</script>

<style scoped>
/* 添加卡片样式 */
.add-card {
  /* 设置背景渐变 */
  background: linear-gradient(135deg, rgba(245, 247, 250, 0.8), rgba(240, 242, 245, 0.6));
  /* 设置虚线边框 */
  border: 2px dashed rgba(74, 144, 226, 0.3);
  /* 设置卡片宽度占满容器 */
  width: 100%;
  /* 设置卡片高度 */
  height: 210px;
  /* 设置边框圆角 */
  border-radius: 16px;
  /* 设置内边距 */
  padding: 20px;
  /* 设置鼠标样式为指针 */
  cursor: pointer;
  /* 设置过渡效果 */
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  /* 设置阴影 */
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04), 
              0 1px 2px rgba(0, 0, 0, 0.02);
  /* 设置文字居中 */
  text-align: center;
  /* 设置相对定位 */
  position: relative;
  /* 设置初始位置 */
  top: 0;
  /* 设置变换原点 */
  transform-origin: center;
  /* 设置溢出隐藏 */
  overflow: hidden;
}

/* 添加卡片内容容器 */
.card-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  gap: 16px;
  position: relative;
  z-index: 2;
}

/* 添加卡片悬停效果 */
.add-card:hover {
  /* 悬停时改变背景渐变 */
  background: linear-gradient(135deg, rgba(240, 249, 255, 0.9), rgba(229, 242, 255, 0.8));
  /* 悬停时改变边框颜色 */
  border-color: rgba(74, 144, 226, 0.6);
  /* 悬停时上移效果 */
  top: -8px;
  /* 悬停时增加阴影 */
  box-shadow: 0 12px 24px rgba(0, 60, 255, 0.06), 
              0 4px 8px rgba(0, 0, 0, 0.03);
}

/* 添加卡片点击效果 */
.add-card:active {
  /* 点击时缩小效果 */
  transform: scale(0.98);
  /* 点击时减少阴影 */
  box-shadow: 0 4px 8px rgba(0, 60, 255, 0.08);
  /* 点击时立即过渡 */
  transition: all 0.1s;
}

/* 添加图标容器样式 */
.add-icon {
  /* 设置宽度 */
  width: 60px;
  /* 设置高度 */
  height: 60px;
  /* 设置边框圆角为50%，形成圆形 */
  border-radius: 50%;
  /* 设置背景渐变 */
  background: linear-gradient(135deg, #4a90e2, #5664bd);
  /* 使用弹性布局 */
  display: flex;
  /* 水平居中对齐 */
  justify-content: center;
  /* 垂直居中对齐 */
  align-items: center;
  /* 设置过渡效果 */
  transition: all 0.3s ease;
  /* 添加阴影效果 */
  box-shadow: 0 4px 10px rgba(74, 144, 226, 0.2);
  /* 设置边框 */
  border: 3px solid rgba(255, 255, 255, 0.8);
  /* 设置缩放 */
  transform: scale(1);
}

/* 加号图标样式 */
.plus-icon {
  /* 设置字体大小 */
  font-size: 32px;
  /* 设置字体颜色 */
  color: white;
  /* 设置字体粗细 */
  font-weight: 300;
  /* 设置行高 */
  line-height: 1;
  /* 设置过渡效果 */
  transition: all 0.3s ease;
  /* 添加文字阴影 */
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  /* 设置固定高度和宽度，确保垂直居中 */
  width: 32px;
  height: 32px;
  /* 向上偏移一点，使视觉上更居中 */
  margin-top: -3px;
}

/* 添加卡片悬停时图标效果 */
.add-card:hover .add-icon {
  /* 悬停时放大效果 */
  transform: scale(1.05);
  /* 悬停时背景效果 */
  background: linear-gradient(135deg, #5a9de8, #6778d0);
  /* 悬停时增加阴影 */
  box-shadow: 0 6px 16px rgba(74, 144, 226, 0.25);
}

/* 添加卡片点击时图标效果 */
.add-card:active .add-icon {
  /* 点击时缩小效果 */
  transform: scale(0.95);
  /* 点击时减少阴影 */
  box-shadow: 0 2px 8px rgba(74, 144, 226, 0.2);
}

/* 添加文本样式 */
.add-text {
  /* 设置字体大小 */
  font-size: 16px;
  /* 设置字体颜色 */
  color: #5a7ba6;
  /* 设置字体粗细 */
  font-weight: 500;
  /* 设置过渡效果 */
  transition: all 0.3s ease;
  /* 添加背景渐变文字 */
  background: linear-gradient(135deg, #4a90e2, #5664bd);
  /* 设置文字背景裁剪 */
  -webkit-background-clip: text;
  background-clip: text;
  /* 设置文字颜色为透明，展示背景 */
  color: transparent;
  /* 添加文字阴影 */
  text-shadow: 0 1px 1px rgba(255, 255, 255, 0.6);
}

/* 添加卡片悬停时文本效果 */
.add-card:hover .add-text {
  /* 悬停时更丰富的渐变 */
  background: linear-gradient(135deg, #3a80d2, #4754ad);
  -webkit-background-clip: text;
  background-clip: text;
  /* 确保文字为透明，显示背景渐变 */
  color: transparent;
  /* 悬停时增加字体粗细 */
  font-weight: 600;
  /* 悬停时放大效果 */
  transform: scale(1.05);
}

/* 添加卡片点击时文本效果 */
.add-card:active .add-text {
  /* 点击时立即过渡 */
  transition: all 0.1s;
}

/* 添加卡片前的装饰效果 */
.add-card::before {
  content: "";
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 20%, transparent 30%);
  opacity: 0;
  pointer-events: none;
  transition: opacity 1.5s ease;
}

/* 添加卡片悬停时的装饰效果 */
.add-card:hover::before {
  opacity: 1;
  animation: ripple 2s infinite linear;
}

/* 波纹动画 */
@keyframes ripple {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style> 