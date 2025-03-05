import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import AdminHomeView from '../views/AdminHomeView.vue'
import StudentHomeView from '../views/StudentHomeView.vue'
import HomePage from '../views/HomePage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/admin',
      name: 'adminHome',
      component: AdminHomeView,
    },
    {
      path: '/student',
      name: 'studentHome',
      component: StudentHomeView,
    },
    {
      path: '/home',
      name: 'home',
      component: HomePage,
    },
  ],
})

/**
 * 全局前置守卫
 * 用于处理路由跳转前的权限验证、登录状态检查和页面重定向
 */
router.beforeEach((to, from, next) => {
  // ---------------------------
  // 1. 用户信息获取
  // ---------------------------
  // 从会话存储中获取用户ID和用户类型
  // 注意：使用sessionStorage而非localStorage，确保会话结束后信息自动清除
  const userId = sessionStorage.getItem('userId')
  const userType = sessionStorage.getItem('userType')
  
  // 将可能的字符串类型转换为数字，方便后续比较
  // 注意: 后端返回的userType可能是数字或字符串类型
  const userTypeNum = parseInt(userType)
  
  // ---------------------------
  // 2. 登录状态检查
  // ---------------------------
  // 确定哪些路由需要登录才能访问（此处除登录页面外的所有页面）
  const requiresAuth = to.path !== '/'
  
  // 未登录用户的处理：如果访问需要登录的页面但未登录，则重定向到登录页
  if (requiresAuth && (!userId || !userType)) {
    console.log("未登录状态拦截：用户尝试访问需要登录的页面，重定向到登录页")
    next('/')
    return
  }
  
  // ---------------------------
  // 3. 已登录用户的路由处理
  // ---------------------------
  if (userId && userType) {
    // 3.1 登录后访问登录页的重定向逻辑
    // 已登录用户访问登录页时，根据用户类型自动重定向到对应的首页
    if (to.path === '/') {
      // 处理不同用户类型：1=管理员，2=学生
      // 同时兼容数字类型和字符串类型的比较
      if (userTypeNum === 1 || userType === '1') {
        console.log("已登录状态重定向：管理员用户尝试访问登录页，重定向到管理员首页")
        next('/admin')
      } else if (userTypeNum === 2 || userType === '2') {
        console.log("已登录状态重定向：学生用户尝试访问登录页，重定向到学生首页")
        next('/student')
      } else {
        // 处理未知用户类型的情况
        console.warn('未知的用户类型:', userType, '类型:', typeof userType)
        // 由于类型未知，保留在登录页
        next('/')
      }
      return
    }
    
    // ---------------------------
    // 4. 访问权限控制
    // ---------------------------
    // 4.1 管理员页面权限控制
    // 拦截非管理员用户访问管理员页面
    if (to.path.startsWith('/admin') && !(userTypeNum === 1 || userType === '1')) {
      console.log("权限不足拦截：非管理员用户尝试访问管理员页面")
      // 根据用户类型重定向到合适的页面
      next((userTypeNum === 2 || userType === '2') ? '/student' : '/')
      return
    }
    
    // 4.2 学生页面权限控制
    // 拦截非学生用户访问学生页面
    if (to.path.startsWith('/student') && !(userTypeNum === 2 || userType === '2')) {
      console.log("权限不足拦截：非学生用户尝试访问学生页面")
      // 根据用户类型重定向到合适的页面
      next((userTypeNum === 1 || userType === '1') ? '/admin' : '/')
      return
    }
  }
  
  // ---------------------------
  // 5. 默认处理：通过所有检查后放行
  // ---------------------------
  next()
})

export default router
