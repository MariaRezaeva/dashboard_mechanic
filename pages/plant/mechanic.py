from dash import html, dcc, Output, Input, dash_table, callback, State
import sqlite3
import pandas as pd
import datetime
from aux_scripts.choose_dropdown import define_dropdown_list
import plotly.graph_objs as go

#Initiliaze a zero variables for initial load
ktg = 0
kio = 0
planned = 0
unplanned = 0
fault = 0
current_date = datetime.datetime.now().date()
last_week = current_date - datetime.timedelta(days=7)
#Open a csv file with info about equipment
choice_of_dropdown = pd.read_csv('C:/Users/rodion.semendyayev/PycharmProjects/Dash_plotly/create_eq/area_type_model.csv', encoding='cp1251', sep=";", header=None)
choice_of_dropdown.columns = ['area','type_eq', 'detail']
detail_output = pd.read_csv('C:/Users/rodion.semendyayev/PycharmProjects/Dash_plotly/create_eq/details.csv', encoding='cp1251',sep=";", header=None)
detail_output.columns = ['detail', 'mech_part']

#Template for visualization
mechanic_layout = html.Div([
    html.Div(html.H1('Служба главного механика'), style={'margin-top':'60px'}),
    html.Div([
        html.Div([
            dcc.Dropdown(choice_of_dropdown.iloc[:, 0].unique(), id='choice_area',
                         placeholder="Выберите участок", clearable=True),
        ], className='choice'),
        html.Div([
            dcc.Dropdown(choice_of_dropdown.iloc[:, 1].unique(), id='choice_type_eq',
                         placeholder="Тип оборудования", clearable=True),
        ], className='choice'),
        html.Div([
            dcc.Dropdown(choice_of_dropdown.iloc[:, 2], id='choice_eq',
                         placeholder="Выберите оборудование", clearable=True),
        ], className='choice'),
        html.Div([
            dcc.DatePickerRange(id="date-range",
                                start_date_placeholder_text='Начало',
                                end_date_placeholder_text='Конец',
                                display_format='DD/MM/YYYY',
                                start_date = last_week ,
                                end_date = current_date,
                                )
        ], className='choice', style={"width":'28%'}),

    ], className='eq_date'),

    html.Div([
        html.Div(dcc.Graph(id='plot_ktg', figure={'layout': go.Layout()}
                           ), className='table_info', style={'float':'left', 'width': '49%', 'overflow-y':'auto', 'height':'340px'}),

        html.Div(dcc.Graph(id='plot_repair', figure={'layout': go.Layout()}
                           ),className='table_info', style={'float':'left', 'width': '49%', 'margin-left': '2%', 'overflow-y':'auto', 'height':'340px'}),

    ], className='table_info_for_two'),

    # html.Div([
    #     dcc.Graph(id='plot_detail', style={'width': '48%', 'margin-left': '1%', 'float':'left', 'height': '340px'},
    #               figure={'layout': go.Layout()}),
    #
    #     dcc.Graph(id='plot_detail', style={'width': '48%', 'margin-left': '1%', 'height':'340px', 'float':'left'}, figure={
    #                 'layout': go.Layout(title='Количество ремонтов',)}),
    #
    # ], className='table_info', style={'overflow-y':'auto'}),

# html.Div([
#         html.Div([
#             #html.Div('Коэффициент технической готовности оборудования', className='name_of_block'),
#             html.Div([
#                 dcc.Graph(id='plot_ktg', style={'width': '98%', 'margin-left': '1%'},
#                           figure={'layout': go.Layout()}
#                           ),
#             ], style={'overflow-y':'auto','height':'340px'}),
#
#         ], className='table_info', style={'float': 'left', 'width': '49%',  'height':'340px'}),
#
#         html.Div(dcc.Graph(id='plot_detail', style={'width': '98%', 'margin-left': '1%', 'height': '340px'}, figure={
#             'layout': go.Layout(
#                 title='Количество запачастей',
#             )
#         }), className='table_info', style={'float': 'left', 'width': '49%', 'margin-left': '2%', 'height': '340px'}),
#
#     ], className='table_info_for_two', style={'overflow-y':'auto', 'height': '340px'}),

    html.Div([
        html.Div([
            html.Div("КТГ", className='span_name'),
            html.Div(f"{ktg} %", className='span_value', id = 'ktg'),
        ], className='range_info'),
        #'background': 'linear-gradient(blue, pink)'
        html.Div([
            html.Div("КИО", className='span_name'),
            html.Div(f"{kio} %", className='span_value'),
            ], className='range_info', style={'margin-left':'2%'}),
        html.Div([
            html.Div("Плановый ремонт", className='span_name'),
            html.Div(f"{planned}", className='span_value', id='planned'),
        ], className='range_info', style={'margin-left':'2%'}),
        html.Div([
            html.Div("Внеплановый ремонт", className='span_name'),
            html.Div(f"{unplanned}", className='span_value', id='unplanned'),
            ], className='range_info', style={'margin-left':'2%'}),
        html.Div([
            html.Div("Аварийный ремонт", className='span_name'),
            html.Div(f"{fault}", className='span_value', id='fault'),
        ], className='range_info', style={'margin-left':'2%'}),
    ], className='info_about_all'),
    #Gradient color 'background': 'linear-gradient(to right, #0ac282, #0df3a3)'

    html.Div([
        html.Div('Количество ремонтов за выбраный период времени', className='name_of_block'),
        dash_table.DataTable(
            id='table_sum',
            columns=[
                {"name": ["", "Деталь или узел"], "id": "detail"},
                {"name": ["Предупредительно плановый ремонт", "Количество"], "id": "ppr_amount"},
                {"name": ["Предупредительно плановый ремонт", "Длительность, ч"], "id": "ppr_duration"},
                {"name": ["Внеплановый ремонт", "Количество"], "id": "vne_amount"},
                {"name": ["Внеплановый ремонт", "Длительность, ч"], "id": "vne_duration"},
                {"name": ["Аварийный ремонт", "Количество"], "id": "fault_amount"},
                {"name": ["Аварийный ремонт", "Длительность, ч"], "id": "fault_duration"},
                {"name": ["Суммарный показатель", "Количество"], "id": "sum_amount"},
                {"name": ["Суммарный показатель", "Длительность, ч"], "id": "sum_duration"},
            ],
            merge_duplicate_headers=True,
            style_table={
                'overflowX': 'auto',
                "width": "100%",
                "borderBottomLeftRadius": "0.625rem",
                "borderBottomRightRadius": "0.625rem",
            },
            style_header={"text-align": "center", "background": '#f8f9fa', 'color': '#5a6169',
                          'font-family': 'var(--bs-body-font-family)'},
            style_data={"text-align": "center"},
            sort_action='native',
            sort_mode='single',
        ),
    ], className="table_info", style={'margin-left': "0px"}),

    html.Div(html.H3('Деталировка по ремонтам'), style={'margin-top': '20px'}),
    html.Div([
        # html.Div('Последние ремонты', className='name_of_block'),
        # dash_table.DataTable(
        # id='table_repair',
        # columns=[
        #     {"name": ["", "Деталь или узел"], "id": "detail"},
        #     {"name": ["Последний ремонт за выбранный период", "Наименование работ"], "id": "works_date_range"},
        #     {"name": ["Последний ремонт за выбранный период", "Дата"], "id": "data_date_range"},
        #     {"name": ["Последний ремонт за выбранный период", "Количество деталей"], "id": "amount_date_range"},
        #     {"name": ["Последний ремонт за все время", "Наименование работ"], "id": "works_all"},
        #     {"name": ["Последний ремонт за все время", "Дата"], "id": "data_all"},
        #     {"name": ["Последний ремонт за все время", "Количество деталей"], "id": "amount_all"},
        # ],
        # merge_duplicate_headers=True,
        # style_table={
        #     'overflowX': 'auto',
        #     "width": "100%",
        #     "borderBottomLeftRadius": "0.625rem",
        #     "borderBottomRightRadius": "0.625rem",
        #     },
        # style_header={"text-align": "center", "background": '#f8f9fa', 'color': '#5a6169',
        #               'font-family': 'var(--bs-body-font-family)'},
        # style_data={"text-align": "center"},
        # sort_action = 'native',
        # sort_mode = 'single',
        # )
    ], style={'margin-left': "0px"}, id = 'div_container'),



    html.Div([
        html.Div('Экономическая эффективность', className='name_of_block'),
        dash_table.DataTable(
            id='table_econimic',
            columns=[
                {"name": ["Деталь или узел", " "], "id": "detail"},
                {"name": ["Бренд", " "], "id": "brand"},
                {"name": ["Количество использованных\nдетателeй за последний ремонт", " "], "id": "detail_last_repair"},
                {"name": ["Стоимость", "Цена"], "id": "cost_one"},
                {"name": ["Стоимость", "Сумма"], "id": "cost_all"},
                {"name": ["Переработка руды", " "], "id": "ore_processing"},
                {"name": ["Себестоимость", " "], "id": "cost_price"},
            ],
            merge_duplicate_headers=True,
            style_table={
                'overflowX': 'auto',
                "width": "100%",
                "borderBottomLeftRadius": "0.625rem",
                "borderBottomRightRadius": "0.625rem",
            },
            style_header={"text-align": "center", "background": '#f8f9fa', 'color': '#5a6169',
                          'font-family': 'var(--bs-body-font-family)', 'whiteSpace': 'pre-wrap'},
            style_data={"text-align": "center", },
            sort_action='native',
            sort_mode='single',

        ),
    ], className="table_info", style={'margin-left': "0px"}),


    html.Div([
        html.Div('Запас оборудования на складах, заявки', className='name_of_block'),
        dash_table.DataTable(
            id='table_reserve',
            columns=[
                {"name": ["", "Деталь или узел"], "id": "detail"},
                {"name": ["Наличие на промплощадке", "Количество"], "id": "industrial_place"},
                {"name": ["Наличие на промплощадке", "Един.изм"], "id": "reserve_prom_area_um"},
                {"name": ["Наличие на складе", "Количество"], "id": "reserve_area"},
                {"name": ["Наличие на складе", "Един.изм"], "id": "reserve_area_um"},
                {"name": ["Заявка на приобретение", "Номер заявки"], "id": "request"},
                {"name": ["Заявка на приобретение", "Дата заявки"], "id": "date_request"},
                {"name": ["", "Запланированная дата следующего ремонта"], "id": "date"},
            ],
            merge_duplicate_headers=True,
            style_table={
                'overflowX': 'auto',
                "width": "100%",
                "borderBottomLeftRadius": "0.625rem",
                "borderBottomRightRadius": "0.625rem",

            },
            style_header={"text-align": "center", "background": '#f8f9fa', 'color': '#5a6169',
                          'font-family': 'var(--bs-body-font-family)'},
            style_data={"text-align": "center"},
            sort_action='native',
            sort_mode='single',
        ),
    ], className="table_info", style={'margin-left': "0px", 'margin-bottom':'20px'}),

], className="mechanic")

def get_df_table_repair(df_little, df, df_details):
    #not a beutiful need a refactor for optimization
    df_little_group = df_little.groupby(['detail'])
    df_group = df.groupby(['detail'])
    uniques_value = df['detail'].unique()
    df_table_repair = pd.DataFrame(columns=['detail', 'works_date_range', 'data_date_range', 'amount_date_range',
                                            'works_all', 'data_all', 'amount_all'])

    df_table_sum = pd.DataFrame(columns=['detail', 'ppr_amount', 'ppr_duration', 'vne_amount',
                                      'vne_duration', 'fault_amount', 'fault_duration',
                                      'sum_amount', 'sum_duration'])

    df_sum = df_little.groupby(['detail', 'type_of_repair'])[['amount', 'repair_time']].sum()
    type_of_repair_ = ['Плановый', 'Внеплановый', 'Аварийный']
    for detail in uniques_value:
        try:
            works_date_range = df_little_group.get_group(detail).iloc[-1]['comment_1']
            data_date_range = df_little_group.get_group(detail).iloc[-1]['date'].date()
            amount_date_range = df_little_group.get_group(detail).iloc[-1]['amount']
        except:
            works_date_range = '-'
            data_date_range = '-'
            amount_date_range = '-'
        works_all = df_group.get_group(detail).iloc[-1]['comment_1']
        data_all = df_group.get_group(detail).iloc[-1]['date']
        amount_all = df_group.get_group(detail).iloc[-1]['amount']
        df_table_repair = df_table_repair._append(
            {'detail': detail, 'works_date_range': works_date_range, 'data_date_range': data_date_range,
             'amount_date_range': amount_date_range, 'works_all': works_all,
             'data_all': data_all.date(), 'amount_all': amount_all}, ignore_index=True)

        cratch = []
        for item in type_of_repair_:
            try:
                repair = list(df_sum.loc[detail, item])
            except:
                repair = [0, 0]
            cratch.append(repair)
        ppr_amount = cratch[0][0]
        ppr_duration = cratch[0][1]
        vne_amount = cratch[1][0]
        vne_duration = cratch[1][1]
        fault_amount = cratch[2][0]
        fault_duration = cratch[2][1]
        sum_amount = ppr_amount + vne_amount + fault_amount
        sum_duration = ppr_duration + vne_duration + fault_duration
        df_table_sum = df_table_sum._append({'detail': detail, 'ppr_amount': ppr_amount, 'ppr_duration': ppr_duration,
                                       'vne_amount': vne_amount, 'vne_duration': vne_duration,
                                       'fault_amount': fault_amount, 'fault_duration': fault_duration,
                                       'sum_amount': sum_amount, 'sum_duration': sum_duration,
                                       }, ignore_index=True)
    planned = df_little.query("type_of_repair == 'Плановый'")['type_of_repair'].count()
    unplanned = df_little.query("type_of_repair == 'Внеплановый'")['type_of_repair'].count()
    fault = df_little.query("type_of_repair == 'Аварийный'")['type_of_repair'].count()
    #Merge two table in one
    df_table_repair = df_table_repair.merge(df_details['detail'], on='detail', how='right').fillna('-')
    df_table_sum = df_table_sum.merge(df_details['detail'], on='detail', how='right').fillna('-')
    repair_time_sum = df_table_sum['sum_duration'].apply(lambda x: x if x != "-" else 0).sum()
    return df_table_repair.to_dict('records'), df_table_sum.to_dict('records'), planned, unplanned, fault, repair_time_sum

def search_info(df, name, what_return):
    mask = df['type_of_repair'] == name
    if len(df[mask]) == 0:
        return 0
    else:
        return df[mask][what_return].iloc[0]

def get_df_table_repair_area_type_eq(df, choice_area_eq, type_area_eq, one_or_two_type = 1):
    pd.set_option('display.expand_frame_repr', False)
    if one_or_two_type == 1:
        df_little = df.query(f"{choice_area_eq} == '{type_area_eq}'")
    else:
        df_little = df.query(f"area == '{choice_area_eq}' & type_eq == '{type_area_eq}' ")
    agg_functions = {
        'repair_time': 'sum',
        'type_of_repair': 'count'
    }
    df_little = df_little.groupby(['equipment', 'type_of_repair']).agg(agg_functions)
    df_little.rename(columns = {'type_of_repair':'type_of_repair_count'}, inplace = True)
    df_little.reset_index(inplace=True)
    df_table_sum = pd.DataFrame(columns=['detail', 'ppr_amount', 'ppr_duration', 'vne_amount',
                                      'vne_duration', 'fault_amount', 'fault_duration',
                                      'sum_amount', 'sum_duration'])
    for item in df_little['equipment'].unique():
        mask = df_little['equipment'] == item
        df_table_sum = df_table_sum._append({'detail': item, 'ppr_amount': search_info(df_little[mask], 'Плановый', 'type_of_repair_count'),
                             'ppr_duration': search_info(df_little[mask], 'Плановый', 'repair_time'),
                             'vne_amount': search_info(df_little[mask], 'Внеплановый', 'type_of_repair_count'),
                             'vne_duration': search_info(df_little[mask], 'Внеплановый', 'repair_time'),
                             'fault_amount': search_info(df_little[mask], 'Аварийный', 'type_of_repair_count'),
                             'fault_duration': search_info(df_little[mask], 'Аварийный', 'repair_time'),
                             'sum_amount': df_little[mask].groupby('equipment')['type_of_repair_count'].sum().iloc[0],
                             'sum_duration': df_little[mask].groupby('equipment')['repair_time'].sum().iloc[0],
                            }, ignore_index=True)

    return df_table_sum.to_dict('records')

def get_db_warehouse_brand(name_db, eq):
    con = sqlite3.connect(f'C:/Users/rodion.semendyayev/PycharmProjects/Dash_plotly/Data_bases/{name_db}.db')
    query = f'SELECT * FROM {name_db} WHERE equipment = ?'
    df = pd.read_sql(query, con, params=[eq])
    con.close()
    return df

def get_table_economic(eq, start_date, end_date, df_eq):
    df = get_db_warehouse_brand('brand_cost', eq)
    df_clean = df.query('date != "ДД.ММ.ГГГГ"').copy()
    df_clean['date'] = pd.to_datetime(df_clean['date'], format='%d.%m.%Y')
    df_clean.set_index(df_clean['date'], inplace=True)
    df_clean.sort_index(inplace=True)
    df_clean.drop(['id','date', 'equipment', 'time'], inplace=True, axis=1)
    bins = df_clean.index.unique()
    if len(bins) != 0:
        a = bins[-1] + pd.Timedelta(days=1)
        df_clean['bins'] = pd.cut(df_clean.index, bins=bins.append(pd.DatetimeIndex([a])), right=False)
        df_eq_groupby = df_eq.loc[start_date:end_date].groupby([df_eq.loc[start_date:end_date].index, 'detail']).sum()
        cost, brand = [], []
        for variable_index, variable_detail in zip(df_eq_groupby.index.get_level_values(0), df_eq_groupby.index.get_level_values(1)):
            mask_0 = df_clean['bins'].apply(lambda x: True if variable_index in x else False)
            mask =  (df_clean['detail'] == variable_detail) & mask_0.astype('bool')
            if len(df_clean[mask]['cost'] != 0):
                cost.append(df_clean[mask]['cost'][0])
                brand.append(df_clean[mask]['brand'][0])
        df_eq_groupby['cost_one'] = cost
        df_eq_groupby['brand'] = brand
        df_eq_groupby['cost_all'] = df_eq_groupby['cost_one']*df_eq_groupby['amount']
        #CRANCH
        df_eq_groupby['ore_processing'] = df_eq_groupby['cost_one']*86541
        df_eq_groupby['cost_price'] = df_eq_groupby['cost_all'] / df_eq_groupby['ore_processing']
        df_eq_groupby.reset_index(inplace=True)
        df_eq_groupby.drop('date', axis = 1, inplace= True)
        df_eq_groupby.rename(columns = {'amount':'detail_last_repair'}, inplace= True)
        if df_eq_groupby.empty:
            return global_table_economic
        else:
            return df_eq_groupby.to_dict('records')
    else:
        return global_table_economic

def get_table_reverse(eq):
    df = get_db_warehouse_brand('warehouse', eq)
    table = df[df['time'] == df['time'].max()][['detail', 'industrial_place','date']]
    #CRANCH
    new_col = ['reserve_prom_area_um', 'reserve_area', 'reserve_area_um',
               'request', 'date_request']
    for item in new_col:
        table[item] = table['industrial_place']*0
    table['reserve_prom_area_um'] = table['reserve_prom_area_um'].apply(lambda x: 'штук')
    table['reserve_area_um'] = table['reserve_area_um'].apply(lambda x: 'штук')
    return table.to_dict('records')
def read_db_mechanic():
    #Read from DB
    con = sqlite3.connect('C:/Users/rodion.semendyayev/PycharmProjects/Dash_plotly/Data_bases/info_mechanic.db')
    df = pd.read_sql('SELECT * FROM info_mechanic', con)
    con.close()
    #Not fast but well known, rewrite on sql - requests
    df['date'] = pd.to_datetime(df['date'])
    df.set_index(df['date'], inplace=True)
    df.drop(['id'], inplace=True, axis=1)
    df = df.sort_index()
    return df

global_table_economic = [{ "detail": "-",
                        "brand":"-",
                        "detail_last_repair":"-",
                        "cost":"-",
                        "cost_all":"-",
                        "ore_processing":"-",
                        "cost_price":"-",
                        }]

def get_df_and_diff_data(start_date, end_date):
    '''
    get a dataframe from database and calculate a time diffrence between work time and equipment downtime
    :return: df and time
    '''
    df = read_db_mechanic()
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    diff_data = int((end_date - start_date).total_seconds()) / 3600
    return df, diff_data
def summation_ktg(start_date, end_date, col_name, elem_name, one_or_two_type = 1):
    '''
    calculate for all equipment coefficient of technical readiness and draw a barplot
    :return: barplot for equipment
    '''
    df, diff_data = get_df_and_diff_data(start_date, end_date)
    if one_or_two_type == 1:
        sum_time = df.loc[start_date:end_date,:].groupby([col_name, 'equipment'])['repair_time'].sum().to_frame('sum_repair_time')
    else:
        sum_time = df.loc[start_date:end_date,:].groupby(['area', 'type_eq', 'equipment'])['repair_time'].sum().to_frame('sum_repair_time')

    sum_time['ktg'] = (diff_data - sum_time['sum_repair_time']) / diff_data * 100
    sum_time.reset_index(inplace=True)
    if one_or_two_type == 1:
        df_aux = choice_of_dropdown.query(f"{col_name} == '{elem_name}'")['detail'].to_frame('equipment')
        df_sum = sum_time.query(f"{col_name} == '{elem_name}'")
    else:
        df_aux = choice_of_dropdown.query(f"area == '{col_name}' & type_eq == '{elem_name}'")['detail'].to_frame('equipment')
        df_sum = sum_time.query(f"area == '{col_name}' & type_eq == '{elem_name}'")


    if len(df_sum) == 0:
        df_aux['ktg'] = 100
    else:
        df_aux = pd.merge(df_sum, df_aux, on='equipment', how='outer')[['equipment','ktg']]
        df_aux.fillna(100, inplace=True)
    rounded_ktg = [round(value, 2) for value in df_aux['ktg']]
    height_ = 40*len(df_aux['ktg'])
    if height_ < 320:
        height_ = 320
    plot_ktg = go.Bar(y=df_aux['equipment'], x=df_aux['ktg'], text=rounded_ktg, orientation='h')
    plot_ktg_fig = go.Figure(plot_ktg, layout = go.Layout(hovermode = 'closest', template='plotly_white',
                             title='Коэффициент технической готовности оборудования',  height=height_, yaxis=dict(autorange="reversed")))
    return plot_ktg_fig, df_aux['equipment']

# def summation_repair(start_date, end_date, col_name, elem_name, one_or_two_type = 1):
#     '''
#     calculate for all equipment type of repairs  and draw a barplot
#     :return: barplot
#     '''
#     df, _ = get_df_and_diff_data(start_date, end_date)
#     if one_or_two_type == 1:
#         df = df.query(f"{col_name} == '{elem_name}'")
#     else:
#         df = df.query(f"area == '{elem_name[0]}' & type_eq == '{elem_name[1]}'")
#
#     if len(df) == 0:
#         traces = go.Bar(x=None, y=None)
#     else:
#         df = df.loc[start_date:end_date,:].groupby(['equipment','type_of_repair'])['type_of_repair'].count().to_frame('count_type_repair').reset_index()
#         df = pd.get_dummies(df, columns=['type_of_repair'])
#
#         not_use_columns = ['equipment','count_type_repair']
#         new_col_names = []
#         for item in df.columns:
#             if item not in not_use_columns:
#                 prefix = 'type_of_repair_'
#                 df[item[len(prefix):]] = df[item]*df['count_type_repair']
#                 new_col_names.append(item[len(prefix):])
#         traces = []
#         for item in new_col_names:
#             traces.append(go.Bar(x=df['equipment'], y=df[item], text=df[item], name=item))
#     plot_repair_fig = go.Figure(data=traces, layout = go.Layout(hovermode = 'closest', template='plotly_white', title='Количество ремонтов'))
#     return plot_repair_fig

def summation_repears(sum_series, name):
    '''
    get an info about
    :param sum_series: pandas series where sum of all repair's type
    :param name:
    :return:
    '''
    try:
        planned = sum_series.loc[name]
    except:
        planned = 0
    return planned
def summation_repair_or_detail(start_date, end_date, col_name, elem_name, title_='Количество ремонтов', repair_or_detail = 'type_repair', one_or_two_type = 1):
    '''
    calculate for all equipment type of repairs or details for repair and draw a barplot, and do summation for all types of repairs
    :return: barplot, stattistic about repairs
    '''
    df, _ = get_df_and_diff_data(start_date, end_date)
    if one_or_two_type == 1:
        df = df.query(f"{col_name} == '{elem_name}'")
    else:
        df = df.query(f"area == '{col_name}' & type_eq == '{elem_name}'")
    new_col_names = []
    if len(df) == 0:
        traces = go.Bar(x=None, y=None)
    else:
        if repair_or_detail == 'type_repair':
            df = df.loc[start_date:end_date,:].groupby(['equipment','type_of_repair'])['type_of_repair'].count().to_frame('count_type_repair').reset_index()
            df = pd.get_dummies(df, columns=['type_of_repair'])
            prefix = 'type_of_repair_'
        else:
            df = df.loc[start_date:end_date, :].groupby(['equipment', 'unit_meas'])['amount'].sum().to_frame(f'count_amount').reset_index()
            df = pd.get_dummies(df, columns=['unit_meas'])
            prefix = 'unit_meas_'

        not_use_columns = ['equipment',f'count_{repair_or_detail}']
        for item in df.columns:
            if item not in not_use_columns:
                df[item[len(prefix):]] = df[item]*df[f'count_{repair_or_detail}']
                new_col_names.append(item[len(prefix):])
        traces = []
        colors = ['#98fb98', '#ffcc00', '#ff4c5b']
        for index, item in enumerate(new_col_names):
            traces.append(go.Bar(
                x=df[item],
                y=df['equipment'],
                text=df[item],
                name=item,
                showlegend=True,
                orientation='h',
                # marker=dict(
                #     color=colors[index],
                #     line=dict(color='rgba(58, 71, 80, 1.0)', width=1)
                # )
            ))
    height_ = 50 * len(df)
    if height_ < 320:
        height_ = 320
    plot_repair_fig = go.Figure(data=traces, layout = go.Layout(hovermode = 'closest', template='plotly_white', title=title_, height=height_))
    plot_repair_fig.update_layout(barmode='stack')
    sum_series = df[new_col_names].sum()
    planned, unplanned, fault = summation_repears(sum_series, 'Плановый'), summation_repears(sum_series, 'Внеплановый'), summation_repears(sum_series, 'Аварийный')

    return plot_repair_fig, planned, unplanned, fault

# def summation_detail(start_date, end_date, col_name, elem_name, one_or_two_type = 1):
#     '''
#
#     :param start_date: datetime
#     :param end_date: datetime
#     :param col_name: str
#     :param elem_name: str
#     :param one_or_two_type: int
#     :return:
#     '''
#     df, _ = get_df_and_diff_data(start_date, end_date)
#     if one_or_two_type == 1:
#         df = df.query(f"{col_name} == '{elem_name}'")
#     else:
#         df = df.query(f"area == '{elem_name[0]}' & type_eq == '{elem_name[1]}'")
#
#     if len(df) == 0:
#         traces = go.Bar(x=None, y=None)
#     else:
#         df = df.loc[start_date:end_date, :].groupby(['equipment', 'unit_meas'])['amount'].sum().to_frame(f'count_amount').reset_index()
#         df = pd.get_dummies(df, columns=['unit_meas'])
#
#         not_use_columns = ['equipment','count_amount']
#         new_col_names = []
#         for item in df.columns:
#             if item not in not_use_columns:
#                 prefix = 'unit_meas_'
#                 df[item[len(prefix):]] = df[item] * df['count_amount']
#                 new_col_names.append(item[len(prefix):])
#         traces = []
#         #pd.set_option('display.max_columns', None)
#
#         for item in new_col_names:
#             traces.append(go.Bar(x=df['equipment'], y=df[item], text=df[item], name=item))
#
#     plot_detail_fig = go.Figure(data=traces, layout = go.Layout(hovermode = 'closest', template='plotly_white', title='Количество использованных запчастей'))
#
#     return plot_detail_fig

@callback(
    [#Output('table', 'columns'),
     #Output('table_repair', 'data'),
     #Output('table_repair', 'columns'),
     Output('table_sum', 'data'),
     Output('planned', 'children'),
     Output('unplanned', 'children'),
     Output('fault', 'children'),
     Output("choice_area", "options"),
     Output("choice_type_eq", "options"),
     Output("choice_eq", "options"),
     Output('table_reserve', 'data'),
     Output('table_econimic', 'data'),
     Output('ktg', 'children'),
     Output('plot_ktg', 'figure'),
     Output('plot_repair', 'figure'),
     Output('div_container', 'children')

    ],
    [
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('choice_eq', 'value'),
     Input('choice_area', 'value'),
     Input('choice_type_eq', 'value'),
     ],
    [
     State('div_container', 'children')
    ]
)

def update_graph(start_date, end_date, eq, choice_area, choice_type_eq, existing_children):
    df, diff_data = get_df_and_diff_data(start_date, end_date)



    if eq != None and start_date != None and end_date != None:
        df_little = df.loc[start_date:end_date, :].query("equipment == @eq")
        df_all = df.query("equipment == @eq")
        mask = detail_output['detail'].apply(lambda x: True if eq in x else False)
        detail_output_mech_part = detail_output[mask]['mech_part'].to_frame('detail')
        table_repair, table_sum, planned, unplanned, fault, repair_time_sum = get_df_table_repair(df_little, df_all, detail_output_mech_part)

        table_economic = get_table_economic(eq, start_date, end_date, df_all[['detail', 'amount']])

        ktg = (diff_data - repair_time_sum) / diff_data * 100
        ktg = f"{ktg:.1f} %"

    else:
        table_repair = [{"detail": "-",
                        "works_date_range": "-",
                        "data_date_range": "-",
                        "amount_date_range": "-",
                        "works_all": "-",
                        "data_all": "-",
                        "amount_all": "-"}]

        table_sum = [{ "detail": "-",
                        "ppr_amount":"-",
                        "ppr_duration":"-",
                        "vne_amount":"-",
                        "vne_duration":"-",
                        "fault_amount":"-",
                        "fault_duration":"-",
                        "sum_amount":"-",
                        "sum_duration":"-",
                    }]
        #planned, unplanned, fault = 0, 0, 0

        table_economic = global_table_economic

        ktg = f"0 %"


    if eq != None:
        table_reserve = get_table_reverse(eq)
    else:
        table_reserve = [{ "detail": "-",
                        "industrial_place":"-",
                        "reserve_prom_area_um":"-",
                        "reserve_area":"-",
                        "reserve_area_um":"-",
                        "request":"-",
                        "date_request":"-",
                        }]

    dropdown_type_area, dropdown_type_eq, dropdown_eq = define_dropdown_list([choice_area,choice_type_eq], choice_of_dropdown)

    # #Visualize a global info about characteristic of mining plant
    # if choice_area != None and choice_type_eq == None:
    #     plot_ktg_fig = summation_ktg(start_date, end_date, 'area', choice_area)
    #     plot_repair, planned, unplanned, fault = summation_repair_or_detail(start_date, end_date, 'area', choice_area)
    #     table_sum = get_df_table_repair_area_type_eq(df.loc[start_date:end_date, :], 'area', choice_area)
    #     #plot_detail = summation_repair_or_detail(start_date, end_date, 'area', choice_area, title_='Количество используемых деталей', repair_or_detail = 'amount')
    # elif choice_area == None and choice_type_eq != None:
    #     plot_ktg_fig = summation_ktg(start_date, end_date, 'type_eq', choice_type_eq)
    #     plot_repair, planned, unplanned, fault = summation_repair_or_detail(start_date, end_date, 'type_eq', choice_type_eq)
    #     table_sum = get_df_table_repair_area_type_eq(df.loc[start_date:end_date, :], 'type_eq', choice_type_eq)
    #     #plot_detail = summation_repair_or_detail(start_date, end_date, 'type_eq', choice_type_eq, title_='Количество используемых деталей', repair_or_detail='amount')
    # elif choice_area != None and choice_type_eq != None:
    #     plot_ktg_fig = summation_ktg(start_date, end_date, 'area', [choice_area, choice_type_eq], one_or_two_type = 2)
    #     plot_repair, planned, unplanned, fault = summation_repair_or_detail(start_date, end_date, 'area', [choice_area, choice_type_eq], one_or_two_type = 2)
    #     table_sum = get_df_table_repair_area_type_eq(df.loc[start_date:end_date, :], choice_area, choice_type_eq, one_or_two_type=2)
    #     # plot_detail = summation_repair_or_detail(start_date, end_date, 'area', [choice_area, choice_type_eq], title_='Количество используемых деталей',
    #     #                                          repair_or_detail='amount', one_or_two_type = 2)
    # else:
    #     plot_ktg_fig = summation_ktg(start_date, end_date, 'type_eq', 'Мельница')
    #     plot_repair, planned, unplanned, fault = summation_repair_or_detail(start_date, end_date, 'type_eq', 'Мельница')
    #     #plot_detail = summation_repair_or_detail(start_date, end_date, 'type_eq', 'Мельница', title_='Количество используемых деталей', repair_or_detail='amount')

    #Visualize a global info about characteristic of mining plant
    if choice_area != None and choice_type_eq == None:
        args_, kwargs_  = ['area', choice_area], {}
        #plot_detail = summation_repair_or_detail(start_date, end_date, 'area', choice_area, title_='Количество используемых деталей', repair_or_detail = 'amount')
    elif choice_area == None and choice_type_eq != None:
        args_, kwargs_  = ['type_eq', choice_type_eq], {}
        #plot_detail = summation_repair_or_detail(start_date, end_date, 'type_eq', choice_type_eq, title_='Количество используемых деталей', repair_or_detail='amount')
    elif choice_area != None and choice_type_eq != None:
        args_, kwargs_ = [choice_area, choice_type_eq], {"one_or_two_type": 2}
        # plot_detail = summation_repair_or_detail(start_date, end_date, 'area', [choice_area, choice_type_eq], title_='Количество используемых деталей',
        #                                          repair_or_detail='amount', one_or_two_type = 2)
    else:
        args_, kwargs_ = ['type_eq', 'Мельница'], {}

    plot_ktg_fig, list_eq = summation_ktg(start_date, end_date, *args_, **kwargs_)
    plot_repair, planned, unplanned, fault = summation_repair_or_detail(start_date, end_date, *args_, **kwargs_)
    table_sum = get_df_table_repair_area_type_eq(df.loc[start_date:end_date, :], *args_, **kwargs_)
    existing_children = []
    for item in list_eq:
        df_little = df.loc[start_date:end_date, :].query("equipment == @item")
        df_all = df.query("equipment == @item")
        mask = detail_output['detail'].apply(lambda x: True if item in x else False)
        detail_output_mech_part = detail_output[mask]['mech_part'].to_frame('detail')
        table_repair, _, _, _, _, _ = get_df_table_repair(df_little, df_all, detail_output_mech_part)
        new_div = html.Div([
            html.Div(f'Последний ремонт оборудования {item}', className='name_of_block'),
            dash_table.DataTable(
                data = table_repair,
                columns=[
                    {"name": ["", "Деталь или узел"], "id": "detail"},
                    {"name": ["Последний ремонт за выбранный период", "Наименование работ"], "id": "works_date_range"},
                    {"name": ["Последний ремонт за выбранный период", "Дата"], "id": "data_date_range"},
                    {"name": ["Последний ремонт за выбранный период", "Количество деталей"], "id": "amount_date_range"},
                    {"name": ["Последний ремонт за все время", "Наименование работ"], "id": "works_all"},
                    {"name": ["Последний ремонт за все время", "Дата"], "id": "data_all"},
                    {"name": ["Последний ремонт за все время", "Количество деталей"], "id": "amount_all"},
                ],
                merge_duplicate_headers=True,
                style_table={
                    'overflowX': 'auto',
                    "width": "100%",
                    "borderBottomLeftRadius": "0.625rem",
                    "borderBottomRightRadius": "0.625rem",
                    },
                style_header={"text-align": "center", "background": '#f8f9fa', 'color': '#5a6169',
                              'font-family': 'var(--bs-body-font-family)'},
                style_data={"text-align": "center"},
                sort_action = 'native',
                sort_mode = 'single',
            ),
        ], className='table_info')
        existing_children.append(new_div)
        #table_economic = get_table_economic(eq, start_date, end_date, df_all[['detail', 'amount']])

        #ktg = (diff_data - repair_time_sum) / diff_data * 100
        #ktg = f"{ktg:.1f} %"

    return table_sum, planned, unplanned, fault, dropdown_type_area, dropdown_type_eq, dropdown_eq, table_reserve, table_economic, ktg, plot_ktg_fig, plot_repair, existing_children
