<template>
  <!-- 导航项容器组件 -->
  <div class="nav-item-container">
    <!-- 父级导航项 -->
    <!-- 当isParent为true时显示 -->
    <!-- 点击时触发handleParentClick事件 -->
    <!-- parent-active类根据isParentActive动态添加 -->
    <!-- aria-expanded属性用于表示当前导航项是否展开 -->
    <div 
      v-if="isParent"
      class="nav-item"
      :class="{ 'parent-active': isParentActive }"
      :data-expanded="isExpanded"
      @click="handleParentClick"
    >
      <div class="item-content">
        <!-- 如果有图标则显示图标 -->
        <img 
          v-if="icon"
          :src="icon"
          class="menu-icon"
          alt="menu icon"
        />
        <span class="item-label" :class="{ 'no-icon': !icon }">{{ label }}</span>
      </div>
      <!-- 如果有子项则显示展开/收起箭头图标 -->
      <!-- 根据isExpanded状态切换上下箭头 -->
      <img 
        v-if="hasChildren"
        src="../assets/arrow_down.svg"
        class="arrow-icon"
        alt="toggle"
      />
    </div>
    <!-- 子级导航项 -->
    <!-- 当不是父级项时显示 -->
    <!-- 点击时触发handleChildClick事件 -->
    <!-- child-active类根据isChildActive动态添加 -->
    <div 
      v-else
      class="nav-item"
      :class="{ 'child-active': isChildActive }"
      @click="handleChildClick"
    >
      <div class="item-content">
        <img 
          v-if="icon"
          :src="icon"
          class="menu-icon"
          alt="menu icon"
        />
        <span class="item-label" :class="{ 'no-icon': !icon }">{{ label }}</span>
      </div>
    </div>

    <!-- 子导航项列表容器 -->
    <!-- 当有子项且处于展开状态时显示 -->
    <!-- 通过具名插槽children插入子导航项 -->
    <transition name="slide">
      <div 
        v-if="hasChildren && isExpanded"
        class="children-container"
      >
        <slot name="children"></slot>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  // 组件名称
  name: 'NavItem',
  
  // 组件接收的属性定义
  props: {
    // 导航项显示的文本标签
    label: {
      type: String,
      required: true
    },
    // 导航项的唯一标识符
    itemKey: {
      type: String, 
      required: true
    },
    // 是否为父级导航项
    isParent: {
      type: Boolean,
      default: false
    },
    // 是否包含子导航项
    hasChildren: {
      type: Boolean,
      default: false
    },
    // 父级导航项是否处于激活状态
    isParentActive: {
      type: Boolean,
      default: false
    },
    // 子级导航项是否处于激活状态
    isChildActive: {
      type: Boolean,
      default: false
    },
    // 添加图标属性
    icon: {
      type: String,
      default: ''
    }
  },

  // 组件内部数据
  data() {
    return {
      // 控制子导航项是否展开
      isExpanded: false,
    }
  },

  // 组件方法
  methods: {
    // 处理父级导航项点击事件
    handleParentClick() {
      // 如果有子项则切换展开状态
      if (this.hasChildren) {
        this.isExpanded = !this.isExpanded
      }
    },

    // 处理子级导航项点击事件
    handleChildClick() {
    }
  }
}
</script>

<style scoped>
/* 导航项的基本样式 */
.nav-item {
  /* 设置内部填充，左侧留出较大空间用于图标 */
  padding: 15px 10px 15px 50px;
  /* 设置文字颜色为米黄色，提高可读性 */
  color: rgb(244, 236, 184);
  /* 设置鼠标悬停时的指针样式为手型 */
  cursor: pointer;
  /* 添加平滑过渡动画效果 */
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  /* 设置相对定位，作为子元素定位的参考 */
  position: relative;
  /* 使用弹性布局 */
  display: flex;
  /* 垂直方向居中对齐 */
  align-items: center;
  /* 水平方向两端对齐 */
  justify-content: space-between;
  /* 设置透明边框，为激活状态预留空间 */
  border: 2px solid transparent;
  /* 设置外边距，增加项目间的间隔 */
  margin: 4px 4px;
  /* 添加圆角效果，使外观更加柔和 */
  border-radius: 8px;
  /* 添加轻微阴影，增加层次感 */
  box-shadow: 0 1px 2px rgba(0, 14, 66, 0.1);
  /* 设置半透明背景色，营造深邃感 */
  background: rgba(50, 66, 139, 0.1);
}

/* 父级导航项激活时的样式 */
.parent-active {
  /* 设置更亮的背景色，突出显示 */
  background: rgba(106, 132, 212, 0.8);
  /* 添加边框，增加视觉层次 */
  border: 2px solid rgba(244, 236, 184, 0.8);
  /* 添加发光效果，增强视觉冲击力 */
  box-shadow: 0 0 8px rgba(244, 236, 184, 0.6);
  /* 设置相对定位，为伪元素提供定位基准 */
  position: relative;
}

/* 父级导航项激活时左侧装饰条样式 */
.parent-active::before {
  /* 设置伪元素内容为空 */
  content: '';
  /* 使用绝对定位 */
  position: absolute;
  /* 定位到左侧 */
  left: 0px;
  /* 定位到顶部 */
  top: 0;
  /* 延伸到底部 */
  bottom: 0;
  /* 设置装饰条宽度 */
  width: 13px;
  /* 设置装饰条背景色 */
  background: rgb(244, 236, 184);
  /* 添加圆角效果 */
  border-radius: 3px;
  /* 添加发光效果，增强视觉冲击力 */
  box-shadow: 0 0 8px rgba(244, 236, 184, 0.6);
}

/* 子级导航项激活时的样式 */
.child-active {
  /* 设置渐变背景，增加视觉层次 */
  background: linear-gradient(135deg, rgba(78, 99, 185, 0.9), rgba(52, 147, 147, 0.8));
  /* 设置透明边框 */
  border: 2px solid transparent;
  /* 设置背景裁剪方式 */
  background-clip: padding-box;
  /* 设置相对定位 */
  position: relative;
  /* 添加双层阴影效果，增强立体感 */
  box-shadow: 
    0 2px 8px rgba(127, 239, 247, 0.5),
    inset 0 0 12px rgba(255, 255, 255, 0.2);
}

/* 子级导航项激活时的边框渐变效果 */
.child-active::before {
  /* 设置伪元素内容为空 */
  content: '';
  /* 使用绝对定位 */
  position: absolute;
  /* 向上延伸2像素 */
  top: -2px;
  /* 向左延伸2像素 */
  left: -2px;
  /* 向右延伸2像素 */
  right: -2px;
  /* 向下延伸2像素 */
  bottom: -2px;
  /* 设置渐变背景 */
  background: linear-gradient(135deg, rgba(118, 221, 228, 0.8), rgba(217, 210, 168, 0.6));
  /* 添加圆角效果 */
  border-radius: 8px;
  /* 设置层级，确保在内容下方 */
  z-index: -1;
}

/* 导航项悬停时的效果 */
.nav-item:hover {
  /* 设置悬停时的背景色 */
  background: rgba(78, 97, 174, 0.8);
  /* 添加轻微上浮效果 */
  transform: translateY(-1px);
  /* 增加阴影效果 */
  box-shadow: 0 4px 8px rgba(0, 14, 66, 0.2);
  /* 添加边框效果 */
  border: 2px solid rgba(233, 227, 196, 0.8);
}

/* 箭头图标的基本样式 */
.arrow-icon {
  /* 设置图标宽度 */
  width: 16px;
  /* 设置图标高度 */
  height: 16px;
  /* 添加旋转过渡动画 */
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  /* 设置图标颜色滤镜效果 */
  filter: invert(95%) sepia(8%) saturate(10%) hue-rotate(332deg) brightness(150%) contrast(100%);
}

/* 展开状态下箭头的样式 */
.nav-item[data-expanded="true"] .arrow-icon {
  /* 旋转180度 */
  transform: rotate(180deg);
}

/* 子项容器的样式 */
.children-container {
  /* 隐藏溢出内容 */
  overflow: hidden;
}

/* 子菜单展开动画 */
.slide-enter-active,
.slide-leave-active {
  /* 设置过渡动画属性 */
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  /* 设置展开时的最大高度 */
  max-height: 400px;
  /* 设置完全不透明 */
  opacity: 1;
}

/* 子菜单收起动画 */
.slide-enter-from,
.slide-leave-to {
  /* 设置收起时的最大高度为0 */
  max-height: 0;
  /* 设置完全透明 */
  opacity: 0;
  /* 添加向上位移效果 */
  transform: translateY(-10px);
}

/* 导航项文本的样式 */
.item-label {
  /* 设置文字大小 */
  font-size: 16px;
  /* 防止文本换行 */
  white-space: nowrap;
  /* 隐藏溢出内容 */
  overflow: hidden;
  /* 使用省略号显示溢出文本 */
  text-overflow: ellipsis;
  /* 添加过渡效果 */
  transition: all 0.3s ease;
  /* 允许文本占据剩余空间 */
  flex-grow: 1;
}

/* 波纹效果的基本样式 */
.nav-item::after {
  /* 设置伪元素内容为空 */
  content: '';
  /* 使用绝对定位 */
  position: absolute;
  /* 定位到顶部 */
  top: 0;
  /* 定位到左侧 */
  left: 0;
  /* 定位到右侧 */
  right: 0;
  /* 定位到底部 */
  bottom: 0;
  /* 设置径向渐变背景 */
  background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
  /* 初始状态设为透明 */
  opacity: 0;
  /* 添加透明度过渡效果 */
  transition: opacity 0.3s ease;
  /* 设置圆角效果 */
  border-radius: 8px;
}

/* 点击时的波纹效果 */
.nav-item:active::after {
  /* 显示波纹效果 */
  opacity: 1;
}

/* 导航项内容的布局样式 */
.item-content {
  /* 使用弹性布局 */
  display: flex;
  /* 垂直居中对齐 */
  align-items: center;
  /* 设置元素间距 */
  gap: 10px;
}

/* 菜单图标的样式 */
.menu-icon {
  /* 设置图标宽度 */
  width: 20px;
  /* 设置图标高度 */
  height: 20px;
  /* 防止图标被压缩 */
  flex-shrink: 0;
  /* 设置图标颜色滤镜 */
  filter: invert(95%) sepia(8%) saturate(10%) hue-rotate(332deg) brightness(150%) contrast(100%);
}

/* 无图标时文本的样式 */
.item-label.no-icon {
  /* 设置左侧边距，保持对齐 */
  margin-left: 32px;
}
</style>