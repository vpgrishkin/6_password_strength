import re
import os
from getpass import getpass


DEFAULT_MIN_PASSWORD_LENGTH = 6


def load_data(file_path):
    with open(file_path, 'rt') as file:
        return file.read().split('\n')


def input_from_file_or_manual(text):
    work_file = input(text)

    if not os.path.exists(work_file):
        print('Файл {} не существует'.format(work_file))
        inputed_user_data = input('Введите данные через пробел:').split()
        print('='*80)
    else:
        inputed_user_data = load_data(work_file)

    return inputed_user_data


def is_password_long(password):
    return (len(password) >= DEFAULT_MIN_PASSWORD_LENGTH)


def has_both_upper_and_lower_cases(password):
    return (not password.isupper() and not password.islower())


def has_numerical_digits(password):
    return bool(re.search('\d+', password))


def has_special_char(password):
    return bool(re.search(r'[ !#$%&():*+,-./[\\\]^_`{|}~]', password))


def has_forbidden_words(password, forbidden_words):
    pattern_dd_mm_yyyy = "(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d"
    pattern_mm_dd_yyyy = "(0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])[- /.](19|20)\d\d"
    has_forbidden_words = bool(re.search(pattern_dd_mm_yyyy, password))
    has_forbidden_words = bool(re.search(pattern_mm_dd_yyyy, password))

    if password in forbidden_words:
        has_forbidden_words = True

    return has_forbidden_words


def get_password_strength(password, forbidden_words):
    strength = 0
    if is_password_long(password):
        strength += 2
    if has_both_upper_and_lower_cases(password):
        strength += 3
    if has_numerical_digits(password):
        strength += 2
    if has_special_char(password):
        strength += 3
    if has_forbidden_words(password, forbidden_words):
        strength /= 2

    return strength


if __name__ == '__main__':
    password = getpass("Введите пароль:")
    
    blacklist = input_from_file_or_manual('Введите имя файла черного списка:')
    personal_info = input_from_file_or_manual('Введите имя файла с персональной ифнормацией:')
    company_name = input_from_file_or_manual('Введите имя файла c полным и кратким названием компании:')
    forbidden_words = blacklist + personal_info + company_name

    password_strength = get_password_strength(password, forbidden_words)
    print('Оценка силы пароля: {}'.format(password_strength))