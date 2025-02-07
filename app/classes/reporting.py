import uuid
from io import BytesIO

import requests
import xlsxwriter
from PIL import Image
from flask import session


class FeedReporting():
    def createReport(self):
        fileName = str(uuid.uuid4()) + ".xlsx"
        session["fileName"] = fileName
        workbook = xlsxwriter.Workbook("temp/" + fileName)
        worksheet = workbook.add_worksheet()

        headerFormat = workbook.add_format({
            "bold": True, "font_size": 14, "align": "center", "valign": "vcenter", "bg_color": "#D9EAD3"
        })

        columnFormat = workbook.add_format({
            "border": 1, "align": "center", "valign": "vcenter"
        })

        wrapFormat = workbook.add_format({
            "border": 1, "align": "center", "valign": "vcenter", "text_wrap": True
        })
        row = 0
        col = 0
        worksheet.merge_range("A1:D1", f"Отчёт по {session.get("feedUrl")}", headerFormat)
        row += 1
        worksheet.write(row, col, "ID", headerFormat)
        worksheet.write(row, col + 1, "Имя", headerFormat)
        worksheet.write(row, col + 2, "Картинки", headerFormat)
        worksheet.write(row, col + 3, "Ошибки", headerFormat)
        row += 1

        worksheet.set_column("A:A", 15)
        worksheet.set_column("B:B", 25)
        worksheet.set_column("C:C", 15)
        worksheet.set_column("D:D", 25)

        for item in session.get("errors"):
            worksheet.write(row, col, item['id'], columnFormat)
            worksheet.write(row, col + 1, item['name'], wrapFormat)
            if item['pictures']:
                response = requests.get(item['pictures'][0])
                if response.status_code == 200:
                    image = BytesIO(response.content)
                    with Image.open(image) as img:
                        width, height = img.size
                    worksheet.insert_image(row, col + 2, "image.png",
                                           {"image_data": image, "x_scale": 80 / width, "y_scale": 80 / height})
            errorText = "\n".join(item['errors'])
            worksheet.write(row, col + 3, errorText, wrapFormat)

            worksheet.set_row(row, 80)
            row += 1
        workbook.close()
