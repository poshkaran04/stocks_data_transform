select
    upper(stock_symbol) as stock_symbol,
    date,
    open,
    high,
    low,
    close,
    volume,
    last_import_date

from {{ source("us_stocks", "stocks_data_usa_partitioned") }}
