-- QUERIE QUESTIONS
SELECT Id, CreationDate, Title, Body, Tags, AnswerCount, 
       ViewCount, CommentCount, FavoriteCount, Score
    FROM `sotorrent-org.2018_09_23.Posts`
    WHERE Tags LIKE '%microservice%' AND AnswerCount >= 1

-- QUERIE ANSWERS
SELECT Id, ParentId, CreationDate, Title, Body, Tags, AnswerCount, 
       ViewCount, CommentCount, FavoriteCount, Score
    FROM `sotorrent-org.2018_09_23.Posts`
    WHERE ParentId IN ({})