<template>
    <div class="user-nav-bar-container">
        <ul class="user-nav-bar">
            <li class="slide1"></li>
            <li class="slide2"></li>
            <li><a href="#" class="nav-bar-link" v-nav-hover @click.prevent="handleClick(1)">首页</a></li>
            <li><a href="#" class="nav-bar-link" v-nav-hover @click.prevent="handleClick(2)">学科广场</a></li>
            <li><a href="#" class="nav-bar-link" v-nav-hover @click.prevent="handleClick(3)">我的学科</a></li>
            <li><a href="#" class="nav-bar-link" v-nav-hover @click.prevent="handleClick(4)">数据统计</a></li>
        </ul>
    </div>
</template>

<script>
export default {
  name: 'UserNavBar',
  data() {
    return {
      activeIndex: 1 // 默认选
    }
  },
  mounted() {
    // 在组件挂载后，初始化滑块位置到默认选中项
    this.$nextTick(() => {
      this.initializeSlider()
    })
  },
  methods: {
    // 处理点击事件
    handleClick(index) {
      this.activeIndex = index
      // 获取选中项的位置和宽度
      const element = this.$el.querySelector(`li:nth-of-type(${index + 2}) a`)
      const position = this.getElementPosition(element)
      const width = element.offsetWidth
      
      // 设置slide1的位置和宽度
      const slide1 = this.$el.querySelector('.slide1')
      slide1.style.opacity = '1'
      slide1.style.left = position.left + 'px'
      slide1.style.width = width + 'px'
    },
    
    // 初始化滑块位置
    initializeSlider() {
      // 获取默认选中项的位置和宽度
      const element = this.$el.querySelector(`li:nth-of-type(${this.activeIndex + 2}) a`)
      const position = this.getElementPosition(element)
      const width = element.offsetWidth
      
      // 设置slide1的位置和宽度
      const slide1 = this.$el.querySelector('.slide1')
      slide1.style.opacity = '1'
      slide1.style.left = position.left + 'px'
      slide1.style.width = width + 'px'
    },
    
    // 获取元素相对于父元素的位置
    getElementPosition(element) {
      const parent = element.closest('.user-nav-bar')
      return {
        left: element.offsetLeft,
        top: element.offsetTop
      }
    }
  },
  directives: {
    // 自定义指令处理悬停效果
    navHover: {
      mounted(el, binding, vnode) {
        // 鼠标悬停事件
        el.addEventListener('mouseover', function() {
          const position = {
            left: el.offsetLeft,
            top: el.offsetTop
          }
          const width = el.offsetWidth
          
          // 设置slide2的位置和宽度
          const slide2 = el.closest('.user-nav-bar').querySelector('.slide2')
          slide2.style.opacity = '1'
          slide2.style.left = position.left + 'px'
          slide2.style.width = width + 'px'
          slide2.classList.add('squeeze')
        })
        
        // 鼠标离开事件
        el.addEventListener('mouseout', function() {
          const slide2 = el.closest('.user-nav-bar').querySelector('.slide2')
          slide2.style.opacity = '0'
          slide2.classList.remove('squeeze')
        })
      }
    }
  }
}
</script>

<style scoped>
.user-nav-bar-container {
    width: 50%;
    height: 100%;
    /* 水平居中 */
    margin: 0 auto;
}

.user-nav-bar {
    position: relative;
    border: none;
    border-radius: 10px;
    display: flex;
    background-color: #f5f5f5;
    box-shadow: 20px 40px 40px 0 rgba(0, 0, 0, 0.1);
    padding: 10px;
    list-style: none;
    margin: 0;
}

.nav-bar-link {
    position: relative;
    padding: 15px 50px;
    font-size: 20px;
    font-weight: 500;
    color: #000;
    font-family: "Microsoft YaHei";
    display: inline-block;
    text-decoration: none;
    z-index: 3;
}

.slide1, .slide2 {
    position: absolute;
    display: inline-block;
    height: 60px;
    border-radius: 10%;
    transition: all 0.6s cubic-bezier(0.23, 1, 0.32, 1.075);
}

.slide1 {
    background-color: rgba(170, 190, 255, 1);
    z-index: 2;
}

.slide2 {
    opacity: 0;
    background-color: rgba(170, 190, 255, 0.5);
    z-index: 1;
    box-shadow: 0 0 20px #ffffffaa inset;
}

.squeeze {
    transform: scale(0.9);
}
</style>
