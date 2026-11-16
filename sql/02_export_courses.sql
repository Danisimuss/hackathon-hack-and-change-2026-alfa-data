SELECT
    c."Id" AS course_id,
    c."Title" AS title,
    c."Description" AS description,
    c."Target" AS target,
    t."Title" AS access_type,
    c."Cost" AS price,
    c."Duration" AS duration,
    c."Url" AS url_path
FROM "Courses" c
JOIN "Statuses" s ON c."StatusId" = s."Id"
LEFT JOIN "CourseTypes" t ON c."TypeId" = t."Id"
WHERE s."Title" = 'Опубликовано'
  AND c."IsDeleted" = false
ORDER BY c."Title";
