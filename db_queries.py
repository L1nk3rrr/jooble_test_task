from sqlalchemy import text

GET_DATA_BY_DOMAIN = text("""
SELECT strftime(:dtf, min(visit_date)) as first_visit_date,
       strftime(:dtf, max(visit_date)) as last_visit_date,
       count(id) as page_count,
       count(CASE status_code
             WHEN 200
                 THEN 1
             END
       ) as active_pages,
       group_concat(original_url, ',|,') as url_list
  FROM employees_visits
 WHERE domain_name = :name
 GROUP BY domain_name
""")

GET_DATA_BY_URL = text("""
SELECT strftime(:dtf, visit_date) as visit_date,
       final_url,
       status_code,
       title,
       domain_name,
       strftime(:dtf, created_date) as parsed_date
  FROM employees_visits
 WHERE original_url = :name
 -- get the last visited url by ordering + limit instead of using query inside query
 ORDER BY visit_date desc
 LIMIT 1
""")