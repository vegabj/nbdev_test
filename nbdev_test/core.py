# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/00_core.ipynb (unless otherwise specified).

__all__ = ['Query', 'Results']

# Cell
class Query:
    def __init__(self, cluster: str="<cluster_name>", db: str="<db_name>", use_secrets: bool=False):
        if use_secrets:
            self.kcsb = KustoConnectionstringBuilder.with_
        else:
            self.kcsb = KustoConnectionStringBuilder.with_interactive_login(cluster)
        self.db = db
        self.client = KustoClient(self.kcsb)
    def __repr__(self):
        return self.kcsb
    def query(self, query_string: str):
        return Results(self.client.execute(self.db, query_string))

# Cell
class Results:
    def __init__(self, response_dataset):
        self.response_dataset = response_dataset
    def __repr__(self):
        if self.response_dataset.errors_count > 0:
            print(f"Request got {self.response_dataset.errors_count} errors")
            print(self.response_dataset.get_exceptions())
        dfs = [dataframe_from_result_table(res) for res in self.response_dataset.primary_results]
        for df in dfs:
            print(df)
        return ""
    def get_results(self):
        if len(self.response_dataset.primary_results) == 1:
            return dataframe_from_result_table(self.response_dataset.primary_results[0])
        return [dataframe_from_result_table(res) for res in self.response_dataset.primary_results]