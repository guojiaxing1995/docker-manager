<template>
  <div class="login">
    <div class="team-name">
      <img src="@/assets/img/login/team-name.png" alt="">
    </div>
    <div class="form-box" v-loading="loading" element-loading-background="rgba(0, 0, 0, 0)">
      <div class="title">
        <h1 title="docker manager">docker manager</h1>
      </div>
      <form class="login-form" autocomplete="off" @submit.prevent="throttleLogin()">
        <div class="form-item nickname">
          <span class="icon account-icon"></span>
          <input type="text"
                 v-model="form.nickname"
                 autocomplete="off"
                 placeholder="请填写用户名">
        </div>
        <div class="form-item password">
          <span class="icon secret-icon"></span>
          <input type="password"
                 v-model="form.password"
                 autocomplete="off"
                 placeholder="请填写密码">
        </div>
        <button class="submit-btn" type="submit">登录</button>
      </form>
    </div>
  </div>
</template>

<script>
import User from '@/lin/models/user'
import Utils from '@/lin/utils/util'
import { mapActions, mapMutations } from 'vuex'

export default {
  name: 'login',
  data() {
    return {
      loading: false, // 加载动画
      wait: 2000, // 2000ms之内不能重复发起请求
      throttleLogin: null, // 节流登录
      form: {
        nickname: 'super',
        password: '123456',
        confirm_password: '',
      },
    }
  },
  methods: {
    async login() {
      const { nickname, password } = this.form
      try {
        this.loading = true
        if (nickname === 'super' && password === '123456') {
          this.$router.push('/about')
          this.$message.success('登录成功')
        } else {
          this.$message.error('用户名或密码错误请重试')
        }
        this.loading = false
      } catch (e) {
        this.loading = false
        console.log(e)
      }
    },
    async getInformation() {
      try {
        // 尝试获取当前用户信息
        const user = await User.getAuths()
        this.setUserAndState(user)
        this.setUserAuths(user.auths)
      } catch (e) {
        console.log(e)
      }
    },
    async register() {
      const obj = {
        data: {
          nickname: this.nickname,
          password: this.password,
          confirm_password: this.confirm_password,
          email: this.email,
        },
      }
      try {
        await User.register(obj)
        this.$message.success('注册成功！')
      } catch (e) {
        console.log(e)
      }
    },
    ...mapActions(['setUserAndState']),
    ...mapMutations({
      setUserAuths: 'SET_USER_AUTHS',
    }),
  },
  created() {
    // 节流登录
    this.throttleLogin = Utils.throttle(this.login, this.wait)
  },
  components: {},
}
</script>

<style lang="scss">
.login {
  width: 100%;
  height: 100%;
  background-size: auto;
  background: #1b2c5f url("../../assets/img/login/login-ba.png") no-repeat center center;

  .team-name {
    position: fixed;
    left: 40px;
    top: 50%;
    width: 50px;
    transform: translateY(-50%);
  }

  .form-box {
    position: fixed;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 445px;

    .title {
      height: 37px;
      font-size: 30px;
      line-height: 37px;
      margin-bottom: 15%;

      h1 {
        // padding-left: 85px;
        box-sizing: border-box;
        text-align: center;
        color: #8c98ae;
      }
    }

    .login-form {
      width: 100%;

      .form-item {
        width: 100%;
        height: 40px;
        box-sizing: border-box;
        padding-bottom: 13px;
        margin-bottom: 34px;

        input {
          width: 100%;
          height: 100%;
          background: transparent;
          color: #c4c9d2;
          font-size: 14px;
          padding-left: 74px;
          box-sizing: border-box;
        }
      }

      .form-item.nickname {
        background: url("../../assets/img/login/nickname.png") no-repeat;
        background-size: 100% auto;
        background-position: left bottom;
      }

      .form-item.password {
        background: url("../../assets/img/login/password.png") no-repeat;
        background-size: 100% auto;
        background-position: left bottom;
      }

      .submit-btn {
        width: 100%;
        height: 70px;
        color: #c4c9d2;
        font-size: 16px;
        text-align: left;
        box-sizing: border-box;
        padding: 0 10px;
        padding-left: 74px;
        background: url("../../assets/img/login/login-btn.png") no-repeat;
        background-size: 90% auto;
        background-position: center bottom;
        border: none;
        cursor: pointer;
      }
    }
  }
  .record {
    position: fixed;
    left: 50%;
    transform: translate(-50%, -50%);
    bottom: 1%;
  }
}
</style>
