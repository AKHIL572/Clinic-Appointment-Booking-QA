import flows


def test_patient_can_upload_a_prescription(driver, patient, tmp_path):
    slot = flows.create_slot(driver)
    dashboard = flows.book_as(driver, patient, slot)
    pdf = tmp_path / "prescription.pdf"
    pdf.write_bytes(b"%PDF-1.4 test file")

    dashboard.upload_prescription(slot["date"], str(pdf))
    dashboard.wait_for_flash("success", "Prescription uploaded.")
    assert "prescription.pdf" in dashboard.appointment_row(slot["date"]).text


def test_unsupported_prescription_file_type_is_rejected(driver, patient, tmp_path):
    slot = flows.create_slot(driver)
    dashboard = flows.book_as(driver, patient, slot)
    bad_file = tmp_path / "notes.txt"
    bad_file.write_text("not a prescription")

    dashboard.upload_prescription(slot["date"], str(bad_file))
    dashboard.wait_for_flash("error", "Unsupported file type")
    assert "notes.txt" not in dashboard.appointment_row(slot["date"]).text


def test_cancelled_appointment_has_no_upload_option(driver, patient):
    slot = flows.create_slot(driver)
    dashboard = flows.book_as(driver, patient, slot)
    dashboard.cancel_appointment(slot["date"])
    dashboard.wait_for_flash("success", "Appointment cancelled.")
    row = dashboard.appointment_row(slot["date"])
    assert row.find_elements("css selector", "[data-qa='upload-input']") == []
