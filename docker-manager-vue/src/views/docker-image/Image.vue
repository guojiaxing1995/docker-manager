<template>
  <div class="container">
    <el-dialog
      title="docker run"
      :visible.sync="runDialogVisible"
      width="33%"
      :show-close="false"
      @close="closeRunForm">
      <div class="el-dialog-div">
        <el-scrollbar style="height:100%">
          <!-- <div class="run-item">
            <div class="run-item-left"></div>
            <div class="run-item-right"></div>
          </div> -->
        <el-form label-position="right" label-width="80px" :model="runForm">
          <el-form-item label="名称">
            <el-input class="run-input" placeholder="容器名称" v-model="runForm.name"></el-input>
          </el-form-item>
          <el-form-item label="运行命令">
            <el-input class="run-input" placeholder="command" v-model="runForm.command"></el-input>
          </el-form-item>
          <el-form-item label="端口映射">
            <i class="el-icon-circle-plus-outline" v-if="!runForm.portList.length" @click="runPortContent"></i>
            <el-row class="input-row" v-for="(item,index) in runForm.portList" :key="index">
              <el-input
                v-model="item.text"
                placeholder="宿主机端口:容器端口"
                size="medium"
                ></el-input>
              <div class="input-row-icon">
                <i class="el-icon-remove-outline" @click="removePortContent(index)"></i>
                <i class="el-icon-circle-plus-outline" v-if="index === runForm.portList.length-1" @click="runPortContent"></i>
              </div>
            </el-row>
          </el-form-item>
          <el-form-item label="数据挂载">
            <i class="el-icon-circle-plus-outline" v-if="!runForm.volumeList.length" @click="runVolumeContent"></i>
            <el-row class="input-row" v-for="(item,index) in runForm.volumeList" :key="index">
              <el-input
                v-model="item.text"
                placeholder="宿主机路径:容器路径"
                size="medium"
                ></el-input>
              <div class="input-row-icon">
                <i class="el-icon-remove-outline" @click="removeVolumeContent(index)"></i>
                <i class="el-icon-circle-plus-outline" v-if="index === runForm.volumeList.length-1" @click="runVolumeContent"></i>
              </div>
            </el-row>
          </el-form-item>
          <el-form-item label="连接容器">
            <i class="el-icon-circle-plus-outline" v-if="!runForm.linkList.length" @click="runLinkContent"></i>
            <el-row class="input-row" v-for="(item,index) in runForm.linkList" :key="index">
              <el-input
                v-model="item.text"
                placeholder="容器名称:别名"
                size="medium"
                ></el-input>
              <div class="input-row-icon">
                <i class="el-icon-remove-outline" @click="removeLinkContent(index)"></i>
                <i class="el-icon-circle-plus-outline" v-if="index === runForm.linkList.length-1" @click="runLinkContent"></i>
              </div>
            </el-row>
          </el-form-item>
          <el-form-item label="重启机制">
            <el-switch v-model="runForm.restart" active-text="总是重启" inactive-text="不重启"></el-switch>
          </el-form-item>
        </el-form>
        </el-scrollbar>
      </div>
        <span slot="footer" class="dialog-footer">
          <el-button @click="runDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="runDockerImage" :loading="runDialogLoading">确 定</el-button>
        </span>
    </el-dialog>
    <div class="select">
      <div class="select-left">
        <label class="select-label">服务器</label>
        <el-select v-model="host" filterable placeholder="请选择服务器">
          <el-option
            v-for="item in hostList"
            :key="item.value"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-select>
        <!-- <div class="select-btn">
          <el-button type="primary" plain :loading="loading" @click="handleRefresh">刷 新</el-button>
        </div> -->
      </div>
      <div class="search">
        <lin-search  placeholder="镜像名称或镜像id" :searchKeyWord="searchWord" @query="onQueryChange"/>
      </div>
    </div>
    <div class="table">
      <el-table
        :data="imageList"
        stripe
        v-loading="loading"
        style="width: 100%">
        <el-table-column
          fixed
          prop="name"
          label="镜像名称"
          :show-overflow-tooltip="true"
          min-width="350">
        </el-table-column>
        <el-table-column
          label="TAG"
          :show-overflow-tooltip="true"
          width="200">
        <template slot-scope="scope">
            <el-tag type="info">{{scope.row.tag}}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="id"
          label="镜像ID"
          width="240">
        </el-table-column>
        <el-table-column
          label="创建时间"
          width="240">
          <template slot-scope="scope">
            <div>
              <i class="el-icon-time"></i>
            </div>
            <span style="margin-left: 10px">{{ scope.row.created }}</span>
          </template>
        </el-table-column>
        <el-table-column
          prop="size"
          label="size"
          width="200">
        </el-table-column>
        <el-table-column
          prop="DockerVersion"
          label="DockerVersion"
          width="240">
        </el-table-column>
        <el-table-column
          width="180"
          fixed="right"
          label="操作">
          <template slot-scope="scope">
            <el-tooltip effect="dark" placement="top-start">
              <div slot="content">docker run</div>
                <el-button
                  size="mini"
                  type="primary"
                  @click="handleRun(scope.$index, scope.row)">运行</el-button>
            </el-tooltip>
            <el-tooltip effect="dark" placement="top-start">
              <div slot="content">docker rmi</div>
                <el-button
                  size="mini"
                  type="danger"
                  @click="handleDelete(scope.$index, scope.row)">删除</el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
    </div>
      <div class="pagination">
        <el-pagination
          background
          :hide-on-single-page=true
          @current-change="handleCurrentChange"
          layout="prev, pager, next"
          :current-page="page"
          :page-size=10
          :total="total">
        </el-pagination>
      </div>
  </div>
</template>

<script>
import axios from 'axios'
import LinSearch from '@/components/base/search/lin-search'

export default {
  components: {
    LinSearch,
  },
  data() {
    return {
      loading: false,
      hostList: [],
      host: '',
      imageList: [],
      page: 1,
      pages: 1,
      total: 0,
      searchWord: '',
      runDialogVisible: false,
      runDialogLoading: false,
      runForm: {
        image: '',
        name: null,
        command: null,
        linkList: [],
        portList: [],
        volumeList: [],
        restart: true,
      },
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
      this.page = 1
      this.total = 0
      this.pages = 1
      this.searchWord = ''
      this.getImageList()
    },
  },
  methods: {
    // handleRefresh() {
    //   this.page = 1
    //   this.total = 0
    //   this.pages = 1
    //   this.getImageList()
    // },
    // docker run
    runDockerImage() {
      this.runDialogLoading = true
      const runDate = {}
      runDate.host = this.host
      runDate.image = this.runForm.image
      runDate.name = this.runForm.name
      runDate.command = this.runForm.command
      runDate.restart = this.runForm.restart
      // 端口列表处理
      if (this.runForm.portList) {
        let ports = ''
        this.runForm.portList.forEach((item) => {
          if (item.text !== '') {
            ports = ports + ',' + item.text
          }
        })
        ports = ports.substr(1)
        runDate.ports = ports
      } else {
        runDate.ports = ''
      }
      // 挂载列表处理
      if (this.runForm.volumeList) {
        let volumes = ''
        this.runForm.volumeList.forEach((item) => {
          if (item.text !== '') {
            volumes = volumes + ',' + item.text
          }
        })
        volumes = volumes.substr(1)
        runDate.volumes = volumes
      } else {
        runDate.volumes = ''
      }
      // link列表处理
      if (this.runForm.linkList) {
        let links = ''
        this.runForm.linkList.forEach((item) => {
          if (item.text !== '') {
            links = links + ',' + item.text
          }
        })
        links = links.substr(1)
        runDate.links = links
      } else {
        runDate.links = ''
      }
      axios.post('/v1/image/run', runDate)
        .then((res) => {
          console.log(res.data)
          this.runDialogLoading = false
          this.runDialogVisible = false
          this.$message({
            type: 'success',
            message: '运行成功',
          })
        })
        .catch((error) => {
          this.$message.error(error.response.data.msg)
          this.runDialogLoading = false
        })
    },
    // 关闭容器运行弹框时重置表单
    closeRunForm() {
      this.runForm = {
        image: '',
        name: null,
        command: null,
        linkList: [],
        portList: [],
        volumeList: [],
        restart: true,
      }
    },
    runPortContent() {
      this.runForm.portList.push({
        text: '',
        type: 'plus',
      })
    },
    removePortContent(index) {
      this.runForm.portList.splice(index, 1)
    },
    runVolumeContent() {
      this.runForm.volumeList.push({
        text: '',
        type: 'plus',
      })
    },
    removeVolumeContent(index) {
      this.runForm.volumeList.splice(index, 1)
    },
    runLinkContent() {
      this.runForm.linkList.push({
        text: '',
        type: 'plus',
      })
    },
    removeLinkContent(index) {
      this.runForm.linkList.splice(index, 1)
    },
    onQueryChange(query) {
      this.searchWord = query.trim()
      this.page = 1
      this.getImageList()
    },
    // 获取host列表
    getHostList() {
      axios.get('/v1/client/hosts')
        .then((res) => {
          const HostListData = res.data
          this.hostList = HostListData
          this.host = this.hostList[0].label
        })
        .catch(this.getHostListFail)
    },
    getHostListFail(error) {
      this.$message.error(error.response.data.msg)
    },
    // 获取镜像列表
    getImageList() {
      this.loading = true
      axios.get('/v1/image/list', {
        params: {
          host: this.host,
          page: this.page,
          search: this.searchWord,
        },
      })
        .then(this.getImageListSucc)
        .catch(this.getHostListFail)
    },
    getImageListSucc(res) {
      this.imageList = res.data.data
      this.page = res.data.page
      this.pages = res.data.pages
      this.total = res.data.total
      this.loading = false
    },
    handleCurrentChange(val) {
      this.page = val
      this.getImageList()
    },
    handleRun(index, val) {
      this.runDialogVisible = true
      this.runForm.image = val.name + ':' + val.tag
    },
    // 点击删除按钮
    handleDelete(index, val) {
      this
        .$confirm('此操作将永久删除该镜像, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        })
        .then(() => {
          const image = val.name + ':' + val.tag
          this.removeImage(image)
        })
    },
    removeImage(val) {
      this.loading = true
      axios.get('/v1/image/delete', {
        params: {
          host: this.host,
          image: val,
        },
      })
        .then((res) => {
          if (res.data.error_code === 1) {
            this.$message({
              type: 'success',
              message: res.data.msg,
            })
            this.page = 1
            this.getImageList()
          }
        })
        .catch((error) => {
          this.loading = false
          if (error.response.data.error_code === 1016) {
            this.$message.error(error.response.data.msg)
          } else if (error.response.data.error_code === 1018) {
            this.$message.error(error.response.data.msg)
          }
        })
    },
  },
}
</script>

<style scoped lang="scss">
.container {
  padding: 40px;
  height: 100%;
  .el-dialog-div{
    height: 50vh;
    overflow: auto;
    .run-input{
      width: 90%;
    }
    .el-icon-circle-plus-outline{
      font-size: 20px;
    }
    .input-row{
      display: flex;
      -webkit-box-pack: justify;
      justify-content: space-between;
      margin-bottom: 10px;
      .input-row-icon{
        width: 20%;
        display: flex;
        align-items:center;
        justify-content: flex-start;
        .el-icon-remove-outline{
          margin-left: 10px;
          font-size: 20px;
          color: #c6848e;
        }
        .el-icon-circle-plus-outline{
          margin-left: 10px;
          font-size: 20px;
        }
      }
    }
    .run-item {
      display: flex;
      height: 20px;
      .run-item-left {
        background: red;
        width: 38.2%;
      }
      .run-item-right {
        background: green;
        width: 61.8%;
      }
    }
  }
  .el-dialog-div /deep/ .el-form-item__content {
    margin-bottom: 10px;
  }
  .el-dialog-div /deep/ .el-scrollbar__wrap {
    overflow-x: hidden;
  }
  .select {
    display: flex;
    align-items: center;
    margin-top: 20px;
    justify-content: space-between;
    .select-left{
      display: flex;
      align-items: center;
      .select-label {
        width: 60px
      }
      .select-btn {
        margin-left: 20px;
      }
    }
    .search {
      float: right;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  }
  .table {
    margin-top: 40px;
  }
  // 滚动条优化
  .table /deep/ .el-table__body-wrapper::-webkit-scrollbar {
    width: 6px;
    height: 10px;
  }
  .table /deep/ .el-table__body-wrapper::-webkit-scrollbar-thumb {
    background-color: #ddd;
    border-radius: 5px;
  }
  .pagination {
    display: flex;
    justify-content: flex-end;
    margin-top: 30px;
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
