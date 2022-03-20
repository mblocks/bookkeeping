# -*- coding: utf-8 -*-
import xlwt
import xlrd
from io import BytesIO
from datetime import datetime
from fastapi import responses


def xls_to_list(file_contents, *, mapper={}):
    sheet_name = 'Sheet1'
    book = xlrd.open_workbook(file_contents=file_contents)
    for sht in book.sheets():
        sheet_name = sht.name
        break
    res = list()
    try:
        # avoid sheet_name not exists
        sheet = book.sheet_by_name(sheet_name=sheet_name)
    except xlrd.biffh.XLRDError:
        return False, res

    """
    get excel column name and column index
    """
    header = [sheet.cell_value(rowx=0, colx=i)
              for i in range(len(sheet.row(rowx=0)))]
    header_map = list()
    for k, v in mapper.items():
        try:
            # avoid col_name not exists
            header_map.append((header.index(v), k))
        except ValueError:
            pass
    # https://stackoverflow.com/questions/32430679/how-to-read-dates-using-xlrd
    # get excel column name, and detect the type of the column
    row_types = sheet.row_types(rowx=1).tolist()
    date_types = []
    for i in range(len(row_types)):
        if row_types[i] == 3:
            date_types.append(i)

    for i in range(sheet.nrows - 1):
        values = sheet.row_values(rowx=i+1)
        res.append({v: datetime(*xlrd.xldate_as_tuple(values[k], book.datemode))
                   if k in date_types else (None if values[k] == '' else values[k]) for (k, v) in header_map})

    return True, res


def list_to_xls(name, *, columns, data):
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('sheet1')
    for column_index, item_column in enumerate(columns):
        sheet.write(0, column_index, item_column)
    for item_index, item_row in enumerate(data):
        for column_index, item_column in enumerate(columns):
            cell_value = getattr(item_row, item_column)
            sheet.write(item_index + 1, column_index, cell_value.strftime('%Y-%m-%d %H:%M:%S') if type(cell_value) == datetime else cell_value)  # nopep8
    out = BytesIO()
    workbook.save(out)
    out.seek(0)
    return responses.StreamingResponse(out, headers={'Content-disposition': 'attachment;filename={}'.format(name)})  # nopep8
