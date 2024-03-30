HeadHunter Vacancies Downloader

Описание:
Этот проект позволяет пользователю искать вакансии на сайте HeadHunter (hh.ru) по ключевым словам, просматривать топ N вакансий по зарплате, находить вакансии с определенными ключевыми словами в описании и сохранять результаты в файл в формате JSON. Программа предназначена для упрощения процесса поиска работы, позволяя пользователям эффективно собирать и анализировать данные о вакансиях.

Установка и запуск
Требования

Программа требует Python версии 3.6 или выше. Все зависимости, включая requests и библиотеки для тестирования, перечислены в файле requirements.txt.

Установка зависимостей

Перед запуском программы установите необходимые зависимости, используя pip. Откройте терминал или командную строку и выполните следующую команду в директории проекта:

pip install -r requirements.txt

Взаимодействие с программой

После запуска программа предложит ввести поисковый запрос для поиска вакансий, количество вакансий для отображения в топе по зарплате и ключевое слово для фильтрации вакансий по описанию. В конце программы будет предложено сохранить полученные результаты в файл. Если вы согласны, данные будут сохранены в vacancies.json в директории Data.
