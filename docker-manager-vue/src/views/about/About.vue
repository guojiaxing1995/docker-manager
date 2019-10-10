<template>
  <div class="container">
    <div class="select">
      <label class="select-label">服务器</label>
      <el-select v-model="IP" filterable placeholder="请选择服务器">
        <el-option
          v-for="item in IPList"
          :key="item.value"
          :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>
    </div>
    <div class="information">
      <div class="about">
        <div class="about-title">服务器</div>
        <div class="about-avatar">
          <img src="../../assets/img/about/Docker.png" class="about-avatar-img" />
        </div>
        <div class="about-influence">
          <div class="about-influence-item">
            <div class="about-influence-num color4">19.03.2</div>
            <div class="about-influece-label">docker版本</div>
          </div>
        </div>
        <div class="server-box">
          <div class="about-influence">
            <div class="about-influence-item">
              <div class="about-influence-num color1">guojiaxing</div>
              <div class="about-influece-label">name</div>
            </div>
          </div>
          <div class="about-influence">
            <div class="about-influence-item">
              <div class="about-influence-num color1">CentOS Linux 7 (Core)</div>
              <div class="about-influece-label">操作系统</div>
            </div>
          </div>
          <div class="about-influence">
            <div class="about-influence-item">
              <div class="about-influence-num color1">/var/lib/docker</div>
              <div class="about-influece-label">DockerRootDir</div>
            </div>
          </div>
          <div class="about-influence">
            <div class="about-influence-item">
              <div class="about-influence-num color1">1</div>
              <div class="about-influece-label">cpu</div>
            </div>
            <div class="about-influence-item">
              <div class="about-influence-num color2">2G</div>
              <div class="about-influece-label">内存</div>
            </div>
          </div>
          <div class="about-influence">
            <div class="about-influence-item">
              <div class="about-influece-label">&nbsp; </div>
              <div class="about-influece-label">created by 郭家兴</div>
            </div>
          </div>
        </div>
      </div>
      <div class="about">
        <div class="about-title">容器</div>
        <div class="about-avatar">
          <img src="../../assets/img/about/container.png" class="about-avatar-img" />
        </div>
        <div class="about-influence">
          <div class="about-influence-item">
            <div class="about-influence-num color1">8</div>
            <div class="about-influece-label">运行中</div>
          </div>
          <div class="about-influence-item">
            <div class="about-influence-num color2">2</div>
            <div class="about-influece-label">已停止</div>
          </div>
          <div class="about-influence-item">
            <div class="about-influence-num color3">0</div>
            <div class="about-influece-label">总数</div>
          </div>
        </div>
        <el-tabs v-model="activeName" class="about-tabs" >
            <el-tab-pane label="运行中" class="about-tabs-item" name="one">
              <div class="about-container-box">
                <el-scrollbar style="height:100%">
                  <ul class="about-list" style="overflow: auto;">
                    <li class="about-list-item">
                      <el-tooltip effect="dark" placement="top-start">
                        <div slot="content">撒旦发射点发射点螺ddddddddddddddddddddddddddddddddddddddddd丝钉咖啡碱老师的</div>
                        <span> 撒旦发射ssss丝ddddddddddddddddddddddddddddddddddddddddd顶顶顶顶</span>
                      </el-tooltip>
                    </li>
                    <li class="about-list-item"><span> 撒旦发射ssss丝ddddddddddddddddddddddddddddddddddddddddd顶顶顶顶</span></li>
                    <li class="about-list-item"><span> 撒旦发射ssss丝ddddddddddddddddddddddddddddddddddddddddd顶顶顶顶</span></li>
                    <li class="about-list-item"><span> 撒旦发射ssss丝ddddddddddddddddddddddddddddddddddddddddd顶顶顶顶</span></li>
                    <li class="about-list-item"><span> 撒旦发射ssss丝ddddddddddddddddddddddddddddddddddddddddd顶顶顶顶</span></li>
                    <li class="about-list-item"><span> 撒旦发射ssss丝ddddddddddddddddddddddddddddddddddddddddd顶顶顶顶</span></li>
                    <li class="about-list-item"><span> 撒旦发射ssss丝ddddddddddddddddddddddddddddddddddddddddd顶顶顶顶</span></li>
                    <li class="about-list-item"><span> 撒旦发射ssss丝ddddddddddddddddddddddddddddddddddddddddd顶顶顶顶</span></li>
                    <li class="about-list-item"><span> 撒旦发射ssss丝ddddddddddddddddddddddddddddddddddddddddd顶顶顶顶</span></li>
                    <li class="about-list-item"><span> 撒旦发射ssss丝ddddddddddddddddddddddddddddddddddddddddd顶顶顶顶</span></li>
                    <li class="about-list-item"><span> 撒旦发射ssss丝ddddddddddddddddddddddddddddddddddddddddd顶顶顶顶</span></li>
                    <li class="about-list-item"><span> 撒旦发射ssss丝ddddddddddddddddddddddddddddddddddddddddd顶顶顶顶</span></li>
                    <li class="about-list-item"><span> 撒旦发射ssss丝ddddddddddddddddddddddddddddddddddddddddd顶顶顶顶</span></li>
                    <li class="about-list-item"><span> 撒旦发射ssss丝ddddddddddddddddddddddddddddddddddddddddd顶顶顶顶</span></li>
                  </ul>
                </el-scrollbar>
              </div>
            </el-tab-pane>
            <el-tab-pane label="已停止" class="about-tabs-item" name="two">
              <div class="content">为什么程序员们愿意在GitHub上开源...</div>
            </el-tab-pane>
            <el-tab-pane label="所 有" class="about-tabs-item" name="three">
              <div class="content">为什么程序员们愿意在么程序员们愿意上开么程序员们愿意么程序员们愿意么程序员们愿意么程序员们愿意源...</div>
            </el-tab-pane>
        </el-tabs>
      </div>
      <div class="about">
        <div class="about-title">镜像</div>
        <div class="about-avatar">
          <img src="../../assets/img/about/image.png" class="about-avatar-img" />
        </div>
        <div class="about-influence">
          <div class="about-influence-item">
            <div class="about-influence-num color3">15</div>
            <div class="about-influece-label">总数</div>
          </div>
        </div>
        <div class="about-box">
          <el-scrollbar style="height:100%">
            <ul class="about-list" style="overflow: auto;">
              <li class="about-list-item">
                <el-tooltip effect="dark" placement="top-start">
                  <div slot="content">撒旦发射点发射点螺ddddddddddddddddddddddddddddddddddddddddd丝钉咖啡碱老师的</div>
                  <span> 撒旦发射ssss丝ddddddddddddddddddddddddddddddddddddddddd顶顶顶顶</span>
                </el-tooltip>
              </li>
              <li class="about-list-item"><span> 撒旦发射ssss丝ddddddddddddddddddddddddddddddddddddddddd顶顶顶顶</span></li>
              <li class="about-list-item"><span> 撒旦发射ssss丝ddddddddddddddddddddddddddddddddddddddddd顶顶顶顶</span></li>
              <li class="about-list-item"><span> 撒旦发射ssss丝ddddddddddddddddddddddddddddddddddddddddd顶顶顶顶</span></li>
              <li class="about-list-item"><span> 撒旦发射ssss丝ddddddddddddddddddddddddddddddddddddddddd顶顶顶顶</span></li>
              <li class="about-list-item"><span> 撒旦发射ssss丝ddddddddddddddddddddddddddddddddddddddddd顶顶顶顶</span></li>
              <li class="about-list-item"><span> 撒旦发射ssss丝ddddddddddddddddddddddddddddddddddddddddd顶顶顶顶</span></li>
              <li class="about-list-item"><span> 撒旦发射ssss丝ddddddddddddddddddddddddddddddddddddddddd顶顶顶顶</span></li>
              <li class="about-list-item"><span> 撒旦发射ssss丝ddddddddddddddddddddddddddddddddddddddddd顶顶顶顶</span></li>
              <li class="about-list-item"><span> 撒旦发射ssss丝ddddddddddddddddddddddddddddddddddddddddd顶顶顶顶</span></li>
              <li class="about-list-item"><span> 撒旦发射ssss丝ddddddddddddddddddddddddddddddddddddddddd顶顶顶顶</span></li>
              <li class="about-list-item"><span> 撒旦发射ssss丝ddddddddddddddddddddddddddddddddddddddddd顶顶顶顶</span></li>
              <li class="about-list-item"><span> 撒旦发射ssss丝ddddddddddddddddddddddddddddddddddddddddd顶顶顶顶</span></li>
              <li class="about-list-item"><span> 撒旦发射ssss丝ddddddddddddddddddddddddddddddddddddddddd顶顶顶顶</span></li>
            </ul>
          </el-scrollbar>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      activeName: 'one',
      showTeam: false,
      IPList: [{
        value: 'www.guojiaxing.red',
        label: 'www.guojiaxing.red',
      }, {
        value: '127.0.0.1',
        label: '127.0.0.1',
      }],
      IP: 'www.guojiaxing.red',
    }
  },
  mounted() {
    if (document.body.clientWidth > 1200 && document.body.clientWidth < 1330) {
      this.showTeam = true
    }
    this.getAboutInfo()
  },
  methods: {
    getAboutInfo() {
      axios.get('http://127.0.0.1:5005/v1/client/info')
        .then(this.getInfoSucc)
    },
    getInfoSucc(res) {
      const infoData = res.data
      console.log(infoData)
    },
  },
}
</script>

<style scoped lang="scss">
.container {
  padding: 20px;
  height: 100%;
  .select {
    display: flex;
    align-items: center;
    margin-top: 20px;
    margin-left: 25px;
    .select-label {
      width: 60px
    }
  }
  .information {
    height: 100%;
    display: flex;
    .about {
      min-width: 0;
      width: 33%;
      height: 100%;
      margin: 25px;
      background:rgba(255,255,255,1);
      box-shadow:0px 2px 14px 0px rgba(243,243,243,1);
      border-radius:10px;
      .server-box {
        height: 400px;
        width: 100%;
        margin-top: 50px;
      }
      .about-title {
        margin: 20px 0 10px 20px;
        height: 22px;
        line-height: 22px;
        font-weight: 500;
        color: #596C8E;
        font-size: 16px;
      }
      .about-avatar {
        width: 120px;
        height: 120px;
        margin: 0 auto 30px;
        .about-avatar-img {
          width: 120px;
          box-shadow: 0 0 30px 0 rgb(247, 247, 248);
        }
      }
      .about-influence {
        display: flex;
        justify-content: space-between;
        padding: 0 30px 30px;
        .about-influence-item {
          display: block;
          margin: auto;
          flex-direction: column;
          align-items: center;
          text-align: center;
          .about-influence-num {
            font-size: 30px;
            line-height: 34px;
            &.color1 {
              color: #00C292;
            }
            &.color2 {
              color: rgb(254, 8, 28);
            }
            &.color3 {
              color: #03A9F3;
            }
            &.color4 {
              color: rgb(241, 186, 35);
            }
          }
          .about-influece-label {
            font-size: 14px;
            font-weight: 400;
            color: #8C98AE;
            line-height: 17px;
            margin: auto;
          }
        }
      }
      .about-box{
        height: 450px;
        width: 100%;
        text-indent: 10px;
        .el-scrollbar{
          height: 100%;
          width: 100%;
          padding: 0;
          margin: 0;
          list-style: none;
          .about-list {
            margin:0px;
            padding:0px;
            overflow:hidden;
            .about-list-item {
              width: 100%;
              height: 50px;
              line-height: 50px;
              font-size: 20px;
              background: rgba(255,255,255,1);
              padding: 0px 0px;
              color: #7dbcfc;
              overflow: hidden;/*超出部分隐藏*/
              white-space: nowrap;/*不换行*/
              text-overflow: ellipsis;/*超出部分文字以...显示*/
            }
          }
        }
      }
      .about-container-box{
        height: 377px;
        width: 100%;
        text-indent: 10px;
        .el-scrollbar{
          height: 100%;
          width: 100%;
          padding: 0;
          margin: 0;
          list-style: none;
          .about-list {
            margin:0px;
            padding:0px;
            overflow:hidden;
            .about-list-item {
              width: 100%;
              height: 50px;
              line-height: 50px;
              font-size: 20px;
              background: rgba(255,255,255,1);
              padding: 0px 0px;
              color: #7dbcfc;
              overflow: hidden;/*超出部分隐藏*/
              white-space: nowrap;/*不换行*/
              text-overflow: ellipsis;/*超出部分文字以...显示*/
            }
          }
        }
      }
      .about-container-box /deep/ .el-scrollbar__wrap {
        overflow-x: hidden;
      }
      .about-box /deep/ .el-scrollbar__wrap {
        overflow-x: hidden;
      }
      .about-tabs {
        margin-bottom: 20px;
      }
      .about-tabs /deep/ .is-top {
        display: flex;
        flex: auto;
        justify-content: space-around;
        .el-tabs__nav-next,
        .el-tabs__nav-prev {
          color: aliceblue;
        }
      }
      .about-tabs /deep/ .el-tabs__content {
        text-indent: 20px;
      }
    }
  }
}

@media screen and (max-width: 1200px){
  .container {
    display: none;
  }
  .container {
    width: 100%;
  }
  .container {
    width: 32%;
    &:last-child {
      display: none;
    }
  }
  .container .information .about{
    display: none;
  }
}

@media screen and (max-width: 1200px){
  .container .lin-info .lin-info-left{
    width: 100%;
  }
}
.el-scrollbar__wrap.default-scrollbar__wrap {
  overflow-x: auto;
}
</style>
