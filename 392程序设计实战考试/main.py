from fastapi import FastAPI, UploadFile, File, Response
from fastapi.responses import FileResponse
app = FastAPI()
import pandas as pd
import io
import matplotlib.pyplot as plt
@app.post("/analyze/salary_by_district")
async def analyze_salary_by_district(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

    salary_stats = df.groupby("district")["salary"]
    mean_salary = salary_stats.mean()
    max_salary = salary_stats.max()
    min_salary = salary_stats.min()
    df["地区平均工资"] = df["district"].map(mean_salary)
    df["地区最高工资"] = df["district"].map(max_salary)
    df["地区最低工资"] = df["district"].map(min_salary)

    excel_filename = "salary_by_district.xlsx"
    df.to_excel(excel_filename, index=False)

    return FileResponse(excel_filename, media_type="application/vnd.ms-excel", filename=excel_filename)


@app.post("/analyze/company_count")
async def analyze_company_count(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

    company_count = df.groupby("district")["companyId"].count().reset_index()
    company_count.columns = ["地区", "公司数量"]

    plt.figure(figsize=(12, 6))
    bars = plt.bar(company_count["地区"], company_count["公司数量"])
    plt.xlabel("地区")
    plt.ylabel("公司数量")
    plt.title("各地区公司数量")
    for bar, count in zip(bars, company_count["公司数量"]):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, str(count), ha="center", va="bottom")

    bar_filename = "company_count.png"
    plt.savefig(bar_filename)
    plt.close()
    return FileResponse(bar_filename, media_type="image/png", filename=bar_filename)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8111)