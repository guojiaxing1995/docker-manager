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
                  @click="handleEdit(scope.$index, scope.row)">运行</el-button>
            </el-tooltip>
            <el-tooltip effect="dark" placement="top-start">
              <div slot="content">docker rmi</div>
                <el-button
                  size="mini"
                  type="danger"
                  @click="handleEdit(scope.$index, scope.row)">删除</el-button>
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
    onQueryChange(query) {
      this.searchWord = query.trim()
      this.page = 1
      this.getImageList()
    },
    getHostList() {
      axios.get('/v1/client/hosts')
        .then((res) => {
          const HostListData = res.data
          this.hostList = HostListData
          this.host = this.hostList[0].label
          this.getImageList()
        })
        .catch(this.getHostListFail)
    },
    getHostListFail(error) {
      this.$message.error(error.response.data.msg)
    },
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
