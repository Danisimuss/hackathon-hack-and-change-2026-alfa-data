SELECT
    c."Id" AS course_id,
    c."Title" AS course_title,
    t."Id" AS topic_id,
    t."Title" AS topic
FROM "Courses" c
JOIN "Statuses" s ON c."StatusId" = s."Id"
LEFT JOIN "ContentSettings" cs ON cs."EntityId" = c."Id"
LEFT JOIN "ContentSettingsTopics" ct ON ct."ContentSettingsId" = cs."Id"
LEFT JOIN "Topics" t ON t."Id" = ct."TopicId"
WHERE s."Title" = 'Опубликовано'
  AND c."IsDeleted" = false;

SELECT cs."EntityId", COUNT(DISTINCT cs."EntityTypeId") AS entity_types
FROM "ContentSettings" cs
JOIN "Courses" c ON cs."EntityId" = c."Id"
GROUP BY cs."EntityId"
HAVING COUNT(DISTINCT cs."EntityTypeId") > 1;
