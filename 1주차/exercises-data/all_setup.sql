-- ============================================================
-- 전체 연습문제 통합 셋업 파일
-- 01~06강 모든 테이블을 한 번에 생성합니다.
-- ============================================================

-- ============================================================
-- [01강] EMPLOYEE, INSTRUCTOR, MEDALS
-- ============================================================
DROP TABLE IF EXISTS EMPLOYEE;

CREATE TABLE EMPLOYEE (
    EMP_ID   CHAR(4)        NOT NULL,
    NAME     VARCHAR(30)    NOT NULL,
    DEPT     VARCHAR(20),
    SALARY   DECIMAL(10, 2),
    COUNTRY  VARCHAR(30),
    PRIMARY KEY (EMP_ID)
);

INSERT INTO EMPLOYEE VALUES
    ('E001', 'Kim Minjun',   'Engineering',  75000.00, 'Korea'),
    ('E002', 'Lee Soyeon',   'Marketing',    52000.00, 'Korea'),
    ('E003', 'Park Jinho',   'HR',           48000.00, 'Korea'),
    ('E004', 'John Smith',   'Engineering',  82000.00, 'USA'),
    ('E005', 'Maria Garcia', 'Marketing',    61000.00, 'USA'),
    ('E006', 'James Brown',  'HR',           45000.00, 'USA'),
    ('E007', 'Priya Sharma', 'Engineering',  70000.00, 'India'),
    ('E008', 'Liu Wei',      'Data Science', 88000.00, 'China'),
    ('E009', 'Ana Silva',    'Data Science', 92000.00, 'Brazil'),
    ('E010', 'Tom Wilson',   'HR',           47000.00, 'UK');

DROP TABLE IF EXISTS INSTRUCTOR;

CREATE TABLE INSTRUCTOR (
    ID    CHAR(2)      PRIMARY KEY,
    NAME  VARCHAR(30),
    DEPT  VARCHAR(30)
);

INSERT INTO INSTRUCTOR VALUES
    ('A1', 'John Kim',  'Data Science'),
    ('A2', 'Jane Lee',  'SQL'),
    ('A3', 'Mike Park', 'Python');

DROP TABLE IF EXISTS MEDALS;

CREATE TABLE MEDALS (
    ID      INTEGER      PRIMARY KEY,
    COUNTRY VARCHAR(30),
    YEAR    INTEGER,
    SPORT   VARCHAR(30),
    GOLD    INTEGER,
    SILVER  INTEGER,
    BRONZE  INTEGER
);

INSERT INTO MEDALS VALUES
    (1,  'USA',       2020, 'Athletics', 10, 8, 6),
    (2,  'China',     2020, 'Swimming',   8, 6, 4),
    (3,  'USA',       2020, 'Swimming',   6, 5, 3),
    (4,  'Japan',     2020, 'Judo',       9, 2, 1),
    (5,  'Korea',     2020, 'Archery',    4, 2, 3),
    (6,  'UK',        2020, 'Cycling',    6, 7, 6),
    (7,  'Australia', 2020, 'Swimming',   5, 3, 5),
    (8,  'France',    2020, 'Athletics',  3, 5, 4),
    (9,  'Germany',   2020, 'Rowing',     4, 3, 2),
    (10, 'Canada',    2020, 'Wrestling',  2, 4, 5);

-- ============================================================
-- [02강 / 03강] AUTHOR, BOOK
-- ============================================================
DROP TABLE IF EXISTS BOOK;
DROP TABLE IF EXISTS AUTHOR;

CREATE TABLE AUTHOR (
    AUTHOR_ID  CHAR(2)       PRIMARY KEY,
    FIRSTNAME  VARCHAR(20),
    LASTNAME   VARCHAR(20),
    COUNTRY    VARCHAR(20),
    BIRTHDATE  DATE
);

INSERT INTO AUTHOR VALUES
    ('A1', 'Patrick',  'Modiano',  'France',    '1945-07-30'),
    ('A2', 'Haruki',   'Murakami', 'Japan',     '1949-01-12'),
    ('A3', 'Gabriel',  'Silva',    'Brazil',    '1960-03-15'),
    ('A4', 'Jane',     'Smith',    'Australia', '1975-06-22'),
    ('A5', 'Carlos',   'Santos',   'Spain',     '1958-09-08'),
    ('A6', 'Emma',     'Stone',    'Canada',    '1980-11-14'),
    ('A7', 'Raj',      'Sharma',   'India',     '1965-02-28'),
    ('A8', 'Sophie',   'Martin',   'France',    '1972-08-19');

CREATE TABLE BOOK (
    BOOK_ID        CHAR(4)        PRIMARY KEY,
    TITLE          VARCHAR(100),
    AUTHOR_ID      CHAR(2),
    PRICE          DECIMAL(6, 2),
    YEAR_PUBLISHED INTEGER,
    FOREIGN KEY (AUTHOR_ID) REFERENCES AUTHOR(AUTHOR_ID)
);

INSERT INTO BOOK VALUES
    ('B001', 'The Night Watch',   'A1', 15.99, 1999),
    ('B002', 'Norwegian Wood',    'A2', 18.50, 1987),
    ('B003', 'Ocean Echoes',      'A3', 12.00, 2005),
    ('B004', 'Red Summer',        'A4', 22.00, 2018),
    ('B005', 'Dark Wind',         'A5', 19.99, 2010),
    ('B006', 'Morning Light',     'A6', 14.50, 2015),
    ('B007', 'Silver Thread',     'A7', 16.75, 2012),
    ('B008', 'Paris Letters',     'A1', 21.00, 2008),
    ('B009', 'Tokyo Dreams',      'A2', 24.99, 2002),
    ('B010', 'Mountain Road',     'A4', 11.00, 2020);

-- ============================================================
-- [04강] PETRESCUE, SALES, DEPARTMENTS, EMPLOYEES
-- ============================================================
DROP TABLE IF EXISTS PETRESCUE;

CREATE TABLE PETRESCUE (
    ID          INTEGER        PRIMARY KEY,
    ANIMAL      VARCHAR(20),
    QUANTITY    INTEGER,
    COST        DECIMAL(8, 2),
    RESCUEDATE  DATE
);

INSERT INTO PETRESCUE VALUES
    (1,  'Dog',     2, 450.00, '2021-05-15'),
    (2,  'Cat',     3, 300.00, '2021-06-20'),
    (3,  'Parrot',  1, 150.00, '2021-07-10'),
    (4,  'Dog',     1, 225.00, '2021-08-05'),
    (5,  'Rabbit',  2, 180.00, '2021-09-12'),
    (6,  'Cat',     1, 100.00, '2021-10-03'),
    (7,  'Dog',     3, 675.00, '2021-11-18'),
    (8,  'Hamster', 4, 120.00, '2021-12-01'),
    (9,  'Parrot',  2, 300.00, '2022-01-15'),
    (10, 'Cat',     2, 200.00, '2022-02-28');

DROP TABLE IF EXISTS SALES;

CREATE TABLE SALES (
    ID        INTEGER        PRIMARY KEY,
    PRODUCT   VARCHAR(50),
    AMOUNT    DECIMAL(10, 2),
    SALEDATE  DATE
);

INSERT INTO SALES VALUES
    (1,  'Laptop',   1200.00, '2023-01-15'),
    (2,  'Keyboard',  150.00, '2023-02-10'),
    (3,  'Monitor',   450.00, '2023-02-20'),
    (4,  'Laptop',   1350.00, '2023-03-05'),
    (5,  'Mouse',      80.00, '2023-03-18'),
    (6,  'Tablet',    750.00, '2023-04-12'),
    (7,  'Keyboard',  200.00, '2023-05-08'),
    (8,  'Monitor',   500.00, '2023-06-22'),
    (9,  'Laptop',   1100.00, '2023-07-14'),
    (10, 'Tablet',    820.00, '2023-08-30');

DROP TABLE IF EXISTS EMPLOYEES;
DROP TABLE IF EXISTS DEPARTMENTS;

CREATE TABLE DEPARTMENTS (
    DEPT_ID_DEP  CHAR(3)      PRIMARY KEY,
    DEP_NAME     VARCHAR(30),
    MANAGER_ID   CHAR(4),
    LOCATION     VARCHAR(30)
);

INSERT INTO DEPARTMENTS VALUES
    ('D01', 'Engineering',  'E004', 'Seoul'),
    ('D02', 'Marketing',    'E005', 'New York'),
    ('D03', 'HR',           'E006', 'London'),
    ('D04', 'Data Science', 'E008', 'Beijing');

CREATE TABLE EMPLOYEES (
    EMP_ID     CHAR(4)        PRIMARY KEY,
    F_NAME     VARCHAR(20),
    L_NAME     VARCHAR(20),
    DEP_ID     CHAR(3),
    SALARY     DECIMAL(10, 2),
    JOB_TITLE  VARCHAR(30),
    FOREIGN KEY (DEP_ID) REFERENCES DEPARTMENTS(DEPT_ID_DEP)
);

INSERT INTO EMPLOYEES VALUES
    ('E001', 'Minjun', 'Kim',    'D01', 75000.00, 'Software Engineer'),
    ('E002', 'Soyeon', 'Lee',    'D02', 52000.00, 'Marketing Manager'),
    ('E003', 'Jinho',  'Park',   'D03', 48000.00, 'HR Specialist'),
    ('E004', 'John',   'Smith',  'D01', 82000.00, 'Senior Engineer'),
    ('E005', 'Maria',  'Garcia', 'D02', 61000.00, 'Marketing Analyst'),
    ('E006', 'James',  'Brown',  'D03', 45000.00, 'HR Manager'),
    ('E007', 'Priya',  'Sharma', 'D01', 70000.00, 'Data Engineer'),
    ('E008', 'Wei',    'Liu',    'D04', 88000.00, 'Data Scientist'),
    ('E009', 'Ana',    'Silva',  'D04', 92000.00, 'ML Engineer'),
    ('E010', 'Tom',    'Wilson', 'D03', 47000.00, 'Recruiter');

-- ============================================================
-- [05강] MENU (영양 정보)
-- ============================================================
DROP TABLE IF EXISTS MENU;

CREATE TABLE MENU (
    Item         VARCHAR(100),
    Category     VARCHAR(50),
    Serving_Size VARCHAR(30),
    Calories     INTEGER,
    Total_Fat    DECIMAL(5, 1),
    Sodium       INTEGER,
    Protein      DECIMAL(5, 1)
);

INSERT INTO MENU VALUES
    ('Big Mac',             'Burgers',   '219g',   540, 28.0,  950, 25.0),
    ('McChicken',           'Chicken',   '164g',   400, 16.0,  700, 14.0),
    ('McDouble',            'Burgers',   '174g',   390, 19.0,  750, 23.0),
    ('Filet-O-Fish',        'Fish',      '142g',   390, 19.0,  580, 15.0),
    ('Quarter Pounder',     'Burgers',   '198g',   520, 26.0, 1100, 30.0),
    ('McNuggets (10pc)',     'Chicken',   '162g',   440, 27.0,  900, 23.0),
    ('Egg McMuffin',        'Breakfast', '135g',   300, 13.0,  760, 17.0),
    ('French Fries (M)',    'Sides',     '117g',   340, 16.0,  310,  4.0),
    ('Apple Pie',           'Desserts',   '77g',   250, 11.0,  170,  2.0),
    ('Iced Coffee',         'Beverages', '355mL',  140,  6.0,   95,  2.0),
    ('Chocolate Shake',     'Beverages', '473mL',  530, 13.0,  290, 12.0),
    ('Caesar Salad',        'Salads',    '225g',    90,  4.0,  190,  7.0);

-- ============================================================
-- [06강] JOBS, BORROWER, LOAN
-- ============================================================
DROP TABLE IF EXISTS JOBS;

CREATE TABLE JOBS (
    JOB_ID      CHAR(4)        PRIMARY KEY,
    JOB_TITLE   VARCHAR(50),
    MIN_SALARY  DECIMAL(10, 2),
    MAX_SALARY  DECIMAL(10, 2)
);

INSERT INTO JOBS VALUES
    ('J001', 'Software Engineer',  60000.00, 120000.00),
    ('J002', 'Marketing Manager',  45000.00,  85000.00),
    ('J003', 'HR Specialist',      40000.00,  70000.00),
    ('J004', 'Data Scientist',     75000.00, 150000.00),
    ('J005', 'Recruiter',          38000.00,  65000.00),
    ('J006', 'Senior Engineer',    80000.00, 140000.00),
    ('J007', 'ML Engineer',        85000.00, 160000.00);

DROP TABLE IF EXISTS LOAN;
DROP TABLE IF EXISTS BORROWER;

CREATE TABLE BORROWER (
    BORROWER_ID  CHAR(4)        PRIMARY KEY,
    NAME         VARCHAR(30),
    EMAIL        VARCHAR(50),
    CITY         VARCHAR(30)
);

INSERT INTO BORROWER VALUES
    ('B001', 'Kim Jiyeon',   'jiyeon@email.com',   'Seoul'),
    ('B002', 'Park Sungmin', 'sungmin@email.com',  'Busan'),
    ('B003', 'Lee Narae',    'narae@email.com',    'Seoul'),
    ('B004', 'Choi Dongwoo', 'dongwoo@email.com',  'Incheon'),
    ('B005', 'Jung Haerin',  'haerin@email.com',   'Daejeon');

CREATE TABLE LOAN (
    LOAN_ID      CHAR(4)    PRIMARY KEY,
    BORROWER_ID  CHAR(4),
    BOOK_ID      CHAR(4),
    LOAN_DATE    DATE,
    RETURN_DATE  DATE,
    FOREIGN KEY (BORROWER_ID) REFERENCES BORROWER(BORROWER_ID)
);

INSERT INTO LOAN VALUES
    ('L001', 'B001', 'B002', '2024-01-10', '2024-02-10'),
    ('L002', 'B002', 'B005', '2024-01-15',         NULL),
    ('L003', 'B001', 'B009', '2024-02-01', '2024-03-01'),
    ('L004', 'B003', 'B001', '2024-02-20',         NULL),
    ('L005', 'B002', 'B003', '2024-03-05', '2024-04-05');
