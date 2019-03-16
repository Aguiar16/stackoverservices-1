from data_module.visualization import data_visualization as dv


METRICS = ('AnswerCount','CommentCount','FavoriteCount','Score')
# METRICS = ('AnswerCount','ViewCount','CommentCount','FavoriteCount','Score')
# METRICS = ('ViewCount',)

input_data = 'data/mde/raw/questions_xtext.csv'
output_data = 'xtext_metrcis.svg'

dv.metrics_boxplot(input_data, METRICS)