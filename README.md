# first_streamlit_app


Features to add:
1) Warehouse usage tracker
2) Warehouse on/off grid
3) Task tracker
4) Task on/off grid
5) Snowpipe tracker
6) Snowpipe on/off grid
7) Role > privelages display
8) Most expensive query history

Cost analysis:
1) Cost saving of stopping warehouse via autosuspend v.s. time lost from losing the cached data
2) Analysis of which warehouse size is best suited to each query (smaller isn't always cheaper) scale out v.s scale up
3) See slide 662 in snowflake notes, there are lots of things that could be monitored to help keep costs down
4) How to determine the most expensive queries from the last 30 days
5) How to determine the top 10 queries with the most spillage to remote storage


=======================================
SEE LAB 21 FOR USEFUL QUERIES

e.g. most expensive queries over last 30 days

WITH WAREHOUSE_SIZE AS
(
     SELECT WAREHOUSE_SIZE, NODES
       FROM (
              SELECT 'XSMALL' AS WAREHOUSE_SIZE, 1 AS NODES
              UNION ALL
              SELECT 'SMALL' AS WAREHOUSE_SIZE, 2 AS NODES
              UNION ALL
              SELECT 'MEDIUM' AS WAREHOUSE_SIZE, 4 AS NODES
              UNION ALL
              SELECT 'LARGE' AS WAREHOUSE_SIZE, 8 AS NODES
              UNION ALL
              SELECT 'XLARGE' AS WAREHOUSE_SIZE, 16 AS NODES
              UNION ALL
              SELECT '2XLARGE' AS WAREHOUSE_SIZE, 32 AS NODES
              UNION ALL
              SELECT '3XLARGE' AS WAREHOUSE_SIZE, 64 AS NODES
              UNION ALL
              SELECT '4XLARGE' AS WAREHOUSE_SIZE, 128 AS NODES
            )
),
QUERY_HISTORY AS
(
     SELECT QH.QUERY_ID
           ,QH.QUERY_TEXT
           ,QH.USER_NAME
           ,QH.ROLE_NAME
           ,QH.EXECUTION_TIME
           ,QH.WAREHOUSE_SIZE
      FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY QH
     WHERE START_TIME > DATEADD(month,-2,CURRENT_TIMESTAMP())
)

SELECT QH.QUERY_ID
      ,'https://' || current_account() || '.snowflakecomputing.com/console#/monitoring/queries/detail?queryId='
            ||QH.QUERY_ID AS QU
      ,QH.QUERY_TEXT
      ,QH.USER_NAME
      ,QH.ROLE_NAME
      ,QH.EXECUTION_TIME as EXECUTION_TIME_MILLISECONDS
      ,(QH.EXECUTION_TIME/(1000)) as EXECUTION_TIME_SECONDS
      ,(QH.EXECUTION_TIME/(1000*60)) AS EXECUTION_TIME_MINUTES
      ,(QH.EXECUTION_TIME/(1000*60*60)) AS EXECUTION_TIME_HOURS
      ,WS.WAREHOUSE_SIZE
      ,WS.NODES
      ,(QH.EXECUTION_TIME/(1000*60*60))*WS.NODES as RELATIVE_PERFORMANCE_COST

FROM QUERY_HISTORY QH
JOIN WAREHOUSE_SIZE WS ON WS.WAREHOUSE_SIZE = upper(QH.WAREHOUSE_SIZE)
ORDER BY RELATIVE_PERFORMANCE_COST DESC
LIMIT 200;

==========================
ACTION YOU COULD TAKE:
--         This query gives you the chance to evaluate expensive queries and
--         take some action. For example, you could look at the query profile,
--         contact the user who executed the query, or take action to optimize
--         these queries.
--         Below is a list of the columns in this secure view,
--         SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY.
--         QUERY_HISTORY view columns

===================================
-- 21.3.2  Top 10 Queries With The Most Spillage to Remote Storage
--         Another way to evaluate the cost of queries is to see if they are
--         spilling to remote storage. The query below allows you do do that.


select query_id, substr(query_text, 1, 50) partial_query_text, user_name, warehouse_name, warehouse_size, 
       BYTES_SPILLED_TO_REMOTE_STORAGE, start_time, end_time, total_elapsed_time/1000 total_elapsed_time
from   snowflake.account_usage.query_history
where  BYTES_SPILLED_TO_REMOTE_STORAGE > 0
and start_time::date > dateadd('days', -45, current_date)
order  by BYTES_SPILLED_TO_REMOTE_STORAGE desc
limit 10;
