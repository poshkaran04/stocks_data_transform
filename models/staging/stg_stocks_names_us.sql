select symbol, name, sector, industry

from {{ source("dbt_staging", "us_stock_names") }}
where sector is not null and industry is not null
