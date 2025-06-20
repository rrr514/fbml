import pandas as pd
from sklearn.metrics import root_mean_squared_error, r2_score, mean_absolute_error

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


def evaluate_model(y_train, train_preds, y_test, test_preds):
    """
    Evaluate a model's performance on training and test data.
    
    Parameters:
    - y_train: Actual training target values
    - train_preds: Predicted training values
    - y_test: Actual test target values  
    - test_preds: Predicted test values
    """

    print("Training RMSE:", root_mean_squared_error(y_train, train_preds))
    print("Training R^2:", r2_score(y_train, train_preds))
    print("Training MAE:", mean_absolute_error(y_train, train_preds))
    print("Testing RMSE:", root_mean_squared_error(y_test, test_preds))
    print("Testing R^2:", r2_score(y_test, test_preds))
    print("Testing MAE:", mean_absolute_error(y_test, test_preds))


def print_model_coefficients(model, features):
    print("Intercept:", model.intercept_)
    print("Feature Coefficients:")
    for feat, coef in zip(features, model.coef_):
        print(f"{feat}: {coef:.4f}")


def append_total_fantasy_points(df, season_df):
    df_merged = df.merge(
        season_df[['Player', 'FantasyPtsPPR']],
        on='Player',
        how='left'
    )
    df_merged['FantasyPtsPPR'] = df_merged['FantasyPtsPPR'].fillna(0)
    return df_merged