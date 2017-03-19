import re
import os


DEFAULT_MIN_PASSWORD_LENGTH = 6


def load_data(file_path):
    with open(file_path, 'rt') as file:
        return file.read().split('\n')


def input_from_file_or_manual(text):
    work_file = input(text)

    if not os.path.exists(work_file):
        print('Файл {} не существует'.format(work_file))
        data = input('Введите данные через пробел:').split()
        print('='*80)
    else:
        data = load_data(work_file)

    return data


def is_password_long(password):
    return (len(password) >= DEFAULT_MIN_PASSWORD_LENGTH)


def has_both_upper_and_lower_cases(password):
    return (not password.isupper() and not password.islower())


def has_numerical_digits(password):
    return bool(re.search('\d+', password))


def has_special_char(password):
    return bool(re.search(r'[ !#$%&():*+,-./[\\\]^_`{|}~]', password))


def has_forbidden_words(password, forbidden_words):
    PATTERN_DD_MM_YYYY = "(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d"
    PATTERN_MM_DD_YYYY = "(0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])[- /.](19|20)\d\d"
    has_forbidden_words = bool(re.search(PATTERN_MM_DD_YYYY, password))

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
    
    password = input('Введите пароль:')
    
    blacklist = input_from_file_or_manual('Введите имя файла черного списка:')
    personal_info = input_from_file_or_manual('Введите имя файла с персональной ифнормацией:')
    company_name = input_from_file_or_manual('Введите имя файла c полным и кратким названием компании:')
    forbidden_words = blacklist + personal_info + company_name

    password_strength = get_password_strength(password, forbidden_words)
    print('Оценка силы пароля: {}'.format(password_strength))