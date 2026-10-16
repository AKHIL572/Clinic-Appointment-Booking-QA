from selenium.webdriver.common.by import By

from pages.base_page import BasePage, by_qa


class AdminDashboardPage(BasePage):
    def open_page(self):
        self.visit("/admin/dashboard")
        self.wait_for_path("/admin/dashboard")
        return self

    def click_add_doctor(self):
        self.click(by_qa("add-doctor-link"))
        return NewDoctorPage(self.driver)

    def doctor_rows(self, name):
        return self.find_all_xpath(f"//tr[@data-testid='doctor-row'][contains(., '{name}')]")

    def click_add_slot_for(self, doctor_name):
        row = self.find_xpath(f"//tr[@data-testid='doctor-row'][contains(., '{doctor_name}')]")
        row.find_element(By.XPATH, ".//a[contains(@href, '/slots/new')]").click()
        return NewSlotPage(self.driver)

    def slot_rows(self, text):
        return self.find_all_xpath(f"//tr[@data-testid='slot-row'][contains(., '{text}')]")


class NewDoctorPage(BasePage):
    def create(self, name, email, specialization, password):
        self.type_into((By.ID, "doctor-name"), name)
        self.type_into((By.ID, "doctor-email"), email)
        self.type_into((By.ID, "doctor-specialization"), specialization)
        self.type_into((By.ID, "doctor-password"), password)
        self.click(by_qa("save-doctor-button"))


class NewSlotPage(BasePage):
    def create(self, date_iso, start, end, capacity):
        date_box = self.find((By.ID, "slot-date"))
        # Typing into <input type="date"> depends on the browser locale, so set it directly.
        self.driver.execute_script("arguments[0].value = arguments[1];", date_box, date_iso)
        self.type_into((By.ID, "slot-start"), start)
        self.type_into((By.ID, "slot-end"), end)
        self.type_into((By.ID, "slot-capacity"), str(capacity))
        self.click(by_qa("save-slot-button"))
