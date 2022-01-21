with randomized as (
select
	{TABLE_NAME}.*
	,row_number() over (partition by website_name order by random()) rn
from {TABLE_NAME}
where lower(recipe_name) like '%{KEYWORD}%'
)
select *
from randomized
where rn = 1
order by random()
limit {RETRIEVE_NUM}
;