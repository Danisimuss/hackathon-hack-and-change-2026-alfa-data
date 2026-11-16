SELECT
    COUNT(*) AS total_courses,
    COUNT(*) - COUNT("Description") AS missing_description,
    COUNT(*) - COUNT("Duration") AS missing_duration,
    COUNT(*) - COUNT("Url") AS missing_url,
    MIN("Rating") AS min_rating,
    MAX("Rating") AS max_rating
FROM "Courses";

SELECT "Id", COUNT(*)
FROM "Courses"
GROUP BY "Id"
HAVING COUNT(*) > 1;
