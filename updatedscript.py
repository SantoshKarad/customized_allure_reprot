import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape


def preprocess_text(text):
    return escape(text.replace('"', "'"))


# parse the input XML file
tree = ET.parse('C:\\Users\\A0083034\\Downloads\\junitResult_2283\\newreport\\updated_junitResult.xml')
root = tree.getroot()

# create a list to store the test cases
testcases = []

# iterate through the cases in the XML file
for suite in root.findall("./suites/suite"):
    for case in suite.findall("./cases/case"):
        # extract the required information from each case
        classname = escape(preprocess_text(case.find("className").text))
        testname = escape(preprocess_text(case.find("testName").text))
        time = case.find("time").text
        status = "passed" if case.find("failedSince").text == "0" else "failed"

        # add the extracted information to the test cases list
        testcases.append({
            "name": testname,
            "time": time,
            "status": status,
            "classname": classname
        })

# generate the Allure report
with open('C:\\Users\\A0083034\\Downloads\\junitResult_2283\\newreport\\updatedreport\\allure_report.xml', "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<testsuite name="JUnit Report">\n')
    for testcase in testcases:
        f.write('<testcase classname="{}" name="{}" time="{}" status="{}">'.format(
            testcase["classname"], testcase["name"], testcase["time"], testcase["status"]))
        if testcase["status"] == "failed":
            error_details_element = case.find("errorDetails")
            error_details = preprocess_text(error_details_element.text) if error_details_element is not None else ""
            f.write('<failure message="{}"></failure>'.format(error_details))
        f.write('</testcase>\n')

    f.write('</testsuite>\n')
