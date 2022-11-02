import pandas as pd
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from base_nadzor.app import app
from base_nadzor.database import DB_CLASS
from base_nadzor.pdf_rsn_creator import pdf_razr_stroit
from base_nadzor.pages import RSN_new


class RSNLayoutClass:
    def __init__(self):
        self.DBClass = DB_CLASS.DBClass()
        self.PDFCreateObj = pdf_razr_stroit.CreatePdfClass()
        self.df_readed = pd.DataFrame()
        self.NewRSNPageClass = RSN_new.NewRsnFormClass()

    def get_df_rns(self):
        df = self.DBClass.read_rns_db()
        self.df_readed = df
        return df

    def make_rns_table(self, full_flag=False):
        style_data_conditional = [
            {
                "if": {"state": "active"},
                "backgroundColor": "rgba(150, 180, 225, 0.2)",
                "border": "1px solid blue",
            },
            {
                "if": {"state": "selected"},
                "backgroundColor": "rgba(0, 116, 217, .03)",
                "border": "1px solid blue",
            },
        ]

        if full_flag:
            df_for_table = self.get_df_rns()
        else:
            df_full_temp = self.get_df_rns()
            df_for_table = pd.DataFrame()

            df_for_table['Дата разрешения на строительство'] = df_full_temp['1.1']
            df_for_table['Номер разрешения на строительство'] = df_full_temp['1.2']
            df_for_table['Срок действия настоящего разрешения'] = df_full_temp['1.4']
            zastroishik_needs_columns = ['2.1.1', '2.1.2', '2.1.3', '2.2.1']
            df_for_table['Застройщик'] = ''
            df_full_temp.fillna(value='', inplace=True)
            for zastr_col in zastroishik_needs_columns:
                df_for_table['Застройщик'] = df_for_table['Застройщик'].astype(str) + ' ' + df_full_temp[
                    zastr_col].astype(str)
            df_for_table['Объект'] = df_full_temp['3.1']
            df_for_table['Адрес объекта'] = df_full_temp['3.3.6'] + ' ' + df_full_temp['3.3.7']
            df_for_table['Кадастровый номер ЗУ'] = df_full_temp['4.1']


        table = dash_table.DataTable(df_for_table.to_dict('records'),
                                     [{"name": i, "id": i} for i in df_for_table.columns],
                                     id='table_rns',
                                     style_data_conditional=style_data_conditional,
                                     style_table={
                                         'overflowY': 'scroll'
                                     },
                                     style_cell={
                                         'height': 'auto',
                                         # all three widths are needed
                                         'minWidth': '120px', 'width': '250px', 'maxWidth': '250px',
                                         'whiteSpace': 'normal'
                                     },
                                     fill_width=False,
                                     row_selectable='single',
                                     filter_action='native',
                                     filter_options={'case': 'insensitive'}
                                     )

        return table

    def make_layout_rns(self):

        layout_create = html.Div([
            html.H4('Разрешения на строительство', className="text-center", style={'margin': '10px'}),
            html.Div(
                children=[self.make_rns_table()],
                id='table_rns_div'
            )
            ,

            html.Div(children=[
                dbc.Button("Добавить", color="success", className="me-1", id='add_rsn_btn'),
                dbc.Button("Распечатать", color="success", className="me-1", id='print_rsn_btn'),
                dbc.Button("Изменить", color="success", className="me-1", id='edit_rsn_btn'),
                dbc.Button("Удалить", color="danger", className="me-1", id='delete_rsn_btn', style={'float': 'right'})
            ], style={'width': '100%', 'display': 'inline-block', 'margin': '20px'}),
            html.Div(id='rsn_list_null', children=[
                dcc.Download(id="download_rsn_pdf"),
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Внесите данные и нажмите сохранить")),
                        dbc.ModalBody(children=[
                            html.Div(id='rsn_list_null_new')
                        ])

                    ],
                    id="modal-xl_rsn",
                    size="xl",
                    is_open=False,
                ),
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Внесите данные и нажмите сохранить")),
                        dbc.ModalBody(children=[
                            html.Div(id='rsn_list_null_edit')
                        ])

                    ],
                    id="modal-xl_rsn_edit",
                    size="xl",
                    is_open=False,
                ),

            ]),
        ], className='container')

        return layout_create


RSNLayoutObj = RSNLayoutClass()
layout = RSNLayoutObj.make_layout_rns()
new_rsn_layout = RSNLayoutObj.NewRSNPageClass.make_new_rsn_layout()


# Выделение всей строки
@app.callback(
    Output("table_rns", "style_data_conditional"),
    [Input("table_rns", "active_cell")]
)
def update_selected_row_color(active):
    style = [
        {
            "if": {"state": "active"},
            "backgroundColor": "rgba(150, 180, 225, 0.2)",
            "border": "1px solid blue",
        },
        {
            "if": {"state": "selected"},
            "backgroundColor": "rgba(0, 116, 217, .03)",
            "border": "1px solid blue",
        },
    ]
    if active:
        style.append(
            {
                "if": {"row_index": active["row"]},
                "backgroundColor": "rgba(150, 180, 225, 0.2)",
                "border": "1px solid blue",
            }
        )
    return style


# Печать разрешения
@app.callback(
    Output('download_rsn_pdf', 'data'),
    Input('print_rsn_btn', 'n_clicks'),
    State('table_rns', 'derived_virtual_data'),
    State('table_rns', 'selected_rows'), prevent_initial_call=True, )
def print_pdf(clicks, rows, id_row):
    if clicks is None:
        return ''
    else:
        RSNLayoutObj.PDFCreateObj.input_data = RSNLayoutObj.df_readed.iloc[id_row[0]].to_dict()
        # PdfClass.input_data = rows[id_row[0]]
        filename_result = RSNLayoutObj.PDFCreateObj.make_razr_pdf()
        # PdfClass.input_data = rows[id_row[0]]
        return dcc.send_file(filename_result)


# Удаление записи с добавлением в архив
@app.callback(
    Output('table_rns_div', 'children'),
    Input('delete_rsn_btn', 'n_clicks'),
    State('table_rns', 'derived_virtual_data'),
    State('table_rns', 'selected_rows'), prevent_initial_call=True, )
def edit(clicks, rows, id_row):
    if clicks is None:
        return ''
    else:
        RSNLayoutObj.DBClass.del_rsn(rows[id_row[0]])
        return RSNLayoutObj.make_rns_table()


# Добавление новой записи
@app.callback(
    Output('rsn_list_null_new', 'children'), Output('modal-xl_rsn', 'is_open'),
    Input('add_rsn_btn', 'n_clicks'),
    prevent_initial_call=True, )
def new_rsn(clicks):
    if clicks is None:
        return '', False
    else:
        return RSNLayoutObj.NewRSNPageClass.make_new_rsn_layout(), True
