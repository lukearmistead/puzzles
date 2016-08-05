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
