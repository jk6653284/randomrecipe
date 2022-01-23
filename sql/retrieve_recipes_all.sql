/*per source randomization*/
select *
from {TABLE_NAME}
order by random()
limit {RETRIEVE_NUM};