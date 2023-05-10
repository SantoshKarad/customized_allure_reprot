# import xml.etree.ElementTree as ET
# from xml.sax.saxutils import escape
# from collections import defaultdict
#
#
# def preprocess_text(text):
#     return escape(text.replace('"', "'"))
#
#
# # parse the input XML file
# tree = ET.parse('C:\\Users\\A0083034\\Downloads\\junitResult_2283\\newreport\\updated_junitResult.xml')
# root = tree.getroot()
#
# # create a dictionary to store the test cases per test suite
# testsuites = {}
#
# # create a dictionary to store the test suite-wise counters
# suite_counters = defaultdict(lambda: defaultdict(int))
#
# # iterate through the cases in the XML file
# for suite in root.findall("./suites/suite"):
#     suite_name = escape(suite.find("name").text)
#     testsuites[suite_name] = []
#
#     # create a dictionary to store the occurrences of test cases for this test suite
#     testcase_occurrences = defaultdict(int)
#
#     for case in suite.findall("./cases/case"):
#         # extract the required information from each case
#         classname = escape(preprocess_text(case.find("className").text))
#         testname = escape(preprocess_text(case.find("testName").text))
#         time = case.find("time").text
#         skipped = case.find("skipped")
#         if skipped is not None and skipped.text.lower() == "true":
#             status = "skipped"
#             suite_counters[suite_name]["skipped_testcases"] += 1
#             skipped_message_element = case.find("skippedMessage")
#             skipped_message = preprocess_text(skipped_message_element.text) if skipped_message_element is not None and skipped_message_element.text is not None else ""
#         else:
#             status = "passed" if case.find("failedSince").text == "0" else "failed"
#             suite_counters[suite_name]["passed_testcases"] += 1 if status == "passed" else 0
#             suite_counters[suite_name]["failed_testcases"] += 1 if status == "failed" else 0
#             skipped_message = ""
#
#         error_details = preprocess_text(case.find("errorDetails").text) if status == "failed" else ""
#
#         # add the extracted information to the test cases list
#         testsuites[suite_name].append({
#             "name": testname,
#             "time": time,
#             "status": status,
#             "classname": classname,
#             "error_details": error_details,
#             "skipped_message": skipped_message
#         })
#
#         # count the test cases per test suite
#         suite_counters[suite_name]["total_testcases"] += 1
#
#         # count the occurrences of the test case
#         testcase_key = (suite_name, classname, testname)
#         testcase_occurrences[testcase_key] += 1
#
#     # count and store the number of duplicate test cases per test suite after iterating through all test cases
#     suite_counters[suite_name]["duplicate_testcases"] = sum(occurrences - 1 for occurrences in testcase_occurrences.values())
#
# # calculate the total counters
# total_testsuites = len(testsuites)
# total_testcases = sum(counters["total_testcases"] for counters in suite_counters.values())
# total_passed_testcases = sum(counters["passed_testcases"] for counters in suite_counters.values())
# total_failed_testcases = sum(counters["failed_testcases"] for counters in suite_counters.values())
# total_skipped_testcases = sum(counters["skipped_testcases"] for counters in suite_counters.values())
# total_duplicate_testcases = sum(counters["duplicate_testcases"] for counters in suite_counters.values())
#
# # print the total counters
# print("Total counters")
# print("{:<20}{:<20}{:<20}{:<20}{:<20}{:<20}".format("Test suites", "Test cases", "Passed", "Failed", "Skipped", "Duplicate"))
# print("{:<20}{:<20}{:<20}{:<20}{:<20}{:<20}".format(total_testsuites, total_testcases, total_passed_testcases, total_failed_testcases, total_skipped_testcases, total_duplicate_testcases))
# print()
#
# # print the test suite-wise counters
# print("Test suite-wise counters")
# print("{:<30}{:<20}{:<20}{:<20}{:<20}{:<20}".format("Test suite", "Test cases", "Passed", "Failed", "Skipped", "Duplicate"))
# for suite_name, counters in suite_counters.items():
#     print("{:<30}{:<20}{:<20}{:<20}{:<20}{:<20}".format(suite_name, counters['total_testcases'], counters['passed_testcases'], counters['failed_testcases'], counters['skipped_testcases'], counters['duplicate_testcases']))
# print()
#
#
# # generate the Allure report per test suite
# for suite_name, testcases in testsuites.items():
#     with open(f'C:\\Users\\A0083034\\Downloads\\junitResult_2283\\newreport\\updatedreport\\allure_report_{suite_name}.xml', "w") as f:
#         f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
#         f.write(f'<testsuite name="{suite_name}">\n')
#         for testcase in testcases:
#             f.write('<testcase classname="{}" name="{}" time="{}" status="{}">'.format(
#             testcase["classname"], testcase["name"], testcase["time"], testcase["status"]))
#             if testcase["status"] == "failed":
#                 f.write('<failure message="{}"></failure>'.format(testcase["error_details"]))
#             elif testcase["status"] == "skipped":  # Write the skipped message for skipped test cases
#                 f.write('<skipped message="{}"></skipped>'.format(testcase["skipped_message"]))
#
#             f.write('</testcase>\n')
#
#         f.write('</testsuite>\n')


import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
from collections import defaultdict
import pandas as pd


def preprocess_text(text):
    return escape(text.replace('"', "'"))


# parse the input XML file
tree = ET.parse('C:\\Users\\A0083034\\Downloads\\junitResult_2283\\newreport\\updated_junitResult.xml')
root = tree.getroot()

# create a dictionary to store the test cases per test suite
testsuites = {}

# create a dictionary to store the test suite-wise counters
suite_counters = defaultdict(lambda: defaultdict(int))

# create a dictionary to store the occurrences of test cases
testcase_occurrences = defaultdict(int)

# iterate through the cases in the XML file
for suite in root.findall("./suites/suite"):
    suite_name = escape(suite.find("name").text)
    testsuites[suite_name] = []

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
            skipped_message = preprocess_text(skipped_message_element.text) if skipped_message_element is not None and skipped_message_element.text is not None else ""
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

        # count the occurrences of the test case
        testcase_key = (suite_name, classname, testname)
        testcase_occurrences[testcase_key] += 1

    # count and store the number of duplicate test cases per test suite after iterating through all test cases
    suite_counters[suite_name]["duplicate_testcases"] = sum(occurrences - 1 for occurrences in testcase_occurrences.values())

# calculate the total counters
total_testsuites = len(testsuites)
total_testcases = sum(counters["total_testcases"] for counters in suite_counters.values())
total_passed_testcases = sum(counters["passed_testcases"] for counters in suite_counters.values())
total_failed_testcases = sum(counters["failed_testcases"] for counters in suite_counters.values())
total_skipped_testcases = sum(counters["skipped_testcases"] for counters in suite_counters.values())
total_duplicate_testcases = sum(counters["duplicate_testcases"] for counters in suite_counters.values())

# print the total counters
print("Total counters")
print("{:<20}{:<20}{:<20}{:<20}{:<20}{:<20}".format("Test suites", "Test cases", "Passed", "Failed", "Skipped", "Duplicate"))
print("{:<20}{:<20}{:<20}{:<20}{:<20}{:<20}".format(total_testsuites, total_testcases, total_passed_testcases, total_failed_testcases, total_skipped_testcases, total_duplicate_testcases))
print()

# print the test suite-wise counters
print("Test suite-wise counters")
print("{:<30}{:<20}{:<20}{:<20}{:<20}{:<20}".format("Test suite", "Test cases", "Passed", "Failed", "Skipped", "Duplicate"))
for suite_name, counters in suite_counters.items():
    print("{:<30}{:<20}{:<20}{:<20}{:<20}{:<20}".format(suite_name, counters['total_testcases'], counters['passed_testcases'], counters['failed_testcases'], counters['skipped_testcases'], counters['duplicate_testcases']))
print()

# print the duplicate test cases per test suite
print("Duplicate test cases per test suite")
print("{:<30}{:<20}{:<20}".format("Test suite", "Class name", "Test name"))
for key, occurrences in testcase_occurrences.items():
    if occurrences > 1:
        print("{:<30}{:<20}{:<20}".format(key[0], key[1], key[2]))


# Prepare the DataFrame for duplicate test cases
duplicate_test_cases = []

for key, occurrences in testcase_occurrences.items():
    if occurrences > 1:
        duplicate_test_cases.append({
            "Test suite": key[0],
            "Class name": key[1],
            "Test name": key[2]
        })

# Create a pandas DataFrame
df_duplicate_test_cases = pd.DataFrame(duplicate_test_cases)

# Write the DataFrame to an Excel file
df_duplicate_test_cases.to_excel("duplicate_test_cases.xlsx", index=False)

# generate the Allure report per test suite
for suite_name, testcases in testsuites.items():
    with open(f'C:\\Users\\A0083034\\Downloads\\junitResult_2283\\newreport\\updatedreport\\allure_report_{suite_name}.xml', "w") as f:
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
