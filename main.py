import shutil
from tempfile import NamedTemporaryFile

import pandas as pd
import pdfplumber
from fastapi import FastAPI, File, UploadFile, applications
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse


def swagger_monkey_patch(*args, **kwargs):
    """
    Wrap the function which is generating the HTML for the /docs endpoint and
    overwrite the default values for the swagger js and css.
    Fuck GFW
    """
    return get_swagger_ui_html(
        *args,
        **kwargs,
        swagger_js_url="https://jsd.cdn.zzko.cn/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://jsd.cdn.zzko.cn/npm/swagger-ui-dist@5/swagger-ui.css"
    )


# Actual monkey patch
applications.get_swagger_ui_html = swagger_monkey_patch


app = FastAPI()


@app.post("/process_pdf/")
async def process_pdf(pdf_file: UploadFile = File(...)):
    try:
        # 创建临时文件
        with NamedTemporaryFile(delete=False) as temp_pdf:
            shutil.copyfileobj(pdf_file.file, temp_pdf)

        # 使用 pdfplumber 打开临时文件
        with pdfplumber.open(temp_pdf.name) as pdf:
            result = []
            for page in pdf.pages:
                table = page.extract_table()
                table_df = pd.DataFrame(table[1:], columns=table[0])
                records = table_df.to_dict(orient="records")
                result.extend(records)

        return JSONResponse(content={"table_data": result})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
