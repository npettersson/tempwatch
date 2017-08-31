CREATE TABLE tempvalues (
  log_id int NOT NULL AUTO_INCREMENT,
  sensor_id varchar(45) NOT NULL,
  temp_value float NOT NULL,
  log_date datetime NOT NULL,
  status varchar(10) NOT NULL DEFAULT 'NOT_SENT',
  sent_ts timestamp NULL DEFAULT NULL,
  PRIMARY KEY (log_id)
)