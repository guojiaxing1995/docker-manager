<template>
  <div class="user">
    <el-dropdown>
      <span class="el-dropdown-link">
        <div class="nav-avatar">
          <img :src="defaultAvatar" alt="头像">
        </div>
      </span>
      <el-dropdown-menu slot="dropdown" class="user-box">
        <div class="user-info">
          <div class="avatar">
            <img :src="defaultAvatar" alt="头像">
          </div>
          <div class="text">
            <div class="username">{{ nickname }}</div>
            <div class="desc">{{ title }}</div>
          </div>
          <img src="../../assets/img/user/corner.png" class="corner">
        </div>
        <ul class="dropdown-box">
          <li class="account" @click="outLogin">
            <i class="iconfont icon-tuichu"></i>
            <span>退出账户</span>
          </li>
        </ul>
      </el-dropdown-menu>
    </el-dropdown>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import defaultAvatar from '@/assets/img/user/user.png'

const width = 150
const height = 150

export default {
  name: 'user',
  components: {},
  data() {
    return {
      nickname: null,
      dialogFormVisible: false,
      form: {
        old_password: '',
        new_password: '',
        confirm_password: '',
      },
      cropRule: {
        width,
        height,
      },
      imgRule: {
        minWidth: width,
        minHeight: height,
      },
      cropVisible: false,
      cropImg: '',
      imgInfo: null,
      quality: 1,
      defaultAvatar,
    }
  },
  computed: {
    title() {
      const { isSuper } = this.user || {}
      if (isSuper) {
        return '超级管理员'
      }
      return '管理员'
    },
    ...mapGetters(['user']),
  },
  watch: {
  },
  created() {
    this.init()
  },
  methods: {
    ...mapActions(['loginOut', 'setUserAndState']),
    init() {
      const { user } = this.$store.state
      this.nickname = user ? user.nickname : 'super'
    },
    changePassword() {
      this.dialogFormVisible = true
    },
    // 弹框 右上角 X
    handleClose(done) {
      this.dialogFormVisible = false
      done()
    },
    outLogin() {
      this.$router.push('/login')
    },
  },
}
</script>

<style lang="scss" scoped>
.user-dialog /deep/ .el-dialog .el-dialog__header {
  border-bottom: 1px solid #dae1ed;
  padding-bottom: 20px;
}

.user-dialog /deep/ .el-dialog .el-dialog__body {
  padding-bottom: 00px;
}

.user {
  height: 40px;
  .el-dropdown-link {
    cursor: pointer;

    .nav-avatar {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      overflow: hidden;
      margin-right: 10px;
    }
  }
}

.user-box {
  width: 326px;
  background-color: none;
  background: transparent;
  margin-bottom: 0;
  padding-bottom: 0;
  border: none;

  .user-info {
    background-image: url("../../assets/img/user/user-bg.png");
    background-size: 100% 100%;
    transform: translateY(-10px);
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    display: flex;
    flex-direction: row;
    padding: 35px 20px 25px 30px;
    z-index: 100;
    position: relative;

    .corner {
      position: absolute;
      right: 18px;
      top: -9px;
      width: 27px;
      height: 10px;
    }

    .avatar {
      width: 80px;
      height: 80px;
      border-radius: 50%;
      overflow: hidden;
      position: relative;

      .mask {
        opacity: 0;
        transition: all .2s;
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, .3);
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        color: white;

        input {
          display: none;
        }
      }

      &:hover {
        .mask {
          opacity: 1;
        }
      }
    }

    .text {
      margin-left: 20px;
      color: #fff;
      display: flex;
      flex-direction: column;
      justify-content: center;

      .username {
        margin-bottom: 10px;
        font-size: 16px;
      }

      .desc {
        font-size: 14px;
        color: rgba(222, 226, 230, 1);
      }
    }
  }

  .dropdown-box {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    padding-left: 35px;
    height: 80px;
    color: #596c8e;
    font-size: 14px;
    background: white;
    margin-top: -10px;

    li {
      cursor: pointer;

      &:nth-child(1) {
        margin-top: 20px;
      }

      &:nth-child(2) {
        margin-bottom: 20px;
      }

      i {
        margin-right: 10px;
      }

      &:hover {
        color: $theme !important;

        i {
          color: $theme !important;
        }
      }
    }
  }
}

.popper__arrow {
  display: none !important;
}

</style>
