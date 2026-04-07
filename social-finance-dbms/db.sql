CREATE DATABASE social_finance;

USE social_finance;

CREATE TABLE users(
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15)
);

CREATE TABLE groups_table(
    group_id INT PRIMARY KEY AUTO_INCREMENT,
    group_name VARCHAR(100),
    created_by INT,
    FOREIGN KEY(created_by) REFERENCES users(user_id)
);

CREATE TABLE expenses(
    expense_id INT PRIMARY KEY AUTO_INCREMENT,
    group_id INT,
    amount DECIMAL(10,2),
    description VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(group_id) REFERENCES groups_table(group_id)
);

CREATE TABLE loans(
    loan_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    loan_amount DECIMAL(10,2),
    interest_rate DECIMAL(5,2),
    duration INT,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE emi_payments(
    emi_id INT PRIMARY KEY AUTO_INCREMENT,
    loan_id INT,
    emi_amount DECIMAL(10,2),
    payment_date DATE,
    FOREIGN KEY(loan_id) REFERENCES loans(loan_id)
);

CREATE TABLE audit_log(
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    action VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users(name,email,phone)
VALUES('Sameera','sameera@email.com','9876543210');

INSERT INTO loans(user_id,loan_amount,interest_rate,duration)
VALUES(1,10000,5,10);

INSERT INTO emi_payments(loan_id)
VALUES(1)