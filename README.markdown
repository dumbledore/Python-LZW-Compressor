# Общо за проекта

Проектът реализира алгоритъма за компресия LZW, като се полза 64K или 16MB речник. При запълване речникът се изпразва и пълни наново.

Проектът е разработен от *Светлин Анков* 

# Структура на проекта

## compress

Реализира компресията. Изпълнява се чрез извикване като метод или от command prompt-а. При извикване без параметри ще даде хелп.

*   *process\_command\_line(arguments, automated = False)* – Обработва аргументите от CMD
*   *compress(file\_in, file\_out, buffer\_size, large\_dict)* – Инициализира компресията
*   *compress\_more(f, o, buffer\_size, dict\_size\_large, flen, read_overall, t)* – Реализира самата компресия. Работи докато речника се запълни или входния буфер се запълни. Викан многократно от *compress* докато файлът бъде прочетен. При всяко извикване речникът се прави наново.
*   *output\_code\_for\_pattern\_to\_disc(buffer\_writer, position, o)* – Записва output буфера на диска.
*   *output\_code\_for\_pattern(buffer\_writer, position, code, large_dict)* – Записва код в текущия буфер.

## decompress

Реализира **де**компресията. Изпълнява се чрез извикване като метод или от command prompt-а. При извикване без параметри ще даде хелп.

*   *process\_command\_line(arguments, automated = False)* – Обработва аргументите от CMD
*   *decompress(file\_in, file\_out, buffer\_size, large\_dict)* – Инициализира декомпресията. Проверява дали файлът започва с магическия код, ако не хвърля *ArchiveError*. 
*   *decompress\_more(f, o, buffer\_size, dict\_size\_large, flen, read_overall, t)* – Реализира самата декомпресия. Работи докато няма повече за четене или е прочетена команда „FLUSH DICTIONARY“. Викан многократно от *decompress* докато файлът бъде прочетен. При всяко извикване речникът се прави наново.
*   *def get\_input\_code(f, large_dict)* – Прочита един (дву или три байтов) код.
*   *def output\_pattern\_for_code(o, pattern)* – За момента просто записва шаблон на диска.

## constants

Съдържа константи ползвани при декомпресията и компресията.

## compare_files

Сравнява файлове байт по байт. Използва се от Unit тестовете.

## test_*

Тестове

*   **test\_compression\_basic** – Тества със случайни изрязъци от wiki.xml-а. Общо взето занимава се с малка файлове
*   **test\_compression\_additional** – Допълнителен тест върху файлове от различни типове.
*   **test\_compression\_wiki** – Тест за компресия на BG WikiDUMP, като ползва най-тежките настройки. Освен Sanity Check, проверява дали е достигнато изисканото ниво на компресия (30%)
<li class="main">
  <b>test_bad_file</b> – Пробва да зададе на декомпресора файл, който не е от LZW формат.
</li>

## testdata\

Данните за тестовете

## doc\
Тази докемунтация