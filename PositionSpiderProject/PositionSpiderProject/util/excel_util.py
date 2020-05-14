import os

import xlsxwriter
import xlrd

from PositionSpiderProject.conf.common import OUTPUT_EXCEL_DIR, EXCEL_SUFFIX, INPUT_EXCEL_DIR


def save_to_excel(data_list: list, excel_name="my_excel", title_name=None, title_name_end_range=None,
                  work_sheet_name=None):
    """
    保存数据到excel
    @param: data_list数据格式:[{},{},{}...]
    @param： excel_name 文件的名称
    @param: title_name 第一行展示的标题
    @param: title_name_end_range 根据实际业务和excel当中的值确定
    """
    if not os.path.exists(OUTPUT_EXCEL_DIR):
        os.makedirs(OUTPUT_EXCEL_DIR)

    with xlsxwriter.Workbook(OUTPUT_EXCEL_DIR + EXCEL_SUFFIX.format(excel_name)) as workbook:
        worksheet = workbook.add_worksheet(work_sheet_name)
        title_format = workbook.add_format({'bold': True, 'border': 6,
                                            'align': 'center',  # 水平居中
                                            'font_size': 18,
                                            'bold': True,
                                            'valign': 'vcenter',  # 垂直居中
                                            'fg_color': '#D7E4BC',  # 颜色填充
                                            })
        format_1 = workbook.add_format(
            {'border': 1, 'align': 'center', 'bg_color': 'e9a34f', 'font_size': 16, 'bold': True})
        format_2 = workbook.add_format({'border': 1, 'align': 'center', 'bg_color': '83DD83', 'font_size': 14})

        # 找出字段数最多的哪一行
        max_column_index = 0
        max_column_count = 0
        for i in range(len(data_list)):
            if len(list(data_list[i].keys())) > max_column_count:
                max_column_index = i

        cols = list(data_list[max_column_index].keys())

        show_title = title_name is not None and title_name_end_range is not None
        if show_title:
            worksheet.merge_range("A1:{}".format(title_name_end_range), title_name, title_format)

        for col_index, col in enumerate(cols):
            worksheet.write(1 if show_title else 0, col_index, col, format_1)

        for row_index, data_dict in enumerate(data_list, start=2 if show_title else 1):
            for col_index, col_key in enumerate(cols):
                if col_key not in data_dict:
                    data_dict[col_key] = None
                worksheet.write(row_index, col_index, data_dict[col_key], format_2)


def save_to_list_from_excel(input_excel_dir, col_name_keys=None, have_title_name=False, have_column_name=False):
    """
    支持批量导出excel中的数据，并且转换成list  [{},{},...]
    @param input_excel_dir 文件所在位置
    @param col_name_keys 导入程序需要的key列表
    @param have_title_name 源文件是否有title
    @param have_column_name 源文件是否有列表头
    """

    if not os.path.exists(input_excel_dir):
        return

    files = os.listdir(input_excel_dir)
    items = []
    for filename in files:
        filename = input_excel_dir + "/" + filename
        print(filename)

        if os.path.isfile(filename):
            # 链接：https://www.cnblogs.com/nancyzhu/p/8401552.html
            # 只能读不能写,打开一个excel
            book = xlrd.open_workbook(filename)
            # 根据顺序获取sheet
            sheet = book.sheet_by_index(0)

            filter_row_count = 0
            if have_title_name and have_column_name:
                filter_row_count = 2
            elif not have_title_name and not have_column_name:
                filter_row_count = 0
            else:
                filter_row_count = 1

            for row in range(sheet.nrows):
                if row < filter_row_count:
                    continue
                item_dict = {}

                if col_name_keys is not None:
                    for index, key in enumerate(col_name_keys):
                        item_dict[key] = sheet.cell(row, index).value

                    items.append(item_dict)
    print(items)
    return items


if __name__ == '__main__':
    # lst = [{"name": "fanfna", "age": 18}]
    # save_to_excel(lst)
    save_to_list_from_excel(INPUT_EXCEL_DIR, col_name_keys=["name", "age", "sex"])
