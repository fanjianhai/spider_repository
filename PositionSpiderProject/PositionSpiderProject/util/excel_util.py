import xlsxwriter

from PositionSpiderProject.conf.common import OUTPUT_EXCEL_PATH


def save_to_excel(data_list: list, excel_name="my_excel", title_name=None, title_name_end_range=None,
                  work_sheet_name=None):
    """
    保存数据到excel
    @param: data_list:[{},{},{}...]
    @param: title_name_end_range 根据实际业务和excel当中的值确定
    """
    with xlsxwriter.Workbook(OUTPUT_EXCEL_PATH.format(excel_name)) as workbook:
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
        if title_name is not None and title_name_end_range is not None:
            worksheet.merge_range("A1:{}".format(title_name_end_range), title_name, title_format)

        for col_index, col in enumerate(cols):
            worksheet.write(1, col_index, col, format_1)

        for row_index, data_dict in enumerate(data_list, start=2):
            for col_index, col_key in enumerate(cols):
                if col_key not in data_dict:
                    data_dict[col_key] = None
                worksheet.write(row_index, col_index, data_dict[col_key], format_2)


if __name__ == '__main__':
    lst = [{"name": "fanfna", "age": 18}]
    save_to_excel(lst)
