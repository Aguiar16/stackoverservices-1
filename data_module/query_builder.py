

class QueryBuilder(object):

    @staticmethod
    def build(query_details):

        if "columns" in query_details.keys():
            num_columns = len(query_details["columns"])
            select_stmt = 'SELECT ' + ", ".join(num_columns * ['{}'])
            columns = query_details["columns"]
        else:
            select_stmt = 'SELECT *'
            columns = []

        from_stmt = "FROM `sotorrent-org.2018_09_23.Posts`"

        if "filters" in query_details.keys():
            filters = "WHERE"

            for query_filter in query_details["filters"]:
                if "conector" in query_filter.keys():
                    conector = query_filter["conector"]
                else:
                    conector = ""

                column = query_filter["column"]
                operator = query_filter["operator"]

                if operator == "IN":
                    num_values = len(query_filter["value"])
                    value = "(" + ", ".join(num_values * ['{}']) + ")"
                else:
                    value = "'{}'"

                if len(conector) == 0:
                    new_filter = " ".join([column, operator, value])
                else:
                    new_filter = " ".join([conector, column, operator, value])
                filters = filters + " " + new_filter

            filters = filters + " AND AnswerCount >= 1"
            values = [item for qf in query_details["filters"]
                      for item in qf["values"]]
        else:
            filters = "WHERE AnswerCount >= 1"
            values = []

        query_inpt = columns + values

        print("QUERY SUCCESSFULLY BUILD")

        complete_query = " ".join(
            [select_stmt, from_stmt, filters]).format(*query_inpt)
        
        print(complete_query)

        return complete_query
