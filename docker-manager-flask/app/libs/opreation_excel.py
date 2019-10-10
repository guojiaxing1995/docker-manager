""" 
@Time    : 2018/8/29 19:08
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : opreation_excel.py
@Desc    :操作excel
"""
import xlrd
from xlutils.copy import copy

class OperationExcel:
    def __init__(self,file_name):
        self.workbook = self.get_workbook(file_name)

    def get_workbook(self,file_name):
        workbook = xlrd.open_workbook(file_name)
        return workbook

    def get_table(self,workbook,sheet_name=None,sheet_id=0):
        table = workbook.sheets()[sheet_id]
        if sheet_name:
            table = workbook.sheet_by_name(sheet_name)
        return table

    def get_rows(self,table):
        rows = table.nrows
        return rows

    def get_cols(self,table):
        cols = table.ncols
        return cols

    def get_cell_value(self,table,x,y):
        cell_value = table.cell_value(x, y)
        return cell_value

    def write_execel(self,workbook,sheetid,row,col,value):
        workbook_copy = copy(workbook)
        sheet_write = workbook_copy.get_sheet(sheetid)
        sheet_write.write(row,col,value)
        workbook_copy.save(self.file_name)