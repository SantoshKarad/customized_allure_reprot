with open('C:\\Users\\A0083034\\Downloads\\junitResult_2283\\allure_report.xml', 'r') as f:
    data = f.read()
    new_data = data.replace("duration", "time")

with open('C:\\Users\\A0083034\\Downloads\\junitResult_2283\\report\\updated_allure_report.xml', 'w') as f:
    f.write(new_data)
