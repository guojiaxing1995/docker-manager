<template>
  <div class="container">
    <div class="select">
      <label class="select-label">服务器</label>
      <el-select v-model="host" filterable placeholder="请选择服务器">
        <el-option
          v-for="item in hostList"
          :key="item.value"
          :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>
      <div class="select-btn">
        <el-button type="primary" plain :loading="imageLoading" @click="handleRefresh">刷 新</el-button>
      </div>
    </div>
    <div class="information">
      <div class="about">
        <div class="about-title">服务器</div>
        <div class="about-avatar">
          <img src="../../assets/img/about/Docker.png" class="about-avatar-img" />
        </div>
        <div class="about-influence">
          <div class="about-influence-item">
            <div class="about-influence-num color4">{{ServerVersion}}</div>
            <div class="about-influece-label">docker版本</div>
          </div>
        </div>
        <div class="server-box">
          <div class="about-influence">
            <div class="about-influence-item">
              <div class="about-influence-num color1">{{Name}}</div>
              <div class="about-influece-label">name</div>
            </div>
          </div>
          <div class="about-influence">
            <div class="about-influence-item">
              <div class="about-influence-num color1">{{OperatingSystem}}</div>
              <div class="about-influece-label">操作系统</div>
            </div>
          </div>
          <div class="about-influence">
            <div class="about-influence-item">
              <div class="about-influence-num color1">{{DockerRootDir}}</div>
              <div class="about-influece-label">DockerRootDir</div>
            </div>
          </div>
          <div class="about-influence">
            <div class="about-influence-item">
              <div class="about-influence-num color1">{{NCPU}}核</div>
              <div class="about-influece-label">cpu</div>
            </div>
            <div class="about-influence-item">
              <div class="about-influence-num color1">{{MemTotal}}G</div>
              <div class="about-influece-label">内存</div>
            </div>
          </div>
          <div class="about-influence">
            <div class="about-influence-item">
              <div class="about-influece-label">&nbsp; </div>
              <el-link type="primary" :underline="false" href="https://github.com/guojiaxing1995/docker-manager" target="_blank">created by 郭家兴</el-link>
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
            <div class="about-influence-num color1">{{ContainersRunning}}</div>
            <div class="about-influece-label">运行中</div>
          </div>
          <div class="about-influence-item">
            <div class="about-influence-num color2">{{ContainersStopped}}</div>
            <div class="about-influece-label">已停止</div>
          </div>
          <div class="about-influence-item">
            <div class="about-influence-num color3">{{Containers}}</div>
            <div class="about-influece-label">总数</div>
          </div>
        </div>
        <el-tabs v-model="activeName" class="about-tabs" >
            <el-tab-pane label="运行中" class="about-tabs-item" name="one">
              <div class="about-container-box" v-loading="containerLoading">
                <el-scrollbar style="height:100%">
                  <ul class="about-list" style="overflow: auto;">
                    <li class="about-list-item" v-for="item of running_list" :key="item">
                      <el-tooltip effect="dark" placement="top-start">
                        <div slot="content">{{item}}</div>
                        <span>{{item}}</span>
                      </el-tooltip>
                    </li>
                  </ul>
                </el-scrollbar>
              </div>
            </el-tab-pane>
            <el-tab-pane label="已停止" class="about-tabs-item" name="two">
              <div class="about-container-box" v-loading="containerLoading">
                <el-scrollbar style="height:100%">
                  <ul class="about-list" style="overflow: auto;">
                    <li class="about-list-item" v-for="item of exited_list" :key="item">
                      <el-tooltip effect="dark" placement="top-start">
                        <div slot="content">{{item}}</div>
                        <span>{{item}}</span>
                      </el-tooltip>
                    </li>
                  </ul>
                </el-scrollbar>
              </div>
            </el-tab-pane>
            <el-tab-pane label="所 有" class="about-tabs-item" name="three">
              <div class="about-container-box" v-loading="containerLoading">
                <el-scrollbar style="height:100%">
                  <ul class="about-list" style="overflow: auto;">
                    <li class="about-list-item" v-for="item of all_list" :key="item">
                      <el-tooltip effect="dark" placement="top-start">
                        <div slot="content">{{item}}</div>
                        <span>{{item}}</span>
                      </el-tooltip>
                    </li>
                  </ul>
                </el-scrollbar>
              </div>
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
            <div class="about-influence-num color3">{{Images}}</div>
            <div class="about-influece-label">总数</div>
          </div>
        </div>
        <div class="about-box" v-loading="imageLoading">
          <el-scrollbar style="height:100%">
            <ul class="about-list" style="overflow: auto;">
              <li class="about-list-item" v-for="item of imageList" :key="item">
                <el-tooltip effect="dark" placement="top-start">
                  <div slot="content">{{item}}</div>
                  <span>{{item}}</span>
                </el-tooltip>
              </li>
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
      hostList: [],
      host: '',
      Containers: 0,
      ContainersRunning: 0,
      ContainersStopped: 0,
      DockerRootDir: '',
      Images: 0,
      MemTotal: 0,
      NCPU: 0,
      Name: '',
      OperatingSystem: '',
      ServerVersion: '',
      imageList: [],
      imageLoading: true,
      containerLoading: true,
      all_list: [],
      exited_list: [],
      running_list: [],
    }
  },
  mounted() {
    if (document.body.clientWidth > 1200 && document.body.clientWidth < 1330) {
      this.showTeam = true
    }
    this.getHostList()
  },
  watch: {
    host() {
      this.getAboutInfo()
      this.getImageList()
      this.getContainerList()
    },
  },
  methods: {
    handleRefresh() {
      this.getAboutInfo()
      this.getImageList()
      this.getContainerList()
    },
    getHostList() {
      axios.get('/v1/client/hosts')
        .then((res) => {
          const HostListData = res.data
          this.hostList = HostListData
          this.host = this.hostList[0].label
          this.getAboutInfo()
          this.getImageList()
          this.getContainerList()
        })
        .catch(this.getHostListFail)
    },
    getAboutInfo() {
      axios.get('/v1/client/info', {
        params: {
          host: this.host,
        },
      })
        .then(this.getInfoSucc)
        .catch(this.getInfoFail)
    },
    getImageList() {
      this.imageLoading = true
      axios.get('/v1/client/imageList', {
        params: {
          host: this.host,
        },
      })
        .then(this.getImageListSucc)
        .catch(this.getInfoFail)
    },
    getContainerList() {
      this.containerLoading = true
      axios.get('/v1/client/containerList', {
        params: {
          host: this.host,
        },
      })
        .then(this.getContainerListSucc)
        .catch(this.getInfoFail)
    },
    getInfoSucc(res) {
      const infoData = res.data
      this.Containers = infoData.Containers
      this.ContainersRunning = infoData.ContainersRunning
      this.ContainersStopped = infoData.ContainersStopped
      this.DockerRootDir = infoData.DockerRootDir
      this.Images = infoData.Images
      this.MemTotal = infoData.MemTotal
      this.NCPU = infoData.NCPU
      this.Name = infoData.Name
      this.OperatingSystem = infoData.OperatingSystem
      this.ServerVersion = infoData.ServerVersion
    },
    getInfoFail(error) {
      this.$message.error(error.response.data.msg)
    },
    getHostListSucc(res) {
      const HostListData = res.data
      this.hostList = HostListData
      this.host = this.hostList[0].label
    },
    getHostListFail(error) {
      console.log(error)
    },
    getImageListSucc(res) {
      const imageData = res.data
      this.imageList = imageData
      this.imageLoading = false
    },
    getContainerListSucc(res) {
      const ContainerData = res.data
      this.all_list = ContainerData.all_list
      this.exited_list = ContainerData.exited_list
      this.running_list = ContainerData.running_list
      this.containerLoading = false
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
    .select-btn {
      margin-left: 20px;
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
              color: #3963BC;
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
              color: #3963BC;
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
