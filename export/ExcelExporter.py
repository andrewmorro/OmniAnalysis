import xlwt


class ExcelExporter:

    @classmethod
    def output(filename, df, rule):
        df.to_excel(filename, sheet_name=rule, index=False)
