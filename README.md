# Dressing for the weather

### Business Case

Evergreens is a Seattle-based company which runs a series of restaurants that serves salads, predominantly at lunchtime. They suspected that adverse weather conditions acted as a deterrent to potential customers, and were looking for a modeling approach that would provide better guidance for potential changes in sales. Accordingly, information gain from the model output could aid in more efficient staffing.


### Data

Evergreens provided sales data for all their stores from January 2, 2017 through August, 2018. The data that is included in this report as been adjusted so to keep Evergreens sales data private.

Weather data is METAR (METeorological Aerodrome Reports), is a format for reporting weather information. A METAR weather report is predominantly used by pilots in fulfillment of a part of a pre-flight weather briefing, and by meteorologists, who use aggregated METAR information to assist in weather forecasting. Data from this site - https://mesonet.agron.iastate.edu/request/download.phtml?network=WA_ASOS - was pulled to be used for historic weather data. The following choices were used: 
  Network: Washington ASOS
  1) BFS (Seattle/Boeing Field)
  2) All Available data
  3) Specific Date Range: 1/1/18 through 8/13/18
  4) Timezone: America/Los Angeles (WST/WDT)
  5) Data Format: Comma delimited
  6) MADIS HFMETAR
  7) Download the data.


### Methodology

Sales data was used as the target for the data set, and temperature, sunny or not, precipitation or not were the weather features used from the METAR data. To account for the time of the year - a 60 degree sunny day in December means something different than a 60 degree sunny day in June - sine and cosine vectors based on the day of the year are included as features. Day of the week is included as features. Because this is a time series problem, 1, 2, 3, and 4 week rolling averages were the last features included.


### Modeling

Gradient Boosting, Random Forest, and Linear Regression were used to evaluate to create models, with MSE and MAE used to evaluate the models. Gradient Boosting showed the lowest error, and was used for the model.


### Notes 

The sales data included in this repo has been adjusted to maintain privacy. Expected columns for sales data before the feature engineering are: locationid', 'locationname', 'date', 'day_of_week', 'ordermodename', 'net_sales', 'guests', 'checks', 'entrees'.
