import pluginsConfig from './plugins'
import Utils from '@/lin/utils/util'

// eslint-disable-next-line import/no-mutable-exports
let homeRouter = [
  {
    title: '资源总览',
    type: 'view',
    name: Symbol('about'),
    route: '/about',
    filePath: 'views/about/About.vue',
    inNav: true,
    icon: 'iconfont iconziyuan',
    order: 0,
  },
  {
    title: '镜像管理',
    type: 'view',
    name: Symbol('image'),
    route: '/image',
    filePath: 'views/docker-image/Image.vue',
    inNav: true,
    icon: 'iconfont iconjingxiangguanli',
    order: 1,
  },
  {
    title: '容器管理',
    type: 'view',
    name: Symbol('container'),
    route: '/container',
    filePath: 'views/docker-container/Container.vue',
    inNav: true,
    icon: 'iconfont iconrongqifuwuContainerServi',
    order: 2,
  },
  {
    title: '日志管理',
    type: 'view',
    name: Symbol('log'),
    route: '/log',
    filePath: 'views/log/Log.vue',
    inNav: true,
    icon: 'iconfont icon-rizhiguanli',
    order: 8,
    right: ['查询所有日志'],
  },
  {
    title: '404',
    type: 'view',
    name: Symbol('404'),
    route: '/404',
    filePath: 'views/error-page/404.vue',
    inNav: false,
    icon: 'iconfont icon-rizhiguanli',
  },
]

const plugins = [...pluginsConfig]

// 筛除已经被添加的插件
function filterPlugin(data) {
  if (plugins.length === 0) {
    return
  }
  if (Array.isArray(data)) {
    data.forEach((item) => {
      filterPlugin(item)
    })
  } else {
    const findResult = plugins.findIndex(item => (data === item))
    if (findResult >= 0) {
      plugins.splice(findResult, 1)
    }
    if (data.children) {
      filterPlugin(data.children)
    }
  }
}

filterPlugin(homeRouter)

homeRouter = homeRouter.concat(plugins)

// 处理顺序
homeRouter = Utils.sortByOrder(homeRouter)

// 使用 Symbol 处理 name 字段, 保证唯一性
const deepReduceName = (target) => {
  if (Array.isArray(target)) {
    target.forEach((item) => {
      if (typeof item !== 'object') {
        return
      }
      deepReduceName(item)
    })
    return
  }
  if (typeof target === 'object') {
    if (typeof target.name !== 'symbol') {
      // eslint-disable-next-line no-param-reassign
      target.name = target.name || Utils.getRandomStr()
      // eslint-disable-next-line no-param-reassign
      target.name = Symbol(target.name)
    }

    if (Array.isArray(target.children)) {
      target.children.forEach((item) => {
        if (typeof item !== 'object') {
          return
        }
        deepReduceName(item)
      })
    }
  }
}

deepReduceName(homeRouter)

export default homeRouter
