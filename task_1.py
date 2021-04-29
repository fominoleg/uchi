import pandas as pd
import numpy as np

# информация о принадлежности пользователя к контрольной или
# экспериментальной группе (А – контроль, B – целевая группа)
groups_frame = pd.read_csv('data/groups.csv', sep=';')

# информация о пользователях, которые зашли на платформу в
# дни проведения эксперимента
active_studs_frame = pd.read_csv('data/active_studs.csv', sep=';')

# информация об оплатах пользователей в дни проведения эксперимента
checks_frame = pd.read_csv('data/checks.csv', sep=';')


frame = groups_frame.merge(active_studs_frame, how='left', left_on='id', right_on='student_id')
frame = frame.merge(checks_frame, how='left', left_on='id', right_on='student_id')

frame.to_csv("~/garbage/uchi.csv", index=False)

result_dict = {
    grp: {
        "Не заходил, не платил": 0,
        "Не заходил, платил": 0,
        "Не заходил, платил (сумма)": 0,
        "Заходил, не платил": 0,
        "Заходил, платил": 0,
        "Заходил, платил (сумма)": 0,
    }
    for grp in sorted(set(frame['grp'].values.tolist()))
}

frame = frame.rename(columns={'student_id_x': 'visit', 'student_id_y': 'paid'})

print("Доля студентов A: ", frame.loc[frame['grp'] == 'A'].shape[0] / frame.shape[0])
print("Доля студентов B: ", frame.loc[frame['grp'] == 'B'].shape[0] / frame.shape[0])

print("Доля студентов A, посетивших сайт: ",
      frame.loc[(frame['grp'] == 'A') & (~np.isnan(frame['visit']))].shape[0] / frame.loc[frame['grp'] == 'A'].shape[0])
print("Доля студентов B, посетивших сайт: ",
      frame.loc[(frame['grp'] == 'B') & (~np.isnan(frame['visit']))].shape[0] / frame.loc[frame['grp'] == 'B'].shape[0])

print("Доля студентов A, посетивших сайт и заплативших: ",
      frame.loc[(frame['grp'] == 'A') &
                (~np.isnan(frame['visit'])) &
                (~np.isnan(frame['paid']))].shape[0] / frame.loc[frame['grp'] == 'A'].shape[0])
print("Доля студентов B, посетивших сайт и заплативших: ",
      frame.loc[(frame['grp'] == 'B') &
                (~np.isnan(frame['visit'])) &
                (~np.isnan(frame['paid']))].shape[0] / frame.loc[frame['grp'] == 'B'].shape[0])


print("Средняя сумма оплаты A: ",
      sum(frame.loc[(frame['grp'] == 'A') &
                (~np.isnan(frame['visit'])) &
                (~np.isnan(frame['paid']))]['rev'].values.tolist()) /
      frame.loc[(frame['grp'] == 'A') &
                (~np.isnan(frame['visit'])) &
                (~np.isnan(frame['paid']))].shape[0])

print("Средняя сумма оплаты B: ",
      sum(frame.loc[(frame['grp'] == 'B') &
                (~np.isnan(frame['visit'])) &
                (~np.isnan(frame['paid']))]['rev'].values.tolist()) /
      frame.loc[(frame['grp'] == 'B') &
                (~np.isnan(frame['visit'])) &
                (~np.isnan(frame['paid']))].shape[0])


'''
Доля студентов A:  0.19702048916541515
Доля студентов B:  0.8029795108345849
Доля студентов A, посетивших сайт:  0.10467569590961683
Доля студентов B, посетивших сайт:  0.11360486281582419
Доля студентов A, посетивших сайт и заплативших:  0.005308650377730892
Доля студентов B, посетивших сайт и заплативших:  0.005243558271963662
Средняя сумма оплаты A:  933.5897435897435
Средняя сумма оплаты B:  1257.8789920382171

Выводы:
1. Смотрим только тех людей, которые посетили сайт за тестируемый период
2. Целевая группа составляет 80% от всех людей (почему?)
3. Доля студентов, посетивших сайт в обеих группах, сопоставимо (10% в группе A и 11% в группе B)
4. Доля студентов, посетивших сайт и заплативших, так же сопоставимо (0.5% в группе A и 0.5% в группе B)
5. При этом средняя сумма оплаты в группе B ~ на 30% больше, чем в группе A
'''