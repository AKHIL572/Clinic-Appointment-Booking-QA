from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage, by_qa, by_testid


class PatientDashboardPage(BasePage):
    SEARCH_BOX = (By.ID, "search_specialization")
    SEARCH_BUTTON = (By.ID, "search_button")
    RESULTS = (By.ID, "doctor-results")
    DOCTOR_NAMES = (By.CSS_SELECTOR, "[data-testid='doctor-card'] h3")
    APPOINTMENT_ROWS = by_testid("appointment-row")
    CANCEL_BUTTON = by_qa("cancel-button")

    def open_page(self):
        self.visit("/patient/dashboard")
        self.wait_for_path("/patient/dashboard")
        return self

    def search(self, text):
        old_results = self.find(self.RESULTS)
        self.type_into(self.SEARCH_BOX, text)
        self.click(self.SEARCH_BUTTON)
        self.wait.until(EC.staleness_of(old_results))   # page reloaded
        self.find(self.RESULTS)

    def doctor_names(self):
        return [e.text for e in self.driver.find_elements(*self.DOCTOR_NAMES)]

    def has_no_results(self):
        return bool(self.driver.find_elements(*by_testid("no-results")))

    def open_doctor(self, name):
        xpath = f"//div[@data-testid='doctor-card'][.//h3[normalize-space()='{name}']]//a"
        self.click((By.XPATH, xpath))
        self.wait.until(lambda d: "/patient/doctor/" in d.current_url)
        return DoctorDetailPage(self.driver)

    def appointment_rows(self):
        return self.driver.find_elements(*self.APPOINTMENT_ROWS)

    def appointment_row(self, text):
        return self.find_xpath(f"//tr[@data-testid='appointment-row'][contains(., '{text}')]")

    def cancel_appointment(self, row_text):
        self.appointment_row(row_text).find_element(*self.CANCEL_BUTTON).click()

    def upload_prescription(self, row_text, file_path):
        row = self.appointment_row(row_text)
        row.find_element(*by_qa("upload-input")).send_keys(file_path)
        row.find_element(*by_qa("upload-button")).click()

    def has_empty_state(self):
        return bool(self.driver.find_elements(*by_testid("no-appointments")))


class DoctorDetailPage(BasePage):
    BOOK_BUTTON = by_qa("book-slot-button")

    @staticmethod
    def _slot_xpath(slot):
        return (f"//div[@data-testid='slot-card']"
                f"[contains(., '{slot['date']}') and contains(., '{slot['start']} - {slot['end']}')]")

    def card(self, slot):
        return self.find_xpath(self._slot_xpath(slot))

    def has_slot(self, slot):
        return bool(self.find_all_xpath(self._slot_xpath(slot)))

    def is_full(self, slot):
        return "(full)" in self.card(slot).text.lower()

    def has_book_button(self, slot):
        return bool(self.card(slot).find_elements(*self.BOOK_BUTTON))

    def book(self, slot):
        self.card(slot).find_element(*self.BOOK_BUTTON).click()

    def book_action(self, slot):
        """The URL the 'Book this slot' form posts to (used to replay a stale booking)."""
        button = self.card(slot).find_element(*self.BOOK_BUTTON)
        return button.find_element(By.XPATH, "ancestor::form").get_attribute("action")

    def replay_post(self, action_url):
        """Re-send a booking POST exactly as a stale, already-open page would."""
        self.driver.execute_script(
            "const f = document.createElement('form');"
            "f.method = 'POST'; f.action = arguments[0];"
            "document.body.appendChild(f); f.submit();", action_url)
