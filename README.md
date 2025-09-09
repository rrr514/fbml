# fbml
## How to use:
1. Scrape current/rookie player data by running scrape_data.ipynb and scrape_rookie_data.py, respectively. 
2. Process scraped current/rookie player data by running preprocess_data.py and preprocess_rookie_data.py, respectively.
3. (Optional) The models are already trained as specified in the respective .ipynb file. If retraining is desired, the years and attributes to use can be changed in the .ipynb file.
4. Create the projections list by running create_projections.ipynb

Benchmark Metrics:
- R² at least 0.3–0.5
- RMSE between 40-60
- MAE between 30-50

# TODO List/Future Ideas:
- Fix rookie qb model overfitting (Improve all rookie models in general lol)
- Eventually add more training data for all models
- Switch to a different type of model (e.g. RandomForest)
- Use more advanced stats in training (e.g. YAC, Y/Route Run, etc.)
