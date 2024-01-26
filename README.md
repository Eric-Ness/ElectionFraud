# Election Fraud

To my knowledge, The Heritage Foundation has one of the best datasets regarding voter fraud in the United States. 

![Chart Image](chart/map.png)

## get_data.py

The following is code to scrape the data from the website, create a dataframe and save it to a csv file. 

Source: https://www.heritage.org/voterfraud

The fields extracted are:
- State
- Year
- Name
- Case Type
- Fraud Type
- Outcome
- Source

## analyze.ipynb

This notebook has a couple charts and maps for basic analysis. Feel free to customize for you own use.

## Blog Post

https://eric.ness.net/2024/01/26/election-fraud/

## Requirements

The following libraries are needed for this project:

- beautifulsoup4==4.12.3
- pandas==2.2
- requests==2.31.0
- matplotlib==3.8.2 
- geopandas==0.14.2 

```
pip install -r requirements.txt
```

## References

**Voter Fraud Data:** https://www.heritage.org/voterfraud

**State Boundary Shapefile:** https://www.sciencebase.gov/catalog/item/52c78623e4b060b9ebca5be5

**Voter Turnout Data:** https://www.electproject.org/election-data/voter-turnout-data