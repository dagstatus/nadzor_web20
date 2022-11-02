import pandas as pd
import datetime
import uuid
import sqlalchemy


class DBClass:
    def __init__(self):
        self.result = None
        # self.con = sqlite3.connect('base_nadzor/read_db/NADZO_DB.db')
        self.engine = sqlalchemy.create_engine('sqlite:///base_nadzor/database/NADZO_DB.db')

    def read_rns_db(self):
        df = pd.read_sql('select * from RSN order by "1.2"', con=self.engine)

        return df

    def del_rsn(self, dict_delete_row: dict):
        # Переносим запись в архив
        new_df = pd.DataFrame({key: [value] for key, value in dict_delete_row.items()})
        try:
            new_df.to_sql('RSN_ARHIVE', con=self.engine, if_exists='append', index=False)
        except:
            df = pd.read_sql_query('select * from RSN_ARHIVE', con=self.engine)
            df_2 = pd.concat([df, new_df])
            df_2.to_sql(name='RSN_ARHIVE', con=self.engine, if_exists='replace', index=False)


        uid = dict_delete_row.get('uid', None)
        if uid:
            # print(uid)

            sql_query = f"""DELETE FROM RSN WHERE uid = '{uid}'"""
            conn = self.engine.connect(close_with_result=True)
            result = conn.execute(sql_query)
            result.close()
