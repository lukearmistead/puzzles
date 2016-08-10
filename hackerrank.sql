/* 
Query the two cities in STATION with the shortest and longest CITY names, as well as their respective lengths (i.e.: number of characters in the name). If there is more than one smallest or largest city, choose the one that comes first when ordered alphabetically.
*/

SELECT CITY, LENGTH(CITY)
FROM STATION
WHERE ID = (
    SELECT ID
    FROM STATION
    ORDER BY LENGTH(CITY), CITY
    LIMIT 1
    )
OR ID = (
    SELECT ID
    FROM STATION
    ORDER BY LENGTH(CITY) DESC, CITY
    LIMIT 1
    );

-- OTHER ANSWERS
(select CITY, length(CITY) from STATION order by length(CITY) limit 1)
UNION
(select CITY, length(CITY) from STATION order by length(CITY) DESC limit 1);

/* 
Query the list of CITY names starting with vowels (a, e, i, o, u) from STATION. Your result cannot contain duplicates.
*/

SELECT DISTINCT CITY
FROM STATION
WHERE LEFT(LOWER(CITY), 1) IN ('a', 'e', 'i', 'o', 'u');

/*
Query the Name of any student in STUDENTS who scored higher than  Marks. Order your output by the last three characters of each name. If two or more students both have names ending in the same last three characters (i.e.: Bobby, Robby, etc.), secondary sort them by ascending ID.
*/

SELECT NAME
FROM STUDENTS
WHERE MARKS > 75
ORDER BY RIGHT(NAME, 3), ID;
/*
Write a query identifying the type of each record in the TRIANGLES table using its three side lengths. Output one of the following statements for each record in the table:

Not A Triangle: The given values of A, B, and C don't form a triangle.
Equilateral: It's a triangle with  sides of equal length.
Isosceles: It's a triangle with  sides of equal length.
Scalene: It's a triangle with  sides of differing lengths.
*/

SELECT CASE
    WHEN C >= A + B OR A >= B + C OR B >= A + C THEN "Not A Triangle"
    WHEN A = B AND B = C THEN "Equilateral"
    WHEN A = C OR B = C OR A = B THEN "Isosceles"
    WHEN A <> B AND B <> C AND C <> A THEN "Scalene"
    ELSE "NA"
    END 
FROM TRIANGLES;

/*
Generate the following two result sets:

Query an alphabetically ordered list of all names in OCCUPATIONS, immediately followed by the first letter of each profession as a parenthetical (i.e.: enclosed in parentheses). For example: AnActorName(A), ADoctorName(D), AProfessorName(P), and ASingerName(S).
Query the number of ocurrences of each occupation in OCCUPATIONS. Sort the occurrences in ascending order, and output them in the following format: 

There are total [occupation_count] [occupation]s.
where [occupation_count] is the number of occurrences of an occupation in OCCUPATIONS and [occupation] is the lowercase occupation name. If more than one Occupation has the same [occupation_count], they should be ordered alphabetically.

Note: There will be at least two entries in the table for each type of occupation.

*/

SELECT CONCAT(Name, "(", LEFT(Occupation, 1), ")")
FROM OCCUPATIONS
ORDER BY Name
UNION
SELECT 
    CONCAT("There are ",COUNT(Occupation), " ", Occupation, "s")
FROM OCCUPATIONS
GROUP BY Occupation;

/*
We define an employee's total earnings to be their monthly  worked, and the maximum total earnings to be the maximum total earnings for any employee in the Employee table. Write a query to find the maximum total earnings for all employees as well as the total number of employees who have maximum total earnings. Then print these values as  space-separated integers.

*/

SELECT CONCAT(salary * months, " ", COUNT(salary * months))
FROM Employee
GROUP BY salary * months
ORDER BY salary * months DESC
LIMIT 1;

-- Another option
select salary * months, count(*) 
from employee 
 where salary * months= (
    select max(salary * months) from employee
    )
group by salary * months;

/*
Query the Western Longitude (LONG_W) for the largest Northern Latitude (LAT_N) in STATION that is less than . Round your answer to  decimal places.
*/

 SELECT ROUND(LONG_W, 4)
FROM STATION
WHERE LAT_N = (
    SELECT MAX(LAT_N) FROM STATION WHERE LAT_N < 137.2345
    );

/*
GET MEDIAN
*/

-- Gathers total row count
set @ct := (SELECT COUNT(*) FROM STATION);
-- Initializes row number at 0
set @row_id := 0;
 
-- Average for two median positions in the case of an even number of rows
SELECT ROUND(AVG(LAT_N), 4) AS median
FROM (
    SELECT * FROM STATION ORDER BY LAT_N
    ) AS S1
-- Simultaneously increments row_id to get a number for each row and
-- performs the check that the row is in the middle
WHERE (SELECT @row_id := @row_id + 1)
BETWEEN @ct/2.0 AND @ct/2.0 + 1;
