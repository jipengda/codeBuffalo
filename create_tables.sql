CREATE TABLE activity_attribute(
attribute_id INT AUTO_INCREMENT PRIMARY KEY,
attribute_text VARCHAR(255) UNIQUE
);

CREATE TABLE activity_attribute_ref(
activity_key INT NOT NULL,
attribute_id INT NOT NULL REFERENCES activity_attribute(attribute_id),
activity_has_attribute BOOLEAN NOT NULL
);
