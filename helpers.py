import pandas as pd

# actual - 1d data frame
# predicted - 1d numpy array
# player - 1d data frame that matches the predictions to the player
def build_results_df(actual, predicted, player):
    results = pd.DataFrame({
        'Player': player,
        'Actual': actual.values,
        'Predicted': predicted
    }, index=actual.index)

    return results

# results - results df from build_results_df()
def compute_rank_squared_error(results):
    results['ActualRank'] = results['Actual'].rank(ascending=False, method='min').astype(int)
    results['PredictedRank'] = results['Predicted'].rank(ascending=False, method='min').astype(int)

    results['RankError'] = results['PredictedRank'] - results['ActualRank']

    rank_squared_error = (results['RankError'] ** 2).sum()

    return rank_squared_error