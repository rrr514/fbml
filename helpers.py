import pandas as pd

# actual - 1d data frame
# predicted - 1d numpy array
# player - 1d data frame that matches the predictions to the player
# display - T/F for displaying a preview of the results
def compute_rank_squared_error(actual, predicted, player, display):
    results = pd.DataFrame({
        'Player': player,
        'Actual': actual.values,
        'Predicted': predicted
    }, index=actual.index)

    results['ActualRank'] = results['Actual'].rank(ascending=False, method='min').astype(int)
    results['PredictedRank'] = results['Predicted'].rank(ascending=False, method='min').astype(int)

    results['RankError'] = results['PredictedRank'] - results['ActualRank']

    rank_squared_error = (results['RankError'] ** 2).sum()

    if display:
        print(results.to_string())

    return rank_squared_error