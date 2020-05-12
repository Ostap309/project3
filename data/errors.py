from data import db_session, users


def login_unique_error_testing(login):
    db_session.global_init('db/db_users.sqlite')
    session = db_session.create_session()
    s = [i.email for i in session.query(users.User).all()]
    if login in s:
        return False
    return True


def age_testing(age):
    if str(age).isdigit() and int(age) >= 18 and int(age) <= 130:
        return True
    return False

def phone_number_testing(pn):
    if len(pn) == 11 and str(pn).isdigit():
        return True
    return False

def age_filter_testing(age1, age2):
    if age1.isdigit() and age2.isdigit() and int(age1) >= 18 and int(age2) >= 18 and int(age1) <= 130 and int(age2) <= 130:
        if int(age1) <= int(age2):
            return True
        else:
            return False
    else:
        return False