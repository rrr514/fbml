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


def print_diagnostics(X_train, X_test, features, y_train, y_test):
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    print(f"Features: {len(features)}")
    print(f"Samples per feature: {len(X_train) / len(features):.1f}")
    print(f"Training target stats: mean={y_train.mean():.1f}, std={y_train.std():.1f}")
    print(f"Testing target stats: mean={y_test.mean():.1f}, std={y_test.std():.1f}")


def compute_qb_features(df):
    # Compute the features needed
    df['PassAttPerGame'] = df['PassAtt'] / df['GamesPlayed'].replace(0, pd.NA)
    df['PassAttPerGame'] = df['PassAttPerGame'].fillna(0)

    df['PassYdsPerGame'] = df['PassYds'] / df['GamesPlayed'].replace(0, pd.NA)
    df['PassYdsPerGame'] = df['PassYdsPerGame'].fillna(0)

    df['PassTDsPerGame'] = df['PassTD'] / df['GamesPlayed'].replace(0, pd.NA)
    df['PassTDsPerGame'] = df['PassTDsPerGame'].fillna(0)

    df['PassIntPerGame'] = df['PassInt'] / df['GamesPlayed'].replace(0, pd.NA)
    df['PassIntPerGame'] = df['PassIntPerGame'].fillna(0)

    df['RushYdsPerGame'] = df['RushYds'] / df['GamesPlayed'].replace(0, pd.NA)
    df['RushYdsPerGame'] = df['RushYdsPerGame'].fillna(0)

    df['RushTDsPerGame'] = df['RushTD'] / df['GamesPlayed'].replace(0, pd.NA)
    df['RushTDsPerGame'] = df['RushTDsPerGame'].fillna(0)


def compute_rb_fb_features(df):
    df['RushAttPerGame'] = df['RushAtt'] / df['GamesPlayed'].replace(0, pd.NA)
    df['RushAttPerGame'] = df['RushAttPerGame'].fillna(0)

    df['RushYdsPerGame'] = df['RushYds'] / df['GamesPlayed'].replace(0, pd.NA)
    df['RushYdsPerGame'] = df['RushYdsPerGame'].fillna(0)

    df['RushTDsPerGame'] = df['RushTD'] / df['GamesPlayed'].replace(0, pd.NA)
    df['RushTDsPerGame'] = df['RushTDsPerGame'].fillna(0)

    df['TargetsPerGame'] = df['Targets'] / df['GamesPlayed'].replace(0, pd.NA)
    df['TargetsPerGame'] = df['TargetsPerGame'].fillna(0)

    df['RecsPerGame'] = df['Receptions'] / df['GamesPlayed'].replace(0, pd.NA)
    df['RecsPerGame'] = df['RecsPerGame'].fillna(0)

    df['RecYdsPerGame'] = df['RecYds'] / df['GamesPlayed'].replace(0, pd.NA)
    df['RecYdsPerGame'] = df['RecYdsPerGame'].fillna(0)

    df['RecTDsPerGame'] = df['RecTD'] / df['GamesPlayed'].replace(0, pd.NA)
    df['RecTDsPerGame'] = df['RecTDsPerGame'].fillna(0)


def compute_te_features(df):
    df['TargetsPerGame'] = df['Targets'] / df['GamesPlayed'].replace(0, pd.NA)
    df['TargetsPerGame'] = df['TargetsPerGame'].fillna(0)

    df['RecsPerGame'] = df['Receptions'] / df['GamesPlayed'].replace(0, pd.NA)
    df['RecsPerGame'] = df['RecsPerGame'].fillna(0)

    df['RecYdsPerGame'] = df['RecYds'] / df['GamesPlayed'].replace(0, pd.NA)
    df['RecYdsPerGame'] = df['RecYdsPerGame'].fillna(0)

    df['RecTDsPerGame'] = df['RecTD'] / df['GamesPlayed'].replace(0, pd.NA)
    df['RecTDsPerGame'] = df['RecTDsPerGame'].fillna(0)


def compute_wr_features(df):
    df['TargetsPerGame'] = df['Targets'] / df['GamesPlayed'].replace(0, pd.NA)
    df['TargetsPerGame'] = pd.to_numeric(df['TargetsPerGame'], errors='coerce').fillna(0)

    df['RecsPerGame'] = df['Receptions'] / df['GamesPlayed'].replace(0, pd.NA)
    df['RecsPerGame'] = pd.to_numeric(df['RecsPerGame'], errors='coerce').fillna(0)

    df['RecYdsPerGame'] = df['RecYds'] / df['GamesPlayed'].replace(0, pd.NA)
    df['RecYdsPerGame'] = pd.to_numeric(df['RecYdsPerGame'], errors='coerce').fillna(0)

    df['RecTDsPerGame'] = df['RecTD'] / df['GamesPlayed'].replace(0, pd.NA)
    df['RecTDsPerGame'] = pd.to_numeric(df['RecTDsPerGame'], errors='coerce').fillna(0)


def compute_rookie_qb_features(df):
    df['GamesPlayed'] = df['Coll_games'].fillna(0)

    df['CompletionPct'] = df['Coll_pass_cmp_pct'].fillna(0)
    
    df['PassAttPerGame'] = df['Coll_pass_att'] / df['Coll_games'].replace(0, pd.NA)
    df['PassAttPerGame'] = df['PassAttPerGame'].fillna(0)

    df['PassYdsPerGame'] = df['Coll_pass_yds_per_g'].fillna(0)

    df['PassTDsPerGame'] = df['Coll_pass_td'] / df['Coll_games'].replace(0, pd.NA)
    df['PassTDsPerGame'] = df['PassTDsPerGame'].fillna(0)

    df['PassIntPerGame'] = df['Coll_pass_int'] / df['Coll_games'].replace(0, pd.NA)
    df['PassIntPerGame'] = df['PassIntPerGame'].fillna(0)

    df['RushYdsPerGame'] = df['Coll_rush_yds_per_g'].fillna(0)

    df['RushTDsPerGame'] = df['Coll_rush_td'] / df['Coll_games'].replace(0, pd.NA)
    df['RushTDsPerGame'] = df['RushTDsPerGame'].fillna(0)


def compute_rookie_rb_fb_features(df):
    df['GamesPlayed'] = df['Coll_games'].fillna(0)

    df['RushAttPerGame'] = df['Coll_rush_att'] / df['Coll_games'].replace(0, pd.NA)
    df['RushAttPerGame'] = df['RushAttPerGame'].fillna(0)

    df['RushYdsPerGame'] = df['Coll_rush_yds_per_g'].fillna(0)

    df['RushTDsPerGame'] = df['Coll_rush_td'] / df['Coll_games'].replace(0, pd.NA)
    df['RushTDsPerGame'] = df['RushTDsPerGame'].fillna(0)

    df['RecsPerGame'] = df['Coll_rec'] / df['Coll_games'].replace(0, pd.NA)
    df['RecsPerGame'] = df['RecsPerGame'].fillna(0)

    df['RecYdsPerGame'] = df['Coll_rec_yds_per_g'].fillna(0)

    df['RecTDsPerGame'] = df['Coll_rec_td'] / df['Coll_games'].replace(0, pd.NA)
    df['RecTDsPerGame'] = df['RecTDsPerGame'].fillna(0)


def compute_rookie_te_features(df):
    df['GamesPlayed'] = df['Coll_games'].fillna(0)

    df['RecsPerGame'] = df['Coll_rec'] / df['Coll_games'].replace(0, pd.NA)
    df['RecsPerGame'] = df['RecsPerGame'].fillna(0)

    df['RecYdsPerGame'] = df['Coll_rec_yds_per_g'].fillna(0)

    df['RecTDsPerGame'] = df['Coll_rec_td'] / df['Coll_games'].replace(0, pd.NA)
    df['RecTDsPerGame'] = df['RecTDsPerGame'].fillna(0)


def compute_rookie_wr_features(df):
    df['GamesPlayed'] = df['Coll_games'].fillna(0)

    df['RecsPerGame'] = df['Coll_rec'] / df['Coll_games'].replace(0, pd.NA)
    df['RecsPerGame'] = df['RecsPerGame'].fillna(0)

    df['RecYdsPerGame'] = df['Coll_rec_yds_per_g'].fillna(0)

    df['RecTDsPerGame'] = df['Coll_rec_td'] / df['Coll_games'].replace(0, pd.NA)
    df['RecTDsPerGame'] = df['RecTDsPerGame'].fillna(0)