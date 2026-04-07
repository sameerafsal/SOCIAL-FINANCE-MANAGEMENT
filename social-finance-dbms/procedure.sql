DELIMITER //

DROP PROCEDURE IF EXISTS calculate_emi //
CREATE PROCEDURE calculate_emi()
BEGIN
  UPDATE emi_payments AS ep
  INNER JOIN loans AS l
    ON ep.loan_id = l.loan_id
  SET ep.emi_amount = (l.loan_amount * (1 + l.interest_rate/100)) / l.duration;
END //

DELIMITER ;