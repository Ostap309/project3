from data import db_session, users
from datetime import datetime

def search_people(user, gender, age1, age2):
    db_session.global_init("db/db_users.sqlite")
    session = db_session.create_session()
    sl = {}
    if user.city != None:
        for person in session.query(users.User).all():
            if person.id != user.id:
                if person.city == user.city:
                    d1 = datetime.strptime(person.date, "%d.%m.%Y")
                    d2 = datetime.strptime(user.date, "%d.%m.%Y")
                    if str(d2 - d1).split(' ')[0] != '0:00:00':
                        n = abs(int(str(d2 - d1).split(' ')[0]))
                    else:
                        n = 0
                    if len(sl) < 3:
                        sl[person.id] = n
                    else:
                        keys = list(sl.keys())
                        values = list(sl.values())
                        if n < max(values):
                            del sl[keys[values.index(max(values))]]
                            sl[person.id] = n
    sl2 = {}
    for person in session.query(users.User).all():
        if person.id != user.id:
            score = 0
            max_score = 4
            if not user.music is None:
                max_score += len(str(user.music).split(','))
            if not user.books is None:
                max_score += len(str(user.books).split(','))

            if person.age >= int(age1) and person.age <= int(age2):
                score += 1
            if gender == 'None' or gender == person.gender:
                score += 1
            if not user.music is None:
                for i in str(user.music).split(','):
                    if i in str(person.music):
                        score += 1
            if not user.books is None:
                for i in str(user.books).split(','):
                    if i in str(person.books):
                        score += 1
            if user.temperament != 'Не отвечать' and person.temperament != 'Не отвечать':
                if user.temperament == 'Сангвиник':
                    if person.temperament == 'Сангвиник':
                        score += 2
                    elif person.temperament != 'Флегматик':
                        score += 1
                elif user.temperament == 'Холерик':
                    if person.temperament == 'Флегматик':
                        score += 2
                    elif person.temperament != 'Холерик':
                        score += 1
                elif user.temperament == 'Флегматик':
                    if person.temperament == 'Флегматик' or person.temperament == 'Меланхолик':
                        score += 2
                    elif person.temperament != 'Сангвиник':
                        score += 1
                else:
                    if person.temperament == 'Сангвиник':
                        score += 2
                    elif person.temperament != 'Меланхолик':
                        score += 1

            sl2[person.id] = int(100 / max_score * score)
    if sl:
        list1 = list(sl.items())
        list1.sort(key=lambda i: i[1])
        list1 = [i[0] for i in list1]

        s1 = [session.query(users.User).filter(users.User.id == i).first() for i in list1]
    else:
        s1 = []

    if sl2:
        list2 = list(sl2.items())
        list2.sort(key=lambda i: i[1], reverse=True)
        list2 = [i[0] for i in list2][:3]

        s2 = [session.query(users.User).filter(users.User.id == i).first() for i in list2]
    else:
        s2 = []

    return s1, s2, sl2
