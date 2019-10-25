<template>
  <div class="container">
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
          <lin-search  placeholder="镜像名称或镜像id" :searchKeyWord="searchWord" @query="onQueryChange"/>
        </div>
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
          label="容器名称"
          :show-overflow-tooltip="true"
          min-width="150">
        </el-table-column>
        <el-table-column
          label="容器状态"
          :show-overflow-tooltip="true"
          width="200">
        <template slot-scope="scope">
            <el-tag type="info">{{scope.row.tag}}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="id"
          label="容器ID"
          width="240">
        </el-table-column>
        <el-table-column
          prop="size"
          label="镜像"
          :show-overflow-tooltip="true"
          width="350">
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
          width="400"
          align="center"
          fixed="right"
          label="操作">
          <template slot-scope="scope">
            <el-tooltip effect="dark" placement="top-start">
              <div slot="content">docker run</div>
                <el-button
                  size="mini"
                  type="primary"
                  style="margin:auto"
                  @click="handleRun(scope.$index, scope.row)">运行</el-button>
            </el-tooltip>
            <el-tooltip effect="dark" placement="top-start">
              <div slot="content">docker rmi</div>
                <el-button
                  size="mini"
                  type="danger"
                  style="margin:auto"
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
      searchResultData: [],
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
    handleRefresh() {
      this.page = 1
      this.total = 0
      this.pages = 1
      this.getImageList()
    },
    onQueryChange(query) {
      this.searchWord = query.trim()
      this.page = 1
      this.pages = 1
      this.total = 0
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
