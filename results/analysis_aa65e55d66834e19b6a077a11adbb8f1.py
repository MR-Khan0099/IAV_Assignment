def perform_analysis(df):
    engine_speed_stats = df['Eng_nEng10ms'].describe()[['min', 'max', 'mean']].to_dict()
    return engine_speed_stats