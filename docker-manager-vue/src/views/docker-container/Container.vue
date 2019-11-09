<template>
  <div class="container">
    <div class="shell-header" v-show="shellDialogVisible">
      <div class="shell-header-name">
        {{shellContainer}}
      </div>
      <div class="close-icon">
        <el-tooltip effect="dark" placement="top-start">
          <div slot="content">关闭终端前请使用 exit 命令退出bash</div>
          <i class="el-icon-info"></i>
        </el-tooltip>
        <i class="el-icon-circle-close" @click="closeShell"></i>
      </div>
    </div>
    <div id="terminal"></div>
    <div v-show="!shellDialogVisible">
      <el-dialog
        class="log"
        title="docker logs"
        :visible.sync="logDialogVisible"
        width="70%"
        :close-on-click-modal="false"
        :show-close="false"
        @close="closeLogDialog">
        <span slot="title">
          <div class="log-header">
            <div class="log-header-left">
              {{logContainer}}
            </div>
            <div class="log-header-right">
              <i v-if="logPrint" class="el-icon-video-pause" @click="pauseLogs"></i>
              <i v-else class="el-icon-video-play" @click="startLogs"></i>
              <i class="el-icon-brush" @click="clearLogDialog"></i>
              <i class="el-icon-circle-close" @click="logDialogVisible = false"></i>
            </div>
          </div>
        </span>
        <div class="el-dialog-div">
          <el-scrollbar style="height:100%" ref="elscrollbar">
            <div v-html="logs">{{logs}}</div>
          </el-scrollbar>
        </div>
      </el-dialog>
      <el-dialog
        title="提示"
        :visible.sync="removeDialogVisible"
        width="25%"
        :show-close="false"
        class="remove-dialog"
        @close="closeRemoveForm">
        <div style="display:flex;align-items:center;"><l-icon name="info-circle" width="1.4rem" height="1.4rem" color="#FFBE4D"></l-icon>&nbsp;此操作将永久删除该容器，是否继续？</div>
        <div style="margin-top:15px;">同时删除挂载卷&nbsp;&nbsp;<el-switch v-model="removeForm.volume"></el-switch></div>
        <span slot="footer" class="dialog-footer">
          <el-button @click="removeDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="removeContainer">确 定</el-button>
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
          <div><i class="el-icon-refresh" @click="handleRefresh"></i></div>
        </div>
        <div class="select-right">
          <div class="search">
            <lin-search  placeholder="容器名称或容器id" :searchKeyWord="searchWord" @query="onQueryChange"/>
          </div>
        </div>
      </div>
      <div class="table">
        <el-table
          :data="containerList"
          stripe
          v-loading="loading"
          style="width: 100%">
          <el-table-column type="expand" fixed>
            <template slot-scope="props">
              <el-form label-position="left" inline class="demo-table-expand">
                <el-form-item label="启动命令">
                  <span>{{ props.row.cmd }}</span>
                </el-form-item>
                <el-form-item label="网络">
                  <span>{{ props.row.network }}</span>
                </el-form-item>
                <el-form-item label="重启次数">
                  <span>{{ props.row.restartCount }}</span>
                </el-form-item>
                <el-form-item label="端口映射">
                  <span>{{ props.row.ports }}</span>
                </el-form-item>
                <el-form-item label="数据挂载">
                  <span>{{ props.row.volumes }}</span>
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>
          <el-table-column
            fixed
            prop="name"
            label="容器名称"
            :show-overflow-tooltip="true"
            min-width="150">
          </el-table-column>
          <el-table-column
            label="容器状态"
            :show-overflow-tooltip="true"
            width="200">
          <template slot-scope="scope">
              <el-tag v-if="scope.row.status === 'running'" type="success">{{scope.row.status}}</el-tag>
              <el-tag v-else-if="scope.row.status === 'exited'" type="danger">{{scope.row.status}}</el-tag>
              <el-tag v-else type="warning">{{scope.row.status}}</el-tag>
            </template>
          </el-table-column>
          <el-table-column
            prop="id"
            label="容器ID"
            width="200">
          </el-table-column>
          <el-table-column
            prop="image"
            label="镜像"
            :show-overflow-tooltip="true"
            width="300">
          </el-table-column>
          <el-table-column
            label="创建时间"
            width="220">
            <template slot-scope="scope">
              <div>
                <i class="el-icon-time"></i>
              </div>
              <span style="margin-left: 10px">{{ scope.row.created }}</span>
            </template>
          </el-table-column>
          <el-table-column
            width="380"
            align="center"
            fixed="right"
            label="操作">
            <template slot-scope="scope">
              <el-tooltip effect="dark" placement="top-start">
                <div slot="content">docker start</div>
                  <el-button
                    :disabled="scope.row.status !== 'exited'"
                    size="mini"
                    type="success"
                    style="margin:auto"
                    @click="handleStart(scope.$index, scope.row)">启动</el-button>
              </el-tooltip>
              <el-tooltip effect="dark" placement="top-start">
                <div slot="content">docker stop</div>
                  <el-button
                    :disabled="scope.row.status !== 'running'"
                    size="mini"
                    type="warning"
                    style="margin:auto"
                    @click="handleStop(scope.$index, scope.row)">停止</el-button>
              </el-tooltip>
              <el-tooltip effect="dark" placement="top-start">
                <div slot="content">docker rm</div>
                  <el-button
                    :disabled="scope.row.status === 'running'"
                    size="mini"
                    type="danger"
                    style="margin:auto"
                    @click="handleDelete(scope.$index, scope.row)">删除</el-button>
              </el-tooltip>
              <el-tooltip effect="dark" placement="top-start">
                <div slot="content">docker logs</div>
                  <el-button
                    :disabled="scope.row.status !== 'running'"
                    size="mini"
                    type="primary"
                    style="margin:auto"
                    @click="handleLogs(scope.$index, scope.row)">日志</el-button>
              </el-tooltip>
              <el-tooltip effect="dark" placement="top-start">
                <div slot="content">docker exec -it /bin/sh</div>
                  <el-button
                    :disabled="scope.row.status !== 'running'"
                    size="mini"
                    type="info"
                    style="margin:auto"
                    @click="handleShell(scope.$index, scope.row)">shell</el-button>
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
  </div>
</template>

<script>
import axios from 'axios'
import LinSearch from '@/components/base/search/lin-search'
import 'xterm/css/xterm.css'
import { Terminal } from 'xterm'
import { FitAddon } from 'xterm-addon-fit'
import { AttachAddon } from 'xterm-addon-attach'

export default {
  name: 'container',
  components: {
    LinSearch,
  },
  data() {
    return {
      loading: false,
      hostList: [],
      host: '',
      containerList: [],
      page: 1,
      pages: 1,
      total: 0,
      searchWord: '',
      searchResultData: [],
      hasLogs: [],
      removeForm: {
        container: '',
        volume: false,
      },
      removeDialogVisible: false,
      logDialogVisible: false,
      logPrint: true,
      logs: '',
      logContainer: '',
      shellDialogVisible: false,
      shellContainer: '',
      terminal: '',
      ws: '',
    }
  },
  activated() {
    if (this.$route.query.id) {
      this.searchWord = this.$route.query.id
    }
  },
  mounted() {
    // 没用。。。
    // this.$socket.emit('disconnect')
    if (document.body.clientWidth > 1200 && document.body.clientWidth < 1330) {
      this.showTeam = true
    }
    this.getHostList()
    if (this.$route.query.id) {
      this.searchWord = this.$route.query.id
    }
  },
  watch: {
    host() {
      this.page = 1
      this.total = 0
      this.pages = 1
      this.searchWord = ''
      this.getContainerList()
    },
  },
  methods: {
    handleRefresh() {
      this.page = 1
      this.total = 0
      this.pages = 1
      this.getContainerList()
    },
    onQueryChange(query) {
      this.searchWord = query.trim()
      this.page = 1
      this.pages = 1
      this.total = 0
      this.getContainerList()
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
    // 获取r容器列表
    getContainerList() {
      this.loading = true
      axios.get('/v1/container/list', {
        params: {
          host: this.host,
          page: this.page,
          search: this.searchWord,
        },
      })
        .then(this.getContainerListSucc)
        .catch(this.getHostListFail)
    },
    getContainerListSucc(res) {
      this.containerList = res.data.data
      this.page = res.data.page
      this.pages = res.data.pages
      this.total = res.data.total
      this.loading = false
    },
    handleCurrentChange(val) {
      this.page = val
      this.getContainerList()
    },
    // 启动容器
    handleStart(index, val) {
      this.loading = true
      axios.get('/v1/container/start', {
        params: {
          host: this.host,
          nameOrId: val.id,
        },
      })
        .then((res) => {
          if (res.data.error_code === 0) {
            this.$message({
              type: 'success',
              message: res.data.msg,
            })
            this.page = 1
            this.pages = 1
            this.total = 0
            this.getContainerList()
          }
        })
        .catch((error) => {
          this.loading = false
          if (error.response.data.error_code === 1023) {
            this.$message.error(error.response.data.msg)
          }
        })
    },
    handleStop(index, val) {
      this.loading = true
      axios.get('/v1/container/stop', {
        params: {
          host: this.host,
          nameOrId: val.id,
        },
      })
        .then((res) => {
          if (res.data.error_code === 0) {
            this.$message({
              type: 'success',
              message: res.data.msg,
            })
            this.page = 1
            this.pages = 1
            this.total = 0
            this.getContainerList()
          }
        })
        .catch((error) => {
          this.loading = false
          if (error.response.data.error_code === 1022) {
            this.$message.error(error.response.data.msg)
          }
        })
    },
    // 点击删除按钮
    handleDelete(index, val) {
      this.removeDialogVisible = true
      this.removeForm.container = val.id
    },
    closeRemoveForm() {
      this.removeForm.container = ''
      this.removeForm.volume = false
    },
    removeContainer() {
      this.loading = true
      this.removeDialogVisible = false
      axios.get('/v1/container/remove', {
        params: {
          host: this.host,
          nameOrId: this.removeForm.container,
          volume: this.removeForm.volume,
        },
      })
        .then((res) => {
          if (res.data.error_code === 0) {
            this.$message({
              type: 'success',
              message: res.data.msg,
            })
            this.page = 1
            this.pages = 1
            this.total = 0
            this.getContainerList()
          }
        })
        .catch((error) => {
          this.loading = false
          if (error.response.data.error_code === 1024) {
            this.$message.error(error.response.data.msg)
          }
        })
    },
    clearLogDialog() {
      this.logs = ''
    },
    closeLogDialog() {
      this.logs = ''
      this.pauseLogs()
    },
    handleLogs(index, val) {
      this.logDialogVisible = true
      this.logPrint = true
      this.logContainer = val.name
      // 如果之前发送过消息则直接订阅
      this.startLogs()
    },
    startLogs() {
      this.logPrint = true
      if (!(this.hasLogs.indexOf(this.host + this.logContainer) > -1)) {
        console.log('请求')
        this.hasLogs.push(this.host + this.logContainer)
        this.$socket.emit('logs', {
          host: this.host,
          name: this.logContainer,
        })
      }
      this.sockets.subscribe(this.host + this.logContainer, (data) => {
        console.log(data.name)
        if (data.name === this.logContainer) {
          this.logs = this.logs + data.msg + '<br>'
          const div = this.$refs.elscrollbar.$refs.wrap
          this.$nextTick(() => {
            div.scrollTop = div.scrollHeight
          })
        }
      })
      // if (this.hasLogs.indexOf(this.host + this.logContainer) > -1) {
      //   this.sockets.subscribe(this.host + this.logContainer, (data) => {
      //     if (data.name === this.logContainer) {
      //       console.log(5)
      //       this.logs = this.logs + data.msg + '<br>'
      //       const div = this.$refs.elscrollbar.$refs.wrap
      //       this.$nextTick(() => {
      //         div.scrollTop = div.scrollHeight
      //       })
      //     }
      //   })
      // } else {
      //   this.hasLogs.push(this.host + this.logContainer)
      //   this.$socket.emit('logs', {
      //     host: this.host,
      //     name: this.logContainer,
      //   })
      //   this.sockets.subscribe(this.host + this.logContainer, (data) => {
      //     if (data.name === this.logContainer) {
      //       console.log(6)
      //       this.logs = this.logs + data.msg + '<br>'
      //       const div = this.$refs.elscrollbar.$refs.wrap
      //       this.$nextTick(() => {
      //         div.scrollTop = div.scrollHeight
      //       })
      //     }
      //   })
      // }
    },
    pauseLogs() {
      this.logPrint = false
      this.sockets.unsubscribe(this.host + this.logContainer)
    },
    handleShell(index, val) {
      this.shellContainer = val.name
      const _self = this
      this.shellDialogVisible = true
      const term = new Terminal({
        // cols: 100,
        rows: 28,
        lineHeight: 1.2,
        rightClickSelectsWord: true,
        convertEol: true,
        cursorStyle: 'underline',
        cursorBlink: true,
        theme: {
          cursor: '#3963bc',
          // selection: '#3963bc',
          black: '\x1b[30m',
          red: '\x1b[30m',
          green: '\x1b[32m',
          yellow: '\x1b[33m',
          blue: 'blue',
          magenta: '\x1b[35m',
          cyan: '\x1b[36m',
          white: '\x1b[37m',
          brightBlack: '\x1b[1;30m',
          brightRed: '\x1b[1;31m',
          brightGreen: '\x1b[1;32m',
          brightYellow: '\x1b[1;33m',
          brightBlue: '\x1b[1;34m',
          brightMagenta: '\x1b[1;35m',
          brightCyan: '\x1b[1;36m',
          brightWhite: '\x1b[1;37m',
        },
      })
      this.terminal = term
      term.open(document.getElementById('terminal'))
      term.writeln('Hello \x1b[1;34mTester\x1B[0m $ ')
      // const ws = new WebSocket(`ws://${location.host}/echo`)
      const ws = new WebSocket('ws://localhost:5006/echo')
      this.ws = ws
      ws.onopen = function () {
        ws.send(_self.host + ',' + val.name)
        // setInterval(function () { ws.send('__ping__') }, 8000)
      }
      const fitAddon = new FitAddon()
      term.loadAddon(fitAddon)
      const attachAddon = new AttachAddon(ws)
      term.loadAddon(attachAddon)
      console.log(term.cols, term.rows)
      ws.onclose = function () {
        term.writeln('closed. Thank you for use!')
      }
    },
    closeShell() {
      this.ws.close()
      this.ws = ''
      this.terminal.dispose()
      this.terminal = ''
      this.shellDialogVisible = false
    },
  },
}
</script>

<style scoped lang="scss">
.container {
  padding: 40px;
  height: 100%;
  .shell-header {
    display: flex;
    align-items: center;
    background: #3963bc;
    width: 100%;
    height: 40px;
    .shell-header-name{
      margin-left: 15px;
      color: #ddd;
      width: 50%;
    }
    .close-icon{
      display: flex;
      justify-content: flex-end;
      width: 50%;
      i {
        margin-top: auto;
        margin-bottom: auto;
        color: #ddd;
        font-size: 1.6rem;
        margin-right: 15px;
        cursor: pointer;
        }
    }
  }
  .log {
    .log-header {
      display: flex;
      align-items: center;
      .log-header-left {
        color: #ddd;
        width: 50%;
      }
      .log-header-right {
        display: flex;
        justify-content: flex-end;
        width: 50%;
        i {
          color: #ddd;
          font-size: 1.6rem;
          margin-left: 15px;
          cursor: pointer;
        }
      }
    }
  }
  .log /deep/ .el-dialog__header {
    padding: 10px 15px;
    background: #3963bc;
  }
  .el-dialog-div{
    height: 60vh;
    overflow: auto;
  }
  .remove-dialog /deep/ .el-dialog__body {
    padding: 20px 20px;
    font-size: 16px;
  }
  .el-dialog-div /deep/ .el-table {
    border: 0px;
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
      .el-icon-refresh{
        font-size: 20px;
        margin-left: 20px;
        cursor: pointer;
      }
      .select-label {
        width: 60px
      }
      .select-btn {
        margin-left: 20px;
      }
    }
    .select-right {
      float: right;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  }
  .table {
    margin-top: 40px;
  }
  .table /deep/ .demo-table-expand {
    font-size: 0;
  }
   .table /deep/ .demo-table-expand label {
    width: 80px;
    color: #3963bc;
  }
   .table /deep/ .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
  }
  .table /deep/ .el-form-item__content {
    margin-bottom: 0;
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
