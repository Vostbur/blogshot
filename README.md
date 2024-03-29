Blogshot 
=======

Еще один простой генератор статических сайтов
--------------------------------------------------------------------------

В один из выходных дней я выбрал время и собрал в одном файле все мысли о *идеальном* блоговом движке. Туда попали требования к прозрачности и простоте кода, удобству использования и платформенной независимости. И всё это должно быть предельно минималистично, но в то же время красиво.

Мне нравятся одностраничные блоги. Только текст статьи и форма для комментирования. Одна колонка шириной 800px. Ничего лишнего. И еще обязательно надо было написать всё самому. Это важно.

Посмотреть результат можно здесь [vostbur.github.com](http://vostbur.github.com/).

Как пользоваться
---------------------------
Настройки хранятся в файле конфигурации *config.json*. Тексты статей в формате [*Markdown*](http://en.wikipedia.org/wiki/Markdown) хранятся в файлах с расширением **.md*. Обязательные поля в заголовке *date, title, slug*. Шаблон - [*Twitter Bootstrap*](http://twitter.github.com/bootstrap/) с элементами разметки [*Jinja*](http://jinja.pocoo.org/). Комментарии - [*Disqus*](http://disqus.com/).

####Пример:

1. `Date: 2013-01-01`
2. `Title: Первая статья`
3. `Slug: 2013-01-01-first-article`
4. `пустая строка` 
5. **`Текст статьи`**

####Ключи:

 **-h, --help**  - Помощь

 **-i, --init** - Начальные установки. Создаются необходимые каталоги из конфигурационного файла. 
 
**-r, --regen** - Пересоздать все файлы.

  **-d, --draft** - Сгенерировать новые статьи из черновиков.

  **-s, --server** - Запуск локального сервера для проверки.

Требования
------------------
- Python 2.7
- Jinja2
- Markdown
- pyatom

Со временем планирую переписать для Python 3.x.
Код очень сырой и как только будет позволять время, буду улучшать, дописывать и переписывать.
