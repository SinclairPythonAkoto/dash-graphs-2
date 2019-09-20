DROP TABLE if exists flight_num;
CREATE TABLE flight_num (
  id SERIAL PRIMARY KEY,
  city VARCHAR,
  amount INTEGER
  );