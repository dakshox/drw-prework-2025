import pandas as pd


def find_tips_nominal_pairs(
    df: pd.DataFrame,
    tip_types: list[int]     = [11, 12],
    nominal_types: list[int] = [1, 2],
    min_years: float         = 5.0,
    caldt_col: str           = 'caldt',
    id_col: str              = 'itype',
    mat_col: str             = 'tmatdt',
    idnum_col: str           = 'kytreasno',
    issue_date_col: str      = 'tdatdt'
) -> pd.DataFrame:
    df = df.copy()
    df[caldt_col]       = pd.to_datetime(df[caldt_col])
    df['maturity_date'] = pd.to_datetime(df[mat_col])
    df[issue_date_col]  = pd.to_datetime(df[issue_date_col])
    df['years_to_mat']  = (df['maturity_date'] - df[caldt_col]).dt.days / 365.25
    df = df[df['years_to_mat'] >= min_years]
    df_tips = df[df[id_col].isin(tip_types)].copy()
    df_nom  = df[df[id_col].isin(nominal_types)].copy()
    prefer_map = {11: 1, 12: 2}
    pairs = []
    for _, tip in df_tips.iterrows():
        cands = df_nom[(df_nom[caldt_col] == tip[caldt_col]) &
                       (df_nom['maturity_date'] == tip['maturity_date'])].copy()
        if cands.empty:
            continue
        pref = prefer_map.get(tip[id_col])
        if pref is not None:
            cands_pref = cands[cands[id_col] == pref]
            if not cands_pref.empty:
                cands = cands_pref
        if len(cands) > 1:
            cands['date_diff'] = (cands[issue_date_col] - tip[issue_date_col]).abs()
            best = cands.loc[cands['date_diff'].idxmin()]
        else:
            best = cands.iloc[0]
        nom_str  = str(int(best[idnum_col]))
        tips_str = str(int(tip[idnum_col]))
        pairs.append({
            'maturity_date': tip['maturity_date'],
            f'{idnum_col} nominal': nom_str,
            f'{idnum_col} tips':   tips_str,
        })
    result = (pd.DataFrame(pairs)
              .drop_duplicates(subset=['maturity_date',
                                        f'{idnum_col} nominal',
                                        f'{idnum_col} tips'])
              .set_index('maturity_date')
              .sort_index())
    return result

