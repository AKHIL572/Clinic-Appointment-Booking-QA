from pages.base_page import BasePage, by_qa


class DoctorDashboardPage(BasePage):
    COMPLETE_BUTTON = by_qa("complete-button")

    def open_page(self):
        self.visit("/doctor/dashboard")
        self.wait_for_path("/doctor/dashboard")
        return self

    def row_for(self, text):
        return self.find_xpath(f"//tr[@data-testid='appointment-row'][contains(., '{text}')]")

    def rows_matching(self, text):
        return self.find_all_xpath(f"//tr[@data-testid='appointment-row'][contains(., '{text}')]")

    def complete(self, row_text):
        self.row_for(row_text).find_element(*self.COMPLETE_BUTTON).click()
