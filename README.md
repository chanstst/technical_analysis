# Stock scanner and multi-chart display for technical analysts

## Problem Statement
Every day technical analysts are required to perform two main tasks:
- scan hundreds and thousands of stocks
- take a closer look at the charts of selected stocks based on certain criteria.

The first step involves downloading relevant financial data (eg stock price, trading volume), then process and consolidate the data, ready to be used for further analysis (moving averages, trend lines, volume changes).

The pain point lies in the second step, where technical analysts often need to type in the stock code in some sort of terminals or applications, in order to see the detailed stock charts.
As there are potentially hundreds of charts to look at, it is time-consuming to key in all the stock codes one at a time, and this manual operation is not ideal for stock comparison.

## Sample of multi-chart display

<img src="images/chart1.png" alt="chart1">
Figure 1: Sample of stock charts on watch list


## Folder Organization

    |__ common/
    |   |__ my_functions_download_charts.ipynb
    |__ code/
    |   |__ download.ipynb
    |   |__ print_selected_stocks.ipynb
    |__ data/
    |   |__ selected_stocks.csv
    |   |__ adj.csv
    |   |__ low.csv	
    |   |__ adj.csv
    |   |__ low.csv
    |   |__ high.csv
    |   |__ open.csv
    |   |__ close.csv
    |   |__ volume.csv	
    |__ images/
    |   |__ chart1.png
    |   |__ chart2.png
    |   |__ chart3.png
    |   |__ chart4.png
