class utils():
    def __init__(self):
        pass 
        
    def get_sort_and_pick_top(self, df, by_column, ascending, number_of_top):
        sort_date = df.sort_values(by=by_column, ascending=ascending).head(number_of_top)
        return sort_date
    

    def get_mean(self,df,group_by_column,mean_by_column):
        mean = df.groupby(by=group_by_column)[mean_by_column].mean().round(2)
        return mean
    
    
    def get_calculation(self, df, group_by_column, agg_by): 
        calculation = df.groupby(by=group_by_column).agg({agg_by: ['sum', 'min', 'max', 'mean', 'count']})
        return calculation