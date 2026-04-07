DELIMITER //

DROP TRIGGER IF EXISTS expense_insert_audit //
CREATE TRIGGER expense_insert_audit
AFTER INSERT ON expenses
FOR EACH ROW
BEGIN
  INSERT INTO audit_log(action)
  VALUES(CONCAT('Expense added with ID: ', NEW.expense_id));
END //

DELIMITER ;