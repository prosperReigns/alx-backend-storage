-- This SQL script creates a stored procedure ComputeAverageScoreForUser that
-- computes and stores the average score for a student.

DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser (IN input_user_id INT)
BEGIN
    DECLARE average_value FLOAT;

    SELECT AVG(score) INTO average_value
    FROM corrections
    WHERE user_id = input_user_id;

    UPDATE users SET average_score = average_value
    WHERE id = input_user_id;
END$$

DELIMITER ;
