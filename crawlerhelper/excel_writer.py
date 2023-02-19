import xlsxwriter
import os
import logger

class ExcelWriter():
    def __init__(self, root_dir, work_book_name) -> None:
        work_book_path = os.path.join(root_dir, work_book_name)
        self.work_book_name = work_book_name
        self.work_book = xlsxwriter.Workbook(work_book_path)
        self.sheet = self.work_book.add_worksheet()
        self.logger = logger.get_logger()

    # init sheet
    def init_sheet(self, column_list):
        self.column_list = column_list
        c_inx = 0
        for co in column_list:
            self.sheet.write(0, c_inx, co)
            c_inx = c_inx + 1
        self.curline = 1
        self.logger.info("excel sheet initialized")

    def close(self):
        self.work_book.close()
    
    def write_line(self, column, info):
        if column not in self.column_list:
            self.logger.error(f"this column '{column}' does not exist")
        self.sheet.write(self.curline, self.column_list.index(column), info)
        self.curline = self.curline + 1
    
    def write_line_at(self, line, column, info):
        if column not in self.column_list:
            self.logger.error(f"this column '{column}' does not exist")
        self.sheet.write(line, self.column_list.index(column), info)
