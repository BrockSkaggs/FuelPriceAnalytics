# Fuel Price Analytics
Fluctuating gas prices is something that everyone observes with the usual goal of minimizing the cost of filling your tank.  A potential stumbling block being that multiple gas stations within the same area can have different prices.  Do some stations typically have a lower relative cost than others?

This project reviewed gas prices for local stations in Carthage, MO in an attempt to identify pricing behaviors.  Components of the project are described below.

**Data Extract, Transfer, & Load (ETL)**  
Pricing data was retrieved on a daily schedule from the [GasBuddy](https://www.gasbuddy.com/gasprices/missouri/carthage) website.  This was implemented using a Python script working with the Selenium web driver to automatically scrape data from the web page.  Resulting data was transformed and stored in a local CSV file.  This component of the project can be found within the WebScrape project folder.

**Data Presentation**  
An interactive web dashboard has been created for the consumption of the data using Plotly's Dash framework.  The dashboard contains time series charts, map locating stations, and cards to present metric associated with each station.  This part of the project is located within the Dashboard project folder.