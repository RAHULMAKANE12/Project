
import random
import string
import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ============================================================
# HACKFORGE | HACKATHON REGISTRATION AUTOMATION
# ============================================================

URL = "http://127.0.0.1:5000"

ACTION_WAIT = 2
PAGE_WAIT = 3
RESULT_DISPLAY_TIME = 15


# ============================================================
# TEST EXECUTION SUMMARY
# ============================================================

TEST_RESULTS = []


def report_test(test_name, status, details=""):
    TEST_RESULTS.append((test_name, status, details))

    print("\n" + "-" * 65)
    print(f"TEST CASE : {test_name}")
    print(f"STATUS    : {status}")

    if details:
        print(f"DETAILS   : {details}")

    print("-" * 65)


def pause(seconds=ACTION_WAIT):
    time.sleep(seconds)


# ============================================================
# RANDOM TEST DATA
# ============================================================

def random_text(prefix, length=7):
    suffix = "".join(
        random.choices(string.ascii_lowercase + string.digits, k=length)
    )
    return f"{prefix}{suffix}"


def generate_registration_data():
    unique_id = random_text("", 10)

    return {
        "name": random_text("Participant_"),
        "roll_number": f"HF{random.randint(100000, 999999)}",
        "email": f"participant_{unique_id}@example.com",
        "phone": str(random.randint(6000000000, 9999999999)),
        "college": "Demo Engineering College",
        "team_name": random_text("Team_"),
        "course": "Cloud and DevOps",
    }


# ============================================================
# BROWSER SETUP
# ============================================================

@pytest.fixture
def driver():
    browser = webdriver.Chrome()
    browser.set_window_size(1366, 900)

    yield browser

    print(
        f"\n⏳ Keeping the browser open for "
        f"{RESULT_DISPLAY_TIME} seconds..."
    )
    time.sleep(RESULT_DISPLAY_TIME)
    browser.quit()


# ============================================================
# COMMON FORM OPERATIONS
# ============================================================

def open_registration_page(driver):
    print("STEP 1: Opening the registration website...")
    driver.get(URL)
    pause(PAGE_WAIT)

    assert driver.find_element(By.ID, "name").is_displayed()
    print("        Website opened successfully.")


def fill_registration_form(driver, data):
    fields = [
        ("name", data["name"], "Participant name"),
        ("roll_number", data["roll_number"], "Roll number"),
        ("email", data["email"], "Email address"),
        ("phone", data["phone"], "Phone number"),
        ("college", data["college"], "College name"),
        ("team_name", data["team_name"], "Team name"),
    ]

    print("\nSTEP 2: Automatically filling registration details...")

    for field_id, value, label in fields:
        driver.find_element(By.ID, field_id).send_keys(value)
        print(f"        {label}: {value}")
        pause()

    print(f"\n        Selecting course: {data['course']}")
    Select(driver.find_element(By.ID, "course")).select_by_value(
        data["course"]
    )
    pause()


def submit_form(driver):
    print("\nSTEP 3: Submitting the registration form...")
    driver.find_element(
        By.CSS_SELECTOR, "button[type='submit']"
    ).click()
    pause(PAGE_WAIT)


# ============================================================
# TC01 - WEBSITE AND FORM FIELD CHECK
# ============================================================

def test_website_and_form_fields(driver):
    test_name = "TC01 - Website and Form Fields"

    print("\n\n[TC01] VERIFY WEBSITE AND REGISTRATION FIELDS")
    open_registration_page(driver)

    field_ids = [
        "name",
        "roll_number",
        "email",
        "phone",
        "college",
        "team_name",
        "course",
    ]

    for field_id in field_ids:
        element = driver.find_element(By.ID, field_id)
        assert element.is_displayed(), f"{field_id} is not visible"

    report_test(
        test_name,
        "PASS",
        "Website loaded and all seven expected fields are visible.",
    )


# ============================================================
# TC02 - SUCCESSFUL REGISTRATION
# ============================================================

def test_successful_registration(driver):
    test_name = "TC02 - Successful Registration"

    print("\n\n[TC02] VERIFY SUCCESSFUL REGISTRATION")
    data = generate_registration_data()

    open_registration_page(driver)
    fill_registration_form(driver, data)
    submit_form(driver)

    WebDriverWait(driver, 10).until(
        EC.url_contains("/register")
    )

    page = driver.page_source

    assert data["name"] in page
    assert data["roll_number"] in page
    assert data["email"] in page
    assert data["phone"] in page
    assert "registered" in page.lower()

    report_test(
        test_name,
        "PASS",
        "Registration submitted and generated details appeared on the page.",
    )


# ============================================================
# TC03 - REQUIRED FIELD VALIDATION
# ============================================================

def test_required_field_validation(driver):
    test_name = "TC03 - Required Field Validation"

    print("\n\n[TC03] VERIFY REQUIRED FIELDS")
    open_registration_page(driver)

    for field_id in ["name", "roll_number", "email", "phone"]:
        element = driver.find_element(By.ID, field_id)

        assert element.get_attribute("required") is not None, (
            f"{field_id} is missing required validation"
        )

    name_field = driver.find_element(By.ID, "name")

    assert driver.execute_script(
        "return arguments[0].validity.valueMissing;",
        name_field,
    )

    report_test(
        test_name,
        "PASS",
        "Required fields are configured and an empty name is invalid.",
    )


# ============================================================
# TC04 - MISSING NAME VALIDATION
# ============================================================

def test_missing_name_validation(driver):
    test_name = "TC04 - Missing Name Validation"

    print("\n\n[TC04] VERIFY EMPTY NAME IS REJECTED")
    open_registration_page(driver)

    data = generate_registration_data()

    driver.find_element(
        By.ID, "roll_number"
    ).send_keys(data["roll_number"])
    pause()

    driver.find_element(By.ID, "email").send_keys(data["email"])
    pause()

    driver.find_element(By.ID, "phone").send_keys(data["phone"])
    pause()

    driver.find_element(By.ID, "college").send_keys(data["college"])
    pause()

    driver.find_element(By.ID, "team_name").send_keys(data["team_name"])
    pause()

    Select(driver.find_element(By.ID, "course")).select_by_value(
        data["course"]
    )

    name_field = driver.find_element(By.ID, "name")

    assert driver.execute_script(
        "return arguments[0].validity.valueMissing;",
        name_field,
    )

    report_test(
        test_name,
        "PASS",
        "The browser identifies the empty name as invalid.",
    )


# ============================================================
# TC05 - PHONE NUMBER VALIDATION
# ============================================================

def test_phone_number_validation(driver):
    test_name = "TC05 - Phone Number Validation"

    print("\n\n[TC05] VERIFY PHONE NUMBER FORMAT")
    open_registration_page(driver)

    phone_field = driver.find_element(By.ID, "phone")
    pattern = phone_field.get_attribute("pattern")

    assert pattern == "[0-9]{10}", (
        f"Expected a 10-digit pattern; received {pattern!r}"
    )

    phone_field.send_keys("12345")
    pause()

    assert not driver.execute_script(
        "return arguments[0].checkValidity();",
        phone_field,
    )

    report_test(
        test_name,
        "PASS",
        "A five-digit number fails the configured 10-digit validation.",
    )


# ============================================================
# TC06 - COURSE DROPDOWN
# ============================================================

def test_course_options(driver):
    test_name = "TC06 - Course Dropdown Options"

    print("\n\n[TC06] VERIFY AVAILABLE COURSES")
    open_registration_page(driver)

    dropdown = Select(driver.find_element(By.ID, "course"))

    available_courses = [
        option.get_attribute("value")
        for option in dropdown.options
    ]

    expected_courses = [
        "Artificial Intelligence",
        "Web Development",
        "Cybersecurity",
        "Cloud and DevOps",
        "Open Innovation",
    ]

    for course in expected_courses:
        assert course in available_courses, (
            f"Course option is missing: {course}"
        )

    print("\n        Available course options:")
    for course in available_courses:
        print(f"        - {course}")

    report_test(
        test_name,
        "PASS",
        "All five expected course options are available.",
    )


# ============================================================
# TC07 - RANDOM DATA GENERATION
# ============================================================

def test_random_registration_data(driver):
    test_name = "TC07 - Random Test Data Generation"

    print("\n\n[TC07] VERIFY RANDOM DATA GENERATION")

    first = generate_registration_data()
    second = generate_registration_data()

    assert first["name"] != second["name"]
    assert first["roll_number"] != second["roll_number"]

    print(f"\n        Generated name      : {first['name']}")
    print(f"        Generated roll no.  : {first['roll_number']}")
    print(f"        Generated email    : {first['email']}")
    print(f"        Generated phone    : {first['phone']}")

    report_test(
        test_name,
        "PASS",
        "Different name and roll number values were generated.",
    )


# ============================================================
# FINAL TEST SUMMARY
# ============================================================

class SummaryPlugin:
    def pytest_terminal_summary(self, terminalreporter, exitstatus, config):
        passed = len(terminalreporter.stats.get("passed", []))
        failed = len(terminalreporter.stats.get("failed", []))
        skipped = len(terminalreporter.stats.get("skipped", []))
        errors = len(terminalreporter.stats.get("error", []))

        terminalreporter.write_sep("=", "HACKFORGE TEST EXECUTION SUMMARY")
        terminalreporter.write_line(f"Passed tests  : {passed}")
        terminalreporter.write_line(f"Failed tests  : {failed}")
        terminalreporter.write_line(f"Skipped tests : {skipped}")
        terminalreporter.write_line(f"Setup errors  : {errors}")
        terminalreporter.write_line(
            "Overall result: "
            + ("SUCCESS" if failed == 0 and errors == 0 else "FAILURE")
        )
        terminalreporter.write_sep("=", "END OF AUTOMATION REPORT")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 65)
    print("       HACKFORGE HACKATHON REGISTRATION")
    print("              SELENIUM AUTOMATION")
    print("=" * 65)
    print(f"Website          : {URL}")
    print(f"Action delay     : {ACTION_WAIT} seconds")
    print(f"Page delay       : {PAGE_WAIT} seconds")
    print(f"Browser display  : {RESULT_DISPLAY_TIME} seconds per test")
    print("=" * 65)

    exit_code = pytest.main(
        ["-v", "-s", __file__],
        plugins=[SummaryPlugin()],
    )

    print("\nAutomation execution completed.")
    raise SystemExit(exit_code)
