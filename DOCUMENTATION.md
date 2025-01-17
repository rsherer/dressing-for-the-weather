# Dressing for the Weather Documentation

### Source Code

Source code is located in the src folder.

#### Functions for sales data
The file sales_data_cleaning.py has functions to adjust sales data so that it can be combined with weather data to be used for modeling.

The sales file is expected to be a .csv or a .txt file with the following columns:<br/><br/>
        *'locationid'<br/>
        *'locationname'<br/>
        *'date'<br/>
        *'day_of_week'<br/>
        *'ordermodename'<br/>
        *'net_sales'<br/>
        *'guests'<br/>
        *'checks'<br/>
        *'entrees'

-clean_up_dateframe(df) will convert the file to a pandas dataframe that includes sales data for all stores.

-store_filter(df, store=1) will take a clean dataframe, and will filter to a dataframe for data for a single store. A list with the possible columns is listed in the doc string.

-get_instore_sales_data_by_type(df) will take a clean dataframe, and will organize into a dataframe by sales type categories. A list of possible sales types is included in the doc string.

-get_sales_data_by_day(df) will take a dataframe and combine all sales types into total revenue by day. It's suggested that store_filter() be used to convert the raw sales data before. Or executed get_sales_data_by_day(store_filter(clean_up_dataframe(df), store=1)) for store number 1 by day. Change store= for other stores.

#### Functions for weather data
There is only one function for weather data, which is get_date_and_weather_from_metar(filename). Executing this function will convert the weather data so that it is ready to be combined with sales data.

#### Functions to combine sales and weather data sets

There is one function that needs to be executed to combine the sales and weather data to be used for modeling. That function is combine_data(sales_df, weather_df). The other functions in the file are included in the combine_data function and aren't necessary to be called on their own.


