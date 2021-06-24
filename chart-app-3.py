# В этом файле я попробую сделать поисковую систему по скачиваемым чартам

######################
# Import libraries
######################

import pandas as pd
import streamlit as st
from PIL import Image
from datetime import date, datetime
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset


# -- Set page config
apptitle = 'Charts by UMD'
st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:")

######################
# Download data
######################
# wb = openpyxl.load_workbook('charts.xlsx')
# sheets = list(wb.sheetnames)

today = datetime.now().date()

######################
# Page Title
######################
image = Image.open('YM1.png')
st.image(image, width=150)


# Title the app
st.title('Поиск по чартам ВК, Yandex, Apple и Spotify')

st.markdown("""
 * В меню слева укажите параметры поиска 
 * результаты поиска можно будет увидеть ниже
 * потрековые чарты - Apple top 100, VK - top 100, Yandex - top 100, Spotify - top 50
 * альбомные чарты - Apple top 50, VK - top 100
""")

######################
# Side menu
######################

st.sidebar.markdown("## Выбор параметров поиска")

select_event = st.sidebar.selectbox('Сводный чарт или поиск по артисту/треку',
                                    ['Сводный чарт', 'поиск по артисту/треку'])

if select_event == 'Сводный чарт':
    # st.sidebar.markdown ( '#### Выбор даты' )
    chart_date_input = today
    chart_date_input = st.sidebar.text_input ( "Введите дату", chart_date_input )
    chart_date = str(chart_date_input)  # начало временного отрезка

    st.sidebar.markdown ( """
                Пример ввода даты:
                * 2021-05-22 (год-месяц-день)
                * 2021-06-9 (год-месяц-день)
                * будьте внимательны к пробелам
                """ )

    unique_pos = ['Apple потрековый', 'Apple альбомный', 'ВК потрековый', 'ВК альбомный', 'Yandex потрековый',
                  'Spotify потрековый']
    selected_pos1 = st.sidebar.multiselect ( 'Выбор чарта', unique_pos, unique_pos )
    selected_pos = []

    if len (selected_pos1) > 0:
        for item in selected_pos1:
            if item == 'Apple потрековый':
                selected_pos.append ( 'apple_chart.csv' )
            elif item == 'Apple альбомный':
                selected_pos.append ( 'apple_alb_chart.csv' )
            elif item == 'ВК потрековый':
                selected_pos.append ( 'vk_track.csv' )
            elif item == 'ВК альбомный':
                selected_pos.append ( 'vk_album.csv' )
            elif item == 'Yandex потрековый':
                selected_pos.append ( 'yandex_chart.csv' )
            elif item == 'Spotify потрековый':
                selected_pos.append ( 'spotify_chart.csv' )
    else:
        st.sidebar.markdown ( """
                    пожалуйста, выберите как минимум 1 чарт
                    """ )
    ######################
    # Обработка и вывод сводного чарта
    ######################

    index = list (range(0,100))
    table = pd.DataFrame(' ',index = index, columns = selected_pos1)
    for i in range(len(selected_pos1)):
        try:
            df = pd.read_csv(selected_pos[i])
            # for col in df.columns:
            #     if "Unnamed" in col:
            #         df.drop([col], axis = 1, inplace = True)
            # создадим список всех колонок, которые относятся к нужному дню
            date_columns = []
            for item in df.columns:
                if pd.to_datetime(item).date() == pd.to_datetime(chart_date).date():
                    date_columns.append(item)
            if len(date_columns)>1:
                col_name = date_columns[round(len(date_columns)/2)+1]
            else:
                # len(date_columns) == 1
                col_name = date_columns[0]
            # else:
            #     st.write(f'Нет информации от этой даты в чарте {selected_pos1[i]}')
            # st.write(selected_pos1[i])
            for j in range(len(df[col_name])):
                table[selected_pos1[i]].iloc[j]=df[col_name].iloc[j]
            # st.write(f'Сводный чарт за {chart_date}')

            # table

        except:
            st.write(f'_Нет информации на указанную дату по чарту {selected_pos1[i]}_')
    st.write ( f'Сводный чарт за {chart_date}' )

    table

else:
    # выбор дат начала и конца поиска
    # st.sidebar.markdown('#### Выбор глубины поиска')

    first_date_input = "2021-05-03"
    first_date_input = st.sidebar.text_input ( "Введите начальную дату поиска", first_date_input)
    first_date = str(first_date_input) # начало временного отрезка

    last_date_input = str(today)
    last_date_input = st.sidebar.text_input ( "Введите финальную дату поиска", last_date_input)
    finish_date = str(last_date_input) # конец временного отрезка

    st.sidebar.markdown ( """
            Пример ввода даты:
            * 2021-05-03 (год-месяц-день)
            * будьте внимательны к пробелам
            """ )
    # выбор чартов, по которым производится поиск
    unique_pos = ['Apple потрековый','Apple альбомный','ВК потрековый','ВК альбомный','Yandex потрековый', 'Spotify потрековый']
    selected_pos1 = st.sidebar.multiselect('Выбор чарта', unique_pos, unique_pos)
    selected_pos = []
    if len(selected_pos1)>0:
        for item in selected_pos1:
            if item == 'Apple потрековый':
                selected_pos.append('apple_chart.csv')
            elif item == 'Apple альбомный':
                selected_pos.append ( 'apple_alb_chart.csv' )
            elif item == 'ВК потрековый':
                selected_pos.append ( 'vk_track.csv' )
            elif item == 'ВК альбомный':
                selected_pos.append ( 'vk_album.csv' )
            elif item == 'Yandex потрековый':
                selected_pos.append ( 'yandex_chart.csv' )
            elif item == 'Spotify потрековый':
                selected_pos.append ( 'spotify_chart.csv' )
    else:
        st.sidebar.markdown ( """
                пожалуйста, выберите как минимум 1 чарт
                """ )


    #-- выбор способа поиска по чартам
    select_event = st.sidebar.selectbox('Артист или трек',
                                        ['По имени артиста', 'По названию трека/альбома'])

    if select_event == 'По названию трека/альбома':

        title_name_input = "Истеричка"
        title_name_input = st.sidebar.text_input ( "Введите название трека или альбома", title_name_input )
        search_title = title_name_input

        st.sidebar.markdown ( """
            Пример ввода названия трека:
            * Истеричка 
            * BESTSELLER 
            """ )

        artist_name_input = "Artik&Asti"
        artist_name_input = st.sidebar.text_input ( "Введите имя артиста", artist_name_input )
        search_name = artist_name_input

        st.sidebar.markdown ( """
                Пример ввода имени артиста:
                * Artik&Asti 
                * Artik & Asti
                * Егор Крид
                """ )

    ######################
    # Обработка и вывод поиска по названию трека или альбома
    ######################
        if len(search_name) == 0 or len(search_title) == 0:
            st.write('## Пожалуйста, укажите название трека и имя артиста')
        else:
            st.header ( f'{search_name} c треком {search_title}' )
            st.subheader (
                f'В период с {pd.to_datetime ( first_date ).strftime ( "%d-%b-%Y" )} по {pd.to_datetime ( finish_date ).strftime ( "%d-%b-%Y" )}' )
            for i in range(len(selected_pos)):
                n = 0
                df = pd.read_csv(selected_pos[i])
                for col in df.columns:
                    if "Unnamed" in col:
                        df.drop ( [col], axis = 1, inplace = True )
                columns = list(df.columns)
                columns_new = []  # выделаем временной отрезок для поиска
                for col in columns:
                    if pd.to_datetime(col) >= pd.to_datetime(first_date) and pd.to_datetime (
                            col) <= pd.to_datetime(finish_date):
                        columns_new.append (col)

                df_for_search = df[columns_new].copy()  # формируем базу, соответствующую временному срезу
                columns1 = list(df_for_search.columns)
                song_dict = {}
                # song_name = []
                # наполняем словарь информацией по треку - место и дата, когда место было
                for col in columns1:
                    for j in range(len(df_for_search[col])):
                        if search_title.lower().replace( ' ', '' ) in str(
                                df_for_search[col].iloc[j]).lower().replace(
                                ' ', '') and search_name.lower().replace(' ', '') in str(
                            df_for_search[col].iloc[j]).lower().replace (
                            ' ', ''):
                            n+=1
                            place = df_for_search[col].iloc[j].split (',')[0]  # место в чарте
                            try:
                                value = song_dict[search_title]
                                new_value = value + [[pd.to_datetime(col).strftime ( "%d-%b-%Y" ), place]]
                                song_dict[search_title] = new_value
                            except:
                                song_dict[search_title] = [[pd.to_datetime (col).strftime ( "%d-%b-%Y" ), place]]

                if n != 0: # то есть если трек и артист встретились в чарте
                    test = pd.DataFrame ( song_dict[search_title] )
                    test[1] = test[1].apply (lambda x: int(x))
                    # st.write (
                    #     f'Tрек {search_title} в период с {pd.to_datetime ( first_date ).strftime ( "%d-%b-%Y" )} по {pd.to_datetime ( finish_date ).strftime ( "%d-%b-%Y" )}' )
                    # определяем пиковую позицию
                    if len(test.index[test[1] == test[1].min ()]) > 1:
                        date = []
                        for j in range(len(test.index[test[1] == test[1].min()])):
                            if test[0].iloc[test.index[test[1] == test[1].min ()][j]] not in date:
                                date.append(test[0].iloc[test.index[test[1] == test[1].min ()][j]])
                    else:
                        date = test[0].iloc[test.index[test[1] == test[1].min ()][0]]

                    # определяем количество дней в чарте
                    days = []
                    for j in range(len(test[0])):
                        if test[0].iloc[j] not in days:
                            days.append(test[0].iloc[j])
                    st.write ( f'количество дней в **{selected_pos1[i]}** -{len ( days )}' )
                    st.write ( f'пиковая позиция  - **{test[1].min ()}** место {date}' )

                    fig = plt.figure ( figsize = (10, 5) )
                    axes = fig.add_axes ( plt.gca () )
                    axes.invert_yaxis ()
                    axes.plot ( test[1] )
                    axes.set_ylabel ( 'место в чарте' )
                    axes.set_xlabel ( 'время в чарте' )
                    axes.set_xticklabels ([])
                    st.pyplot ( fig )
                else:
                    st.write ( f'В чарте "{selected_pos1[i]}" не появлялся' )

    else:
        artist_name_input = "Artik&Asti"
        artist_name_input = st.sidebar.text_input ( "Введите имя артиста", artist_name_input)
        search_name = artist_name_input
        search_title = 'Не выбрано'

        st.sidebar.markdown ( """
            Пример ввода имени артиста:
            * Artik&Asti 
            * Artik & Asti
            * Егор Крид
            """ )

        ######################
        # Обработка и вывод поиска по артисту
        ######################
        if len(search_name) == 0:
            st.write('## Пожалуйста, укажите имя артиста')
        else:
            st.header ( f'{search_name}' )
            st.subheader (
                f'В период с {pd.to_datetime ( first_date ).strftime ( "%d-%b-%Y" )} по {pd.to_datetime ( finish_date ).strftime ( "%d-%b-%Y" )}' )

            for i in range(len(selected_pos)):
                n = 0
                df = pd.read_csv(selected_pos[i])
                for col in df.columns:
                    if "Unnamed" in col:
                        df.drop ( [col], axis = 1, inplace = True )
                columns = list(df.columns)
                columns_new = []
                # формируем базу для поиска по заданным временнЫм параметрам
                for col in columns:
                    if pd.to_datetime(col) >= pd.to_datetime (first_date) and pd.to_datetime (
                            col) <= pd.to_datetime(finish_date):
                        columns_new.append(col)
                df_for_search = df[columns_new].copy ()
                columns1 = list ( df_for_search.columns )

                # определяем какие песни артиста были в чартах в указанные сроки
                song_dict = {}
                song_name = []
                for col in columns1:
                    for j in range(len(df_for_search[col])):
                        if search_name.lower ().replace(' ', '') in str(df_for_search[col].iloc[j]).lower().replace(
                                ' ', ''):
                            n+=1
                            place = df_for_search[col].iloc[j].split( ',' )[0]  # место в чарте
                            song = df_for_search[col].iloc[j].split( ',' )[-1]  # название трек
                            if song not in song_name:
                                song_name.append(song)
                            try:
                                value = song_dict[song]
                                new_value = value + [[pd.to_datetime(col).strftime("%d-%b-%Y"),place]]
                                song_dict[song] = new_value
                            except:
                                song_dict[song] = [[pd.to_datetime (col).strftime("%d-%b-%Y"), place]]
                if n != 0:
                    st.write ( f'**{selected_pos1[i]}**:')  # название чарта
                    for item in song_name:
                        test = pd.DataFrame(song_dict[item])
                        test[1] = test[1].apply(lambda x: int(x))  # переводим место в число

                        # определяем пиковую позицию в чарте
                        if len(test.index[test[1] == test[1].min()]) > 1:
                            date = []
                            for j in range (len(test.index[test[1] == test[1].min ()])):
                                if test[0].iloc[test.index[test[1] == test[1].min ()][j]] not in date:
                                    date.append (test[0].iloc[test.index[test[1] == test[1].min ()][j]])
                        # elif len(test.index[test[1] == test[1].min()]) == 0:
                        #     st.write(f'{item} не было в чарте в указанные дни')
                        #     break
                        else:
                            date = test[0].iloc[test.index[test[1] == test[1].min()][0]]

                        # определяем количество дней в чарте
                        days = []
                        for j in range(len(test[0])):
                            if test[0].iloc[j] not in days:
                                days.append(test[0].iloc[j])
                        st.write ( f'**{item}**' )
                        st.write (
                            f'количество дней в чарте _(в указанный период времени)_ - {len ( days )}')
                        st.write (
                            f'пиковая позиция  - **{test[1].min ()}** место {date}' )

                        fig = plt.figure ( figsize = (10, 5) )
                        axes = fig.add_axes ( plt.gca () )
                        axes.invert_yaxis ()
                        axes.plot ( test[1] )
                        axes.set_ylabel ('место в чарте')
                        axes.set_xlabel ('время в чарте')
                        # axes.set_yticklabels ( [] )
                        axes.set_xticklabels ([])
                        st.pyplot ( fig )
                else:
                    st.write(f'В чарте "{selected_pos1[i]}" не появлялся')




    st.write("""
    ***
    """)
