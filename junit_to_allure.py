import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
from collections import defaultdict


def preprocess_text(text):
    return escape(text.replace('"', "'"))


# parse the input XML file
tree = ET.parse('C:\\Users\\A0083034\\Downloads\\junitResult_2283\\newreport\\updated_junitResult.xml')
root = tree.getroot()

# create a dictionary to store the test cases per test suite
testsuites = {}

# create a dictionary to store the test suite-wise counters
suite_counters = defaultdict(lambda: defaultdict(int))

# iterate through the cases in the XML file
for suite in root.findall("./suites/suite"):
    suite_name = escape(suite.find("name").text)
    testsuites[suite_name] = []

    # create a dictionary to store the occurrences of test cases for this test suite
    testcase_occurrences = defaultdict(int)

    for case in suite.findall("./cases/case"):
        # extract the required information from each case
        classname = escape(preprocess_text(case.find("className").text))
        testname = escape(preprocess_text(case.find("testName").text))
        time = case.find("time").text
        skipped = case.find("skipped")
        if skipped is not None and skipped.text.lower() == "true":
            status = "skipped"
            suite_counters[suite_name]["skipped_testcases"] += 1
            skipped_message_element = case.find("skippedMessage")
            skipped_message = preprocess_text(
                skipped_message_element.text) if skipped_message_element is not None and skipped_message_element.text is not None else ""
        else:
            status = "passed" if case.find("failedSince").text == "0" else "failed"
            suite_counters[suite_name]["passed_testcases"] += 1 if status == "passed" else 0
            suite_counters[suite_name]["failed_testcases"] += 1 if status == "failed" else 0
            skipped_message = ""

        error_details = preprocess_text(case.find("errorDetails").text) if status == "failed" else ""

        # add the extracted information to the test cases list
        testsuites[suite_name].append({
            "name": testname,
            "time": time,
            "status": status,
            "classname": classname,
            "error_details": error_details,
            "skipped_message": skipped_message
        })


# generate the Allure report per test suite
for suite_name, testcases in testsuites.items():
    with open(
            f'C:\\Users\\A0083034\\Downloads\\junitResult_2283\\newreport\\updatedreport\\allure_report_{suite_name}.xml',
            "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(f'<testsuite name="{suite_name}">\n')
        for testcase in testcases:
            f.write('<testcase classname="{}" name="{}" time="{}" status="{}">'.format(
                testcase["classname"], testcase["name"], testcase["time"], testcase["status"]))
            if testcase["status"] == "failed":
                f.write('<failure message="{}"></failure>'.format(testcase["error_details"]))
            elif testcase["status"] == "skipped":  # Write the skipped message for skipped test cases
                f.write('<skipped message="{}"></skipped>'.format(testcase["skipped_message"]))

            f.write('</testcase>\n')

        f.write('</testsuite>\n')
