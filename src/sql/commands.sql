
SELECT * FROM users WHERE username='kakka';

SELECT * FROM joo;
 

SELECT * FROM information_schema.tables WHERE username=creeppa;


ALTER TABLE joo ADD COLUMN user_id INTEGER;

ALTER TABLE joo
ADD CONSTRAINT user_id_fk
FOREIGN KEY (user_id)
REFERENCES users(id);



SELECT * FROM information_schema.tables WHERE user_id = users.id;

SELECT * FROM users;

SELECT * FROM huhuu2;

INSERT INTO users (username,password) VALUES ('huhuu2','qwerty')





CREATE TABLE huhuu2(
            query_id        SERIAL PRIMARY KEY,
            user_id         int,
            start_date      varchar(255) NOT NULL,
            start_time      varchar(255) NOT NULL,
            end_date        varchar(255) NOT NULL,
            end_time        varchar(255) NOT NULL,
            project_name    varchar(255) NOT NULL,
            definition      varchar(255) NOT NULL,
            CONSTRAINT fk_users
            FOREIGN KEY (user_id)
            REFERENCES users(id)

)


INSERT INTO huhuu (
    id,
    user_id,
    start_date,
    start_time,
    end_date,
    end_time,
    project_name,
    definition
  )

VALUES (
    2,
    (SELECT id FROM users WHERE username='huhuu'),
    '25/11/2020',
    '15:22',
    '28/11/2021',
    '11:11',
    'aaa',
    'aaaa'
  );



  INSERT INTO huhuu2 (
      user_id,
      start_date,
      start_time,
      end_date,
      end_time,
      project_name,
      definition
    )
  VALUES (
     (SELECT id FROM users WHERE username='huhuu2'),
        '25/11/2020',
        '15:22',
        '28/11/2021',
        '11:11',
        'aaa',
        'aaaa'
    );




SELECT * FROM information_schema.tables WHERE user_id = users.id;

-- HAKEE KAIKKI TAULUT JOTKA ON KÄYTTÄJÄNIMISSÄ
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES, users WHERE TABLE_NAME = users.username;

SELECT * FROM creeppa;


